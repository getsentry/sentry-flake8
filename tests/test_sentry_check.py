import os
import subprocess
import unittest

from sentry_check import (
    B010,
    B101,
    B314,
    SentryCheck,
)


def path(*paths):
    return os.path.join(os.path.dirname(__file__), "cases", *paths)


class SentryCheckTestCase(unittest.TestCase):
    maxDiff = None

    def errors(self, *errors):
        return [SentryCheck.adapt_error(e) for e in errors]

    def test_b101(self):
        bbc = SentryCheck(filename=path("b101.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B101(6, 0, vars=("assert_called_once",))))

    def test_b314(self):
        bbc = SentryCheck(filename=path("b314.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B314(1, 0)))

    def test_b317(self):
        bbc = SentryCheck(filename=path("b317.py"))
        errors = list(bbc.run())
        assert errors == [
            (
                1,
                0,
                "B317: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                2,
                0,
                "B317: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                3,
                0,
                "B317: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                4,
                0,
                "B317: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
        ]

    def test_selfclean_sentry_check(self):
        stdout = subprocess.check_output(
            ["flake8", os.path.join(os.path.dirname(__file__), os.pardir, "src")]
        )
        self.assertEqual(stdout, b"")
        # self.assertEqual(proc.stderr, b"")

    def test_selfclean_test_sentry_check(self):
        stdout = subprocess.check_output(["flake8", __file__])
        self.assertEqual(stdout, b"")
        # self.assertEqual(proc.stderr, b'')


if __name__ == "__main__":
    unittest.main()
