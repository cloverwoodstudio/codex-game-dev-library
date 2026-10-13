#!/usr/bin/env python3
"""Fail-closed parser for exactly one expected Swift Testing behavioral failure.

This parser does not run Swift. The shell harness must execute the filtered test
in a disposable package and pass its original non-zero exit status here.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPECTED_NAME = "latest response wins even if older result arrives later"
EXPECTED_ASSERTION = "Expectation failed: !(await inbox.deliver(11, for: old))"
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")
STARTED = re.compile(r'^\s*[^\n]*?Test "([^"]+)" started\.', re.M)
FAILED = re.compile(r'^\s*[^\n]*?Test "([^"]+)" failed after', re.M)
PASSED = re.compile(r'^\s*[^\n]*?Test "([^"]+)" passed after', re.M)
RUN_FAILED = re.compile(r"Test run with 1 test in 1 suite failed after .* with 1 issue")
ASSERTION_LINE = re.compile(r'Test "' + re.escape(EXPECTED_NAME)
                            + r'" recorded an issue at RevisionedInboxTests.swift:\d+:\d+: '
                            + re.escape(EXPECTED_ASSERTION))
COMPILATION_FAILURE = re.compile(r"(?im)\berror:|compile command failed|fatal error")


def verify(log: str, exit_code: int) -> list[str]:
    normalized = ANSI_ESCAPE.sub("", log)
    errors: list[str] = []
    if exit_code == 0:
        errors.append("unexpected success: mutation not detected")
    if exit_code < 0:
        errors.append("test was terminated by signal")
    started = STARTED.findall(normalized)
    failed = FAILED.findall(normalized)
    passed = PASSED.findall(normalized)
    if started != [EXPECTED_NAME]:
        errors.append(f"wrong tests started: {started!r}")
    if failed != [EXPECTED_NAME]:
        errors.append(f"wrong tests failed: {failed!r}")
    if passed:
        errors.append(f"unexpected passing test records: {passed!r}")
    if not RUN_FAILED.search(normalized):
        errors.append("missing exactly-one-test/one-issue Swift Testing failed summary")
    if not ASSERTION_LINE.search(normalized):
        errors.append("missing exact stale-response expectation failure")
    if COMPILATION_FAILURE.search(normalized):
        errors.append("compiler/runtime crash detected instead of intended assertion failure")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--exit-code", required=True, type=int)
    args = parser.parse_args()
    try:
        source = args.log.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        print(f"NEGATIVE_REGRESSION_FAIL: cannot read test log: {error}", file=sys.stderr)
        return 1
    errors = verify(source, args.exit_code)
    if errors:
        for item in errors:
            print("NEGATIVE_REGRESSION_FAIL:", item, file=sys.stderr)
        return 1
    print("EXPECTED_RED_TEST_PASS exact_test=staleResponseIsRejected exact_issue=stale_generation_guard")
    print(f"EXPECTED_RED_TEST_EXIT={args.exit_code} (nonzero expected; harness PASS)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
