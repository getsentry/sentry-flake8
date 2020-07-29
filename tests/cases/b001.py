from __future__ import absolute_import

try:
    import something
except:
    # should be except ImportError:
    import something_else as something

try:
    pass
except ValueError:
    # no warning here, all good
    pass

try:
    pass
except (KeyError, IndexError):
    # no warning here, all good
    pass

try:
    pass
except BaseException as be:
    # no warning here, all good
    pass

try:
    pass
except BaseException:
    # no warning here, all good
    pass


def func(**kwargs):
    try:
        is_debug = kwargs["debug"]
    except:
        # should be except KeyError:
        return

    results = something.call(debug=is_debug)
    try:
        results["ok"]
    except:  # noqa
        # warning silenced
        return
