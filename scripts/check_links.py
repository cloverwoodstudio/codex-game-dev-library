#!/usr/bin/env python3
"""Check HTTP(S) references in tracked Markdown; independent of stdin and rg."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
import html
import ipaddress
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
from urllib.parse import urldefrag, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r'''https?://[^\s<>`"']+''')
MAX_BYTES = 2_000_000
MAX_URLS = 2048
REDIRECTS = {301, 302, 303, 307, 308}


class LinkError(ValueError):
    """Invalid input or unsafe request; never silently skip it."""


def extract_links(content: str) -> list[tuple[str, int]]:
    result = []
    for line_no, line in enumerate(content.splitlines(), 1):
        for match in URL.finditer(line):
            url = html.unescape(match.group()).rstrip('.,;!')
            # Retain balanced parentheses in real URLs, remove Markdown wrappers.
            while url.endswith(')') and url.count(')') > url.count('('):
                url = url[:-1]
            while url.endswith(']') and url.count(']') > url.count('['):
                url = url[:-1]
            result.append((url, line_no))
    return result


def validate_url(url: str) -> tuple[str, int]:
    if len(url) > 8192 or any(c.isspace() or not c.isprintable() for c in url) or '\\' in url:
        raise LinkError('invalid URL characters or length')
    parsed = urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username is not None or parsed.password is not None:
        raise LinkError('only credential-free HTTP(S) URLs are accepted')
    port = parsed.port if parsed.port is not None else (443 if parsed.scheme == 'https' else 80)
    if port not in (80, 443):
        raise LinkError('non-web port rejected')
    host = parsed.hostname.encode('idna').decode('ascii').lower()
    if host == 'localhost' or host.endswith(('.localhost', '.local')) or '.' not in host and ':' not in host:
        raise LinkError('local hostname rejected')
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise LinkError('non-public address rejected')
    return host, port


def discover(root: Path) -> tuple[int, dict[str, list[str]]]:
    files = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', '*.md'],
                           stdin=subprocess.DEVNULL, capture_output=True, check=True, timeout=10).stdout
    names = [p for p in files.decode('utf-8').split('\0') if p]
    if not names or len(names) > 4096:
        raise LinkError('no tracked Markdown files or inventory too large')
    links: dict[str, list[str]] = {}
    for name in sorted(names):
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or not all(c.isprintable() for c in name):
            raise LinkError('unsafe tracked Markdown path')
        path = root
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise LinkError(f'symlink Markdown rejected: {name}')
        if not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise LinkError(f'Markdown missing or oversized: {name}')
        for url, line in extract_links(path.read_text(encoding='utf-8')):
            try:
                validate_url(url)
            except ValueError as exc:
                raise LinkError(f'{name}:{line}: {exc}') from exc
            url = urldefrag(url)[0]
            links.setdefault(url, []).append(f'{name}:{line}')
            if len(links) > MAX_URLS:
                raise LinkError('URL inventory exceeds bound')
    if not links:
        raise LinkError('zero HTTP(S) links discovered; refusing a vacuous PASS')
    return len(names), dict(sorted(links.items()))


def public_address(host: str, port: int) -> str:
    addresses = {entry[4][0] for entry in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)}
    if not addresses or any(not ipaddress.ip_address(a).is_global for a in addresses):
        raise LinkError('DNS contains a non-public address')
    # Pin the checked address in curl, avoiding a second unvalidated DNS lookup.
    return sorted(addresses, key=lambda a: (':' in a, a))[0]


def request(url: str, method: str) -> tuple[int, str | None, int]:
    host, port = validate_url(url)
    address = public_address(host, port)
    if ':' in address:
        address = f'[{address}]'
    cmd = ['curl', '-q', '--silent', '--show-error', '--globoff', '--noproxy', '*',
           '--proto', '=http,https', '--connect-timeout', '5', '--max-time', '15',
           '--resolve', f'{host}:{port}:{address}', '--dump-header', '-',
           '--output', '/dev/null', '--write-out', '\n%{http_code}']
    if method == 'HEAD':
        cmd.append('--head')
    else:
        cmd += ['--range', '0-0', '--max-filesize', '2000000']
    result = subprocess.run(cmd + ['--url', url], stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, timeout=18)
    header, _, status = result.stdout.rpartition('\n')
    locations = re.findall(r'^location:\s*(.*?)\r?$', header, re.I | re.M)
    return int(status) if status.isdigit() else 0, locations[-1] if locations else None, result.returncode


@dataclass(frozen=True)
class Result:
    url: str
    state: str
    status: int
    detail: str
    attempts: int = 1


def check_once(url: str) -> Result:
    current = url
    visited = set()
    try:
        for hop in range(6):
            if current in visited:
                return Result(url, 'FAIL', 0, 'redirect loop')
            visited.add(current)
            status, location, error = request(current, 'HEAD')
            # Some documentation servers reject HEAD with a misleading 404.
            if not error and status in (400, 401, 403, 404, 405, 410, 501):
                status, location, error = request(current, 'GET')
            if error:
                return Result(url, 'UNVERIFIED', status, f'curl transport exit {error}')
            if 200 <= status < 300:
                return Result(url, 'PASS', status, f'HTTP response after {hop} redirects; content/anchors not checked')
            if status in REDIRECTS:
                if not location:
                    return Result(url, 'FAIL', status, 'redirect without Location')
                current = urldefrag(urljoin(current, location))[0]
                validate_url(current)
                continue
            if status in (401, 403, 429):
                # Historical policy allows restrictions, but not as proof of validity.
                return Result(url, 'RESTRICTED', status, 'not verified: authentication, access or rate restriction')
            return Result(url, 'FAIL' if 400 <= status < 500 else 'UNVERIFIED', status, 'unexpected HTTP response')
        return Result(url, 'FAIL', 0, 'redirect limit exceeded')
    except LinkError as exc:
        return Result(url, 'FAIL', 0, str(exc))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return Result(url, 'UNVERIFIED', 0, type(exc).__name__)


def check_url(url: str) -> Result:
    first = check_once(url)
    if first.state != 'UNVERIFIED':
        return first
    # One retry for transient transport/server failure, never unlimited rerolls.
    time.sleep(0.25)
    final = check_once(url)
    return replace(final, attempts=2, detail=final.detail + '; prior attempt: ' + first.detail)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--offline', action='store_true', help='inventory/URL syntax only; no HTTP check')
    mode.add_argument('--list', action='store_true', help='list URLs and source lines without networking')
    parser.add_argument('--jobs', type=int, default=4, choices=range(1, 9), metavar='1..8')
    args = parser.parse_args(argv)
    try:
        files, links = discover(ROOT)
        print(json.dumps({'event': 'LINK_INVENTORY', 'markdownFiles': files, 'uniqueURLs': len(links)}), flush=True)
        if args.offline or args.list:
            if args.list:
                for url, sources in links.items():
                    print(json.dumps({'url': url, 'sources': sources}))
            print('LINK_INVENTORY_PASS network=NOT_PERFORMED')
            return 0
        counts = {'PASS': 0, 'RESTRICTED': 0, 'FAIL': 0, 'UNVERIFIED': 0}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for result in pool.map(check_url, links):
                counts[result.state] += 1
                print(json.dumps({**asdict(result), 'sources': links[result.url]}), flush=True)
        failed = counts['FAIL'] + counts['UNVERIFIED'] > 0
        print(json.dumps({'event': 'LINK_CHECK_FAIL' if failed else 'LINK_CHECK_POLICY_PASS',
                          **counts, 'restrictionPolicy': '401/403/429 reported but non-blocking; not verified',
                          'contentAndAnchorsVerified': False}), flush=True)
        return 1 if failed else 0
    except (LinkError, OSError, UnicodeError, ValueError, subprocess.SubprocessError) as exc:
        print(f'LINK_CHECK_ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
