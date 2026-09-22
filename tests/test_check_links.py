"""Offline link-check regressions; all HTTP responses are mocked."""
import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_links', ROOT / 'scripts/check_links.py')
links = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = links
spec.loader.exec_module(links)


class LinkCheckerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='links-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'README.md').write_text('Source: https://example.com/docs\n')
        subprocess.run(['git', '-C', str(self.root), 'add', 'README.md'], check=True)

    def track(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        subprocess.run(['git', '-C', str(self.root), 'add', name], check=True)
        return p

    def cli(self, args):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(links, 'ROOT', self.root), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = links.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_inventory_includes_hidden_tracked_docs(self):
        self.track('.agents/skills/test.md', 'https://example.com/hidden')
        files, found = links.discover(self.root)
        self.assertEqual(files, 2)
        self.assertEqual(found['https://example.com/hidden'], ['.agents/skills/test.md:1'])

    def test_untracked_docs_are_not_uploaded_or_checked(self):
        (self.root / 'private.md').write_text('https://example.com/do-not-send')
        self.assertNotIn('https://example.com/do-not-send', links.discover(self.root)[1])

    def test_colon_filename_does_not_corrupt_url(self):
        self.track('notes:old.md', 'https://example.com/colon')
        self.assertEqual(links.discover(self.root)[1]['https://example.com/colon'], ['notes:old.md:1'])

    def test_balanced_parenthesis_and_markdown_wrapper(self):
        found = links.extract_links('[doc](https://example.com/f(x)). <https://example.com/a>')
        self.assertEqual(found, [('https://example.com/f(x)', 1), ('https://example.com/a', 1)])

    def test_html_escapes_and_source_lines(self):
        self.assertEqual(links.extract_links('one\nhttps://example.com/?a=1&amp;b=2'), [('https://example.com/?a=1&b=2', 2)])

    def test_duplicates_and_fragments_share_one_request(self):
        self.track('second.md', 'https://example.com/docs#chapter')
        found = links.discover(self.root)[1]
        self.assertEqual(len(found), 1)
        self.assertEqual(len(found['https://example.com/docs']), 2)

    def test_empty_stdin_and_foreign_cwd(self):
        scripts = self.root / 'scripts'; scripts.mkdir()
        for name in ['check_links.py', 'check-links.sh']:
            shutil.copyfile(ROOT / 'scripts' / name, scripts / name)
        foreign = self.root / 'elsewhere'; foreign.mkdir()
        run = subprocess.run(['bash', str(scripts / 'check-links.sh'), '--offline'], cwd=foreign,
                             input='', capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('"uniqueURLs": 1', run.stdout)
        self.assertIn('network=NOT_PERFORMED', run.stdout)

    def test_no_markdown_is_diagnostic_failure(self):
        subprocess.run(['git', '-C', str(self.root), 'rm', '-q', '--cached', 'README.md'], check=True)
        code, out, err = self.cli(['--offline'])
        self.assertEqual(code, 1); self.assertIn('no tracked Markdown', err)

    def test_no_urls_is_not_silent_pass(self):
        (self.root / 'README.md').write_text('No URLs')
        code, out, err = self.cli([])
        self.assertEqual(code, 1); self.assertIn('zero HTTP(S)', err)

    def test_offline_and_list_do_not_request(self):
        with patch.object(links, 'check_url', side_effect=AssertionError('network attempted')):
            for arg in ['--offline', '--list']:
                self.assertEqual(self.cli([arg])[0], 0)

    def test_symlink_doc_rejected(self):
        path = self.root / 'README.md'; path.unlink(); path.symlink_to(self.root / 'outside.md')
        with self.assertRaisesRegex(links.LinkError, 'symlink'):
            links.discover(self.root)

    def test_oversized_doc_rejected(self):
        (self.root / 'README.md').write_bytes(b'x' * (links.MAX_BYTES + 1))
        with self.assertRaisesRegex(links.LinkError, 'oversized'):
            links.discover(self.root)

    def test_non_utf8_fails_with_diagnostic(self):
        (self.root / 'README.md').write_bytes(b'\xff')
        self.assertEqual(self.cli(['--offline'])[0], 1)

    def test_no_credentials_local_addresses_or_non_web_ports(self):
        bad = ['http://localhost/a', 'http://127.0.0.1/a', 'http://[::1]/',
               'http://169.254.169.254/', 'http://10.0.0.1/', 'https://example.com:22/',
               'https://example.com:0/', 'https://user:password@example.com/', 'file:///etc/passwd',
               'https://example.com/\nfoo', 'https://example.com\\@127.0.0.1/']
        for url in bad:
            with self.subTest(url=url), self.assertRaises(links.LinkError): links.validate_url(url)

    def test_public_dns_is_pinned_in_curl_command_without_config_or_credentials(self):
        result = subprocess.CompletedProcess([], 0, 'HTTP/2 200\r\n\r\n\n200', '')
        with patch.object(links, 'public_address', return_value='93.184.216.34'), patch.object(links.subprocess, 'run', return_value=result) as run:
            self.assertEqual(links.request('https://example.com/', 'HEAD'), (200, None, 0))
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[:2], ['curl', '-q'])
        self.assertIn('example.com:443:93.184.216.34', cmd)
        self.assertNotIn('--location', cmd)
        self.assertFalse(run.call_args.kwargs.get('shell', False))

    def test_mixed_public_private_dns_rejected(self):
        values = [(socket.AF_INET, socket.SOCK_STREAM, 0, '', ('93.184.216.34', 443)),
                  (socket.AF_INET, socket.SOCK_STREAM, 0, '', ('127.0.0.1', 443))]
        with patch.object(links.socket, 'getaddrinfo', return_value=values), self.assertRaises(links.LinkError):
            links.public_address('example.com', 443)

    def test_ok_head(self):
        with patch.object(links, 'request', return_value=(200, None, 0)):
            self.assertEqual(links.check_url('https://example.com/').state, 'PASS')

    def test_head_unsupported_falls_back_to_get(self):
        with patch.object(links, 'request', side_effect=[(405, None, 0), (206, None, 0)]) as request:
            self.assertEqual(links.check_url('https://example.com/').state, 'PASS')
            self.assertEqual(request.call_args_list[-1].args[1], 'GET')

    def test_false_head_not_found_verified_by_get(self):
        with patch.object(links, 'request', side_effect=[(404, None, 0), (200, None, 0)]) as request:
            self.assertEqual(links.check_url('https://example.com/').state, 'PASS')
            self.assertEqual(request.call_args_list[-1].args[1], 'GET')

    def test_head_forbidden_can_be_verified_by_get(self):
        with patch.object(links, 'request', side_effect=[(403, None, 0), (200, None, 0)]):
            self.assertEqual(links.check_url('https://example.com/').state, 'PASS')

    def test_redirect_followed_and_revalidated(self):
        with patch.object(links, 'request', side_effect=[(301, '/new', 0), (200, None, 0)]) as request:
            self.assertEqual(links.check_url('https://example.com/').state, 'PASS')
            self.assertEqual(request.call_args_list[-1].args[0], 'https://example.com/new')

    def test_redirect_to_private_address_or_file_is_not_followed(self):
        for location in ['http://127.0.0.1/', 'file:///etc/passwd']:
            with patch.object(links, 'request', return_value=(302, location, 0)) as request:
                self.assertEqual(links.check_url('https://example.com/').state, 'FAIL')
                self.assertEqual(request.call_count, 1)

    def test_loop_and_missing_location_fail(self):
        for location in ['https://example.com/', None]:
            with patch.object(links, 'request', return_value=(302, location, 0)):
                self.assertEqual(links.check_url('https://example.com/').state, 'FAIL')

    def test_404_fails_with_source_diagnostic(self):
        with patch.object(links, 'request', return_value=(404, None, 0)):
            code, out, err = self.cli([])
            self.assertEqual(code, 1); self.assertIn('README.md:1', out); self.assertIn('LINK_CHECK_FAIL', out)

    def test_transport_and_server_errors_never_pass(self):
        for response in [(0, None, 28), (500, None, 0), (200, None, 60)]:
            with patch.object(links, 'request', return_value=response):
                self.assertEqual(links.check_url('https://example.com/').state, 'UNVERIFIED')
                self.assertEqual(self.cli([])[0], 1)

    def test_restricted_keeps_old_policy_but_never_claims_verified(self):
        for status in [401, 403, 429]:
            with patch.object(links, 'request', return_value=(status, None, 0)):
                code, out, err = self.cli([])
                self.assertEqual(code, 0); self.assertIn('RESTRICTED', out)
                self.assertIn('not verified', out); self.assertIn('LINK_CHECK_POLICY_PASS', out)


    def test_transient_failure_retried_once_and_reported(self):
        values = [links.Result('https://example.com/', 'UNVERIFIED', 0, 'timeout'),
                  links.Result('https://example.com/', 'PASS', 200, 'HTTP response')]
        with patch.object(links, 'check_once', side_effect=values) as check, patch.object(links.time, 'sleep'):
            result = links.check_url('https://example.com/')
            self.assertEqual(result.state, 'PASS')
            self.assertEqual(result.attempts, 2)
            self.assertEqual(check.call_count, 2)
            self.assertIn('prior attempt: timeout', result.detail)

    def test_hard_failures_are_not_retried_until_lucky_pass(self):
        with patch.object(links, 'check_once', return_value=links.Result('https://example.com/', 'FAIL', 404, 'missing')) as check:
            self.assertEqual(links.check_url('https://example.com/').state, 'FAIL')
            self.assertEqual(check.call_count, 1)

    def test_missing_curl_is_unverified_failure(self):
        with patch.object(links, 'request', side_effect=FileNotFoundError):
            self.assertEqual(links.check_url('https://example.com/').state, 'UNVERIFIED')


if __name__ == '__main__': unittest.main()
