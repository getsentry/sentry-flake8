from __future__ import absolute_import

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
    B102,
    B301,
    B302,
    B303,
    B304,
    B305,
    B306,
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
        self.assertEqual(errors, self.errors(B101(8, 0, vars=("assert_called_once",))))

    def test_b102(self):
        bbc = SentryCheck(filename=path("b102.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B102(1, 1)))

    def test_b301_b302_b305(self):
        bbc = SentryCheck(filename=path("b301_b302_b305.py"))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B301(34, 4),
                B301(35, 4),
                B301(36, 4),
                B301(37, 4),
                B302(38, 4),
                B302(39, 4),
                B302(40, 4),
                B302(41, 4),
                B305(42, 4),
                B305(43, 4),
            ),
        )

    def test_b303_b304(self):
        bbc = SentryCheck(filename=path("b303_b304.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B303(21, 4), B304(38, 4)))

    def test_b306(self):
        bbc = SentryCheck(filename=path("b306.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B306(8, 10)))

    def test_b314(self):
        bbc = SentryCheck(filename=path("b314.py"))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B314(3, 0)))

    def test_b315(self):
        bbc = SentryCheck(filename=path("b315.py"))
        errors = list(bbc.run())
        assert errors == [
            (
                3,
                0,
                "B315: map is an iterable in Python 3. Use ``from sentry.utils.compat import map`` instead.",
                SentryCheck,
            ),
            (
                4,
                0,
                "B315: filter is an iterable in Python 3. Use ``from sentry.utils.compat import filter`` instead.",
                SentryCheck,
            ),
            (
                4,
                21,
                "B315: zip is an iterable in Python 3. Use ``from sentry.utils.compat import zip`` instead.",
                SentryCheck,
            ),
        ]

    def test_b316(self):
        bbc = SentryCheck(filename=path("b316.py"))
        errors = list(bbc.run())
        assert errors == [
            (
                10,
                0,
                "B316: itertools.izip is not available in Python 3. Use ``from sentry.utils.compat import zip as izip`` instead.",
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
        stdout = subprocess.check_output(["flake8", path("test_sentry_check.py")])
        self.assertEqual(stdout, b"")
        # self.assertEqual(proc.stderr, b'')


if __name__ == "__main__":
    unittest.main()
