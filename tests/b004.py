from __future__ import absolute_import

import sys


def this_is_a_bug():
    o = object()
    if hasattr(o, "__call__"):
        sys.stdout.write("Ooh, callable! Or is it?\n")
    if getattr(o, "__call__", False):
        sys.stdout.write("Ooh, callable! Or is it?\n")


def this_is_fine():
    o = object()
    if callable(o):
        sys.stdout.write("Ooh, this is actually callable.\n")
