from __future__ import absolute_import

import ast
from collections import namedtuple
from functools import partial

import pycodestyle

__version__ = "0.0.1"


class SentryVisitor(ast.NodeVisitor):
    NODE_WINDOW_SIZE = 4

    def __init__(self, filename, lines):
        self.errors = []
        self.filename = filename
        self.lines = lines

        self.has_absolute_import = False
        self.node_stack = []
        self.node_window = []

    def finish(self):
        if not self.has_absolute_import:
            self.errors.append(B102(1, 1))

    def visit(self, node):
        self.node_stack.append(node)
        self.node_window.append(node)
        self.node_window = self.node_window[-self.NODE_WINDOW_SIZE :]
        super(SentryVisitor, self).visit(node)
        self.node_stack.pop()

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.errors.append(B001(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_UAdd(self, node):
        trailing_nodes = list(map(type, self.node_window[-4:]))
        if trailing_nodes == [ast.UnaryOp, ast.UAdd, ast.UnaryOp, ast.UAdd]:
            originator = self.node_window[-4]
            self.errors.append(B002(originator.lineno, originator.col_offset))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in B307.names:
            self.errors.append(B307(node.lineno, node.col_offset))

        if node.module == "__future__":
            for nameproxy in node.names:
                if nameproxy.name == "absolute_import":
                    self.has_absolute_import = True
                    break

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split(".", 1)[0] in B307.names:
                self.errors.append(B307(node.lineno, node.col_offset))

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            for bug in (B301, B302, B305):
                if node.func.attr in bug.methods:
                    call_path = ".".join(self.compose_call_path(node.func.value))
                    if call_path not in bug.valid_paths:
                        self.errors.append(bug(node.lineno, node.col_offset))
                    break
            else:
                self.check_for_b005(node)
            for bug in (B312,):
                if node.func.attr in bug.methods:
                    call_path = ".".join(self.compose_call_path(node.func.value))
                    if call_path in bug.invalid_paths:
                        self.errors.append(bug(node.lineno, node.col_offset))
                    break
        else:
            self.check_for_b004(node)
            self.check_for_b009_b010(node)
        self.generic_visit(node)

    def check_for_b004(self, node):
        try:
            if (
                node.func.id in ("getattr", "hasattr")
                and node.args[1].s == "__call__"  # noqa: W503
            ):
                self.errors.append(B004(node.lineno, node.col_offset))
        except (AttributeError, IndexError):
            pass

    def check_for_b009_b010(self, node):
        try:
            if (
                node.func.id == "getattr"
                and len(node.args) == 2  # noqa: W503
                and isinstance(node.args[1], ast.Str)  # noqa: W503
            ):
                self.errors.append(B009(node.lineno, node.col_offset))
            elif (
                node.func.id == "setattr"
                and len(node.args) == 3  # noqa: W503
                and isinstance(node.args[1], ast.Str)  # noqa: W503
            ):
                self.errors.append(B010(node.lineno, node.col_offset))
        except (AttributeError, IndexError):
            pass

    def visit_Attribute(self, node):
        call_path = list(self.compose_call_path(node))
        if ".".join(call_path) == "sys.maxint":
            self.errors.append(B304(node.lineno, node.col_offset))
        elif len(call_path) == 2 and call_path[1] == "message":
            name = call_path[0]
            for elem in reversed(self.node_stack[:-1]):
                if isinstance(elem, ast.ExceptHandler) and elem.name.id == name:
                    self.errors.append(B306(node.lineno, node.col_offset))
                    break

        if node.attr in B101.methods:
            self.errors.append(B101(node.lineno, node.col_offset, vars=(node.attr,)))

    def visit_Assign(self, node):
        # TODO(dcramer): pretty sure these aren't working correctly on Python2
        if isinstance(self.node_stack[-2], ast.ClassDef):
            # note: by hasattr belowe we're ignoring starred arguments, slices
            # and tuples for simplicity.
            assign_targets = {t.id for t in node.targets if hasattr(t, "id")}
            if "__metaclass__" in assign_targets:
                self.errors.append(B303(node.lineno, node.col_offset))
            if "__unicode__" in assign_targets:
                self.errors.append(B313(node.lineno, node.col_offset))
        elif len(node.targets) == 1:
            t = node.targets[0]
            if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name):
                if (t.value.id, t.attr) == ("os", "environ"):
                    self.errors.append(B003(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_For(self, node):
        self.check_for_b007(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        # self.check_for_b902(node)
        self.check_for_b006(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # self.check_for_b901(node)
        # self.check_for_b902(node)
        self.check_for_b006(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # self.check_for_b903(node)
        self.generic_visit(node)

    def visit_Name(self, node):
        for bug in (B308, B309, B310, B311):
            if node.id in bug.names:
                self.errors.append(bug(lineno=node.lineno, col=node.col_offset))
        if node.id == "print":
            self.check_print(node)

    def visit_Print(self, node):
        self.check_print(node)

    def check_print(self, node):
        if not self.filename.startswith("tests/"):
            self.errors.append(B314(lineno=node.lineno, col=node.col_offset))

    def check_for_b005(self, node):
        if node.func.attr not in B005.methods:
            return  # method name doesn't match

        if len(node.args) != 1 or not isinstance(node.args[0], ast.Str):
            return  # used arguments don't match the builtin strip

        call_path = ".".join(self.compose_call_path(node.func.value))
        if call_path in B005.valid_paths:
            return  # path is exempt

        s = node.args[0].s
        if len(s) == 1:
            return  # stripping just one character

        if len(s) == len(set(s)):
            return  # no characters appear more than once

        self.errors.append(B005(node.lineno, node.col_offset))

    def check_for_b006(self, node):
        for default in node.args.defaults:
            if isinstance(default, B006.mutable_literals):
                self.errors.append(B006(default.lineno, default.col_offset))
            elif isinstance(default, ast.Call):
                call_path = ".".join(self.compose_call_path(default.func))
                if call_path in B006.mutable_calls:
                    self.errors.append(B006(default.lineno, default.col_offset))
                elif call_path not in B008.immutable_calls:
                    self.errors.append(B008(default.lineno, default.col_offset))

    def check_for_b007(self, node):
        targets = NameFinder()
        targets.visit(node.target)
        ctrl_names = set(filter(lambda s: not s.startswith("_"), targets.names))
        body = NameFinder()
        for expr in node.body:
            body.visit(expr)
        used_names = set(body.names)
        for name in sorted(ctrl_names - used_names):
            n = targets.names[name][0]
            self.errors.append(B007(n.lineno, n.col_offset, vars=(name,)))

    def compose_call_path(self, node):
        if isinstance(node, ast.Attribute):
            for item in self.compose_call_path(node.value):
                yield item
            yield node.attr
        elif isinstance(node, ast.Name):
            yield node.id


class NameFinder(ast.NodeVisitor):
    """Finds a name within a tree of nodes.
    After `.visit(node)` is called, `found` is a dict with all name nodes inside,
    key is name string, value is the node (useful for location purposes).
    """

    def __init__(self, names=None):
        self.names = names or {}

    def visit_Name(self, node):
        self.names.setdefault(node.id, []).append(node)

    def visit(self, node):
        """Like super-visit but supports iteration over lists."""
        if not isinstance(node, list):
            return super(NameFinder, self).visit(node)

        for elem in node:
            super(NameFinder, self).visit(elem)
        return node


class SentryCheck(object):
    name = "sentry-flake8"
    version = __version__

    def __init__(self, tree=None, filename=None, lines=None, visitor=SentryVisitor):
        self.tree = tree
        self.filename = filename
        self.lines = lines
        self.visitor = visitor

    def run(self):
        if not self.tree or not self.lines:
            self.load_file()

        visitor = self.visitor(filename=self.filename, lines=self.lines)
        visitor.visit(self.tree)
        visitor.finish()
        for e in visitor.errors:
            try:
                if pycodestyle.noqa(self.lines[e.lineno - 1]):
                    continue
            except IndexError:
                pass

            yield self.adapt_error(e)

    def load_file(self):
        """
        Loads the file in a way that auto-detects source encoding and deals
        with broken terminal encodings for stdin.
        Stolen from flake8_import_order because it's good.
        """

        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    # def run(self):
    #     visitor = Py2to3Visitor()
    #     visitor.visit(self.tree)
    #     for code, lineno, name in visitor.errors:
    #         yield lineno, 0, self.codes[code], type(self)

    @classmethod
    def adapt_error(cls, e):
        """Adapts the extended error namedtuple to be compatible with Flake8."""
        return e._replace(message=e.message.format(*e.vars))[:4]


error = namedtuple("error", "lineno col message type vars")
Error = partial(partial, error, message=u"", type=SentryCheck, vars=())

B001 = Error(
    message=u"B001: Do not use bare `except:`, it also catches unexpected "
    "events like memory errors, interrupts, system exit, and so on.  "
    "Prefer `except Exception:`.  If you're sure what you're doing, "
    "be explicit and write `except BaseException:`."
)

B002 = Error(
    message=u"B002: Python does not support the unary prefix increment. Writing "
    "++n is equivalent to +(+(n)), which equals n. You meant n += 1."
)

B003 = Error(
    message=u"B003: Assigning to `os.environ` doesn't clear the environment. "
    "Subprocesses are going to see outdated variables, in disagreement "
    "with the current process. Use `os.environ.clear()` or the `env=` "
    "argument to Popen."
)

B004 = Error(
    message=u"B004: Using `hasattr(x, '__call__')` to test if `x` is callable "
    "is unreliable. If `x` implements custom `__getattr__` or its "
    "`__call__` is itself not callable, you might get misleading "
    "results. Use `callable(x)` for consistent results."
)

B005 = Error(
    message=u"B005: Using .strip() with multi-character strings is misleading "
    "the reader. It looks like stripping a substring. Move your "
    "character set to a constant if this is deliberate. Use "
    ".replace() or regular expressions to remove string fragments."
)
B005.methods = {"lstrip", "rstrip", "strip"}
B005.valid_paths = {}

B006 = Error(
    message=u"B006: Do not use mutable data structures for argument defaults. "
    "All calls reuse one instance of that data structure, persisting "
    "changes between them."
)
B006.mutable_literals = (ast.Dict, ast.List, ast.Set)
B006.mutable_calls = {
    "Counter",
    "OrderedDict",
    "collections.Counter",
    "collections.OrderedDict",
    "collections.defaultdict",
    "collections.deque",
    "defaultdict",
    "deque",
    "dict",
    "list",
    "set",
}
B007 = Error(
    message=u"B007: Loop control variable {!r} not used within the loop body. "
    "If this is intended, start the name with an underscore."
)
B008 = Error(
    message=u"B008: Do not perform calls in argument defaults. The call is "
    "performed only once at function definition time. All calls to your "
    "function will reuse the result of that definition-time call. If "
    "this is intended, assign the function call to a module-level "
    "variable and use that variable as a default value."
)
B008.immutable_calls = {"tuple", "frozenset"}
B009 = Error(
    message=u"B009: Do not call getattr with a constant attribute value, "
    "it is not any safer than normal property access."
)
B010 = Error(
    message=u"B010: Do not call setattr with a constant attribute value, "
    "it is not any safer than normal property access."
)

B101 = Error(
    message=u"B101: Avoid using the {} mock call as it is "
    "confusing and prone to causing invalid test "
    "behavior."
)
B101.methods = {
    "assert_calls",
    "assert_not_called",
    "assert_called",
    "assert_called_once",
    "not_called",
    "called_once",
    "called_once_with",
}

B102 = Error(message=u"B102: Missing `from __future__ import absolute_import`")

# Those could be false positives but it's more dangerous to let them slip
# through if they're not.
B301 = Error(
    message=u"B301: Python 3 does not include .iter* methods on dictionaries. "
    "Use `six.iter*` or `future.utils.iter*` instead."
)
B301.methods = {"iterkeys", "itervalues", "iteritems", "iterlists"}
B301.valid_paths = {"six", "future.utils", "builtins"}

B302 = Error(
    message=u"B302: Python 3 does not include .view* methods on dictionaries. "
    "Remove the ``view`` prefix from the method name. Use `six.view*` "
    "or `future.utils.view*` instead."
)
B302.methods = {"viewkeys", "viewvalues", "viewitems", "viewlists"}
B302.valid_paths = {"six", "future.utils", "builtins"}

B303 = Error(
    message=u"B303: __metaclass__ does not exist in Python 3. Use "
    "use `@six.add_metaclass()` instead."
)

B304 = Error(message=u"B304: sys.maxint does not exist in Python 3. Use `sys.maxsize`.")

B305 = Error(
    message=u"B305: .next() does not exist in Python 3. Use ``six.next()`` " "instead."
)
B305.methods = {"next"}
B305.valid_paths = {"six", "future.utils", "builtins"}

B306 = Error(
    message=u"B306: ``BaseException.message`` has been deprecated as of Python "
    "2.6 and is removed in Python 3. Use ``str(e)`` to access the "
    "user-readable message. Use ``e.args`` to access arguments passed "
    "to the exception."
)

B307 = Error(
    message=u"B307: Python 3 has combined urllib, urllib2, and urlparse into "
    "a single library. For Python 2 compatibility, utilize the "
    "six.moves.urllib module."
)
B307.names = {"urllib", "urlib2", "urlparse"}

B308 = Error(
    message=u"B308: The usage of ``str`` differs between Python 2 and 3. Use "
    "``six.binary_type`` instead."
)
B308.names = {"str"}

B309 = Error(
    message=u"B309: ``unicode`` does not exist in Python 3. Use "
    "``six.text_type`` instead."
)
B309.names = {"unicode"}

B310 = Error(
    message=u"B310: ``basestring`` does not exist in Python 3. Use "
    "``six.string_types`` instead."
)
B310.names = {"basestring"}

B311 = Error(
    message=u"B311: ``long`` should not be used. Use int instead, and allow "
    "Python to deal with handling large integers."
)
B311.names = {"long"}

B312 = Error(
    message=u"B312: ``cgi.escape`` and ``html.escape`` should not be used. Use "
    "sentry.utils.html.escape instead."
)
B312.methods = {"escape"}
B312.invalid_paths = {"cgi", "html"}

B313 = Error(
    message=u"B313: ``__unicode__`` should not be defined on classes. Define "
    "just ``__str__`` returning a unicode text string, and use the "
    "sentry.utils.compat.implements_to_string class decorator."
)

B314 = Error(message=u"B314: print functions or statements are not allowed.")
