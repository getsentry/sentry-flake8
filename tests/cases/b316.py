from __future__ import absolute_import

izip = 1
izip = lambda _:_

izip("foo")

from itertools import izip

izip

# XXX: not smart enough to detect that this overrides the problem import
# from sentry.utils.compat import zip as izip
# izip
