# sentry-flake8

[![PyPI](https://img.shields.io/pypi/v/sentry-flake8.svg)](https://pypi.org/project/sentry-flake8)
[![Travis](https://img.shields.io/travis/com/getsentry/sentry-flake8.svg)](https://travis-ci.com/getsentry/sentry-flake8)

Sentry's custom flake8 checker plugin.

## Install

`pip install sentry-flake8`

No further configuration is necessary for `flake8` to load the plugin. An example successful installation:

```
$ flake8 --version
3.5.0 (mccabe: 0.6.1, pycodestyle: 2.3.1, pyflakes: 1.6.0, sentry-flake8: 0.0.1) CPython 2.7.15 on Darwin
```

## Credits

This extension is inspired by, and based upon work done by Łukasz Langa in [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear).
