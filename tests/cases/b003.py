from os import environ
import os


os.environ = {}
environ = {}  # that's fine, assigning a new meaning to the module-level name


class Object:
    os = None


o = Object()
o.os.environ = {}
