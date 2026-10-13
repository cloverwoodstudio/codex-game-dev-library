"""Regression tests for the strict red-case validator (no Swift runtime)."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "samples/swift-testing-concurrency-pilot/verify_expected_red.py"
spec = importlib.util.spec_from_file_location("swift_red_validator", SOURCE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

NAME = "latest response wins even if older result arrives later"
ASSERTION = "Expectation failed: !(await inbox.deliver(11, for: old))"
GOOD = (
    f'◇ Test "{NAME}" started.\n'
    f'✘ Test "{NAME}" recorded an issue at RevisionedInboxTests.swift:12:9: {ASSERTION}\n'
    f'✘ Test "{NAME}" failed after 0.001 seconds with 1 issue.\n'
    '✘ Test run with 1 test in 1 suite failed after 0.001 seconds with 1 issue.\n'
)


class NegativeRedValidatorTests(unittest.TestCase):
    def check_rejected(self, log, code=1):
        self.assertTrue(module.verify(log, code), (log, code))

    def test_exact_expected_failure_is_accepted(self):
        self.assertEqual(module.verify(GOOD, 1), [])

    def test_ansi_wrapped_genuine_failure_accepted(self):
        self.assertEqual(module.verify("\x1b[31m" + GOOD + "\x1b[0m", 1), [])

    def test_original_review_false_pass_is_rejected(self):
        bogus = (
            f'◇ Test "{NAME}" started.\n'
            f'✔ Test "{NAME}" passed after 0.001 seconds.\n'
            '✘ Test "a task cancelled before delivery cannot publish" failed after 0.001 seconds.\n'
            '✘ Test run with 1 test in 1 suite failed after 0.001 seconds with 1 issue.\n'
        )
        self.check_rejected(bogus)

    def test_only_other_test_failed_is_rejected(self):
        self.check_rejected(GOOD.replace(NAME, "other test"))

    def test_same_test_but_wrong_assertion_is_rejected(self):
        self.check_rejected(GOOD.replace(ASSERTION, "Expectation failed: 1 == 2"))

    def test_missing_actual_issue_is_rejected(self):
        self.check_rejected(GOOD.replace(f'✘ Test "{NAME}" recorded an issue at RevisionedInboxTests.swift:12:9: {ASSERTION}\n', ""))

    def test_zero_executed_tests_is_rejected(self):
        self.check_rejected("Test run with 0 tests passed.")

    def test_compiler_error_does_not_count(self):
        self.check_rejected(GOOD + "error: failed to build target\n")

    def test_two_test_summary_is_rejected(self):
        self.check_rejected(GOOD.replace("1 test in 1 suite", "2 tests in 1 suite"))

    def test_ambiguous_multiple_started_tests_rejected(self):
        self.check_rejected(GOOD + '◇ Test "other test" started.\n')

    def test_successful_exit_is_rejected(self):
        self.check_rejected(GOOD, 0)


if __name__ == "__main__":
    unittest.main()
