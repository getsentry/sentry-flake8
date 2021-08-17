import os
import subprocess
import unittest

from sentry_check import (
    S001,
    S002,
    SentryCheck,
)


def path(*paths):
    return os.path.join(os.path.dirname(__file__), "cases", *paths)


class SentryCheckTestCase(unittest.TestCase):
    maxDiff = None

    def errors(self, *errors):
        return [SentryCheck.adapt_error(e) for e in errors]

    def test_S001(self):
        bbc = SentryCheck(filename=path("S001.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(S001(6, 0, vars=("assert_called_once",))))

    def test_S002(self):
        bbc = SentryCheck(filename=path("S002.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(S002(1, 0)))

    def test_S003(self):
        bbc = SentryCheck(filename=path("S003.py"))
        errors = list(bbc.run())
        assert errors == [
            (
                1,
                0,
                "S003: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                2,
                0,
                "S003: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                3,
                0,
                "S003: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                4,
                0,
                "S003: Use ``from sentry.utils import json`` instead.",
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
