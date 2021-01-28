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
        self.assertEqual(errors, self.errors(B001(5, 0), B001(37, 4)))

    def test_b002(self):
        bbc = SentryCheck(filename=path("b002.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B002(12, 8), B002(17, 11)))

    def test_b003(self):
        bbc = SentryCheck(filename=path("b003.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B003(7, 0)))

    def test_b004(self):
        bbc = SentryCheck(filename=path("b004.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B004(8, 7), B004(10, 7)))

    def test_b005(self):
        bbc = SentryCheck(filename=path("b005.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B005(6, 0),
                B005(9, 0),
                B005(12, 0),
                B005(15, 0),
                B005(18, 0),
                B005(21, 0),
            ),
        )

    def test_b006_b008(self):
        bbc = SentryCheck(filename=path("b006_b008.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B006(16, 24),
                B006(20, 29),
                B006(24, 19),
                B006(28, 19),
                # B006(32, 31),
                B008(41, 38),
                # B006(55, 32),
            ),
        )

    def test_b007(self):
        bbc = SentryCheck(filename=path("b007.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B007(10, 4, vars=("i",)),
                B007(22, 12, vars=("k",)),
                B007(34, 4, vars=("i",)),
                B007(34, 12, vars=("k",)),
            ),
        )

    def test_b009_b010(self):
        bbc = SentryCheck(filename=path("b009_b010.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B009(11, 0), B010(18, 0)))

    def test_b101(self):
        bbc = SentryCheck(filename=path("b101.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B101(9, 0, vars=("assert_called_once",))))

    def test_b314(self):
        bbc = SentryCheck(filename=path("b314.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B314(3, 0)))

    def test_b317(self):
        bbc = SentryCheck(filename=path("b317.py"))
        errors = list(bbc.run())
        assert errors == [
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
            (
                5,
                0,
                "B317: Use ``from sentry.utils import json`` instead.",
                SentryCheck,
            ),
            (
                6,
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
