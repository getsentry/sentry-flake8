from __future__ import absolute_import

import sys

try:
    import some_library
except ImportError as e:
    foo = e.message
else:
    foo = some_library.message
