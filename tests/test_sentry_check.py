import os
import subprocess
import unittest

from sentry_check import (
    B001,
    B002,
    B003,
    B004,
    B005,
    B006,
    B007,
    B008,
    B009,
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

    def test_b001(self):
        bbc = SentryCheck(filename=path("b001.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B001(3, 0), B001(35, 4)))

    def test_b002(self):
        bbc = SentryCheck(filename=path("b002.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B002(9, 8), B002(14, 11)))

    def test_b003(self):
        bbc = SentryCheck(filename=path("b003.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B003(5, 0)))

    def test_b004(self):
        bbc = SentryCheck(filename=path("b004.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B004(6, 7), B004(8, 7)))

    def test_b005(self):
        bbc = SentryCheck(filename=path("b005.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B005(4, 0),
                B005(7, 0),
                B005(10, 0),
                B005(13, 0),
                B005(16, 0),
                B005(19, 0),
            ),
        )

    def test_b006_b008(self):
        bbc = SentryCheck(filename=path("b006_b008.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B006(14, 24),
                B006(18, 29),
                B006(22, 19),
                B006(26, 19),
                B008(39, 38),
            ),
        )

    def test_b007(self):
        bbc = SentryCheck(filename=path("b007.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B007(8, 4, vars=("i",)),
                B007(20, 12, vars=("k",)),
                B007(32, 4, vars=("i",)),
                B007(32, 12, vars=("k",)),
            ),
        )

    def test_b009_b010(self):
        bbc = SentryCheck(filename=path("b009_b010.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B009(9, 0), B010(16, 0)))

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
