import sys
from setuptools import setup

assert (3, 6, 0) <= sys.version_info < (3, 10, 0), "sentry-flake8 requires Python 3.6 - 3.9."

setup(
    name="sentry-flake8",
    version="2.0.0",
    description="Sentry's custom flake8 checker plugin.",
    license="Apache 2.0",
    url="https://github.com/getsentry/sentry-flake8",
    author="Sentry",
    author_email="hello@sentry.io",
    install_requires=[
        "flake8>=3.8.0,<3.10.0",
        "flake8-bugbear==21.4.3",
    ],
    package_dir={"": "src"},
    extras_require={
        "tests": [
            "pytest==6.2.4",
        ]
    },
    python_requires=">=3.6, <3.10",
    py_modules=["sentry_check"],
    entry_points={"flake8.extension": ["S = sentry_check:SentryCheck"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
)
