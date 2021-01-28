import sys

if sys.version_info[:2] < (3, 6):
    sys.exit("sentry-flake8 requires at least Python 3.6.")

from setuptools import setup  # noqa: e402

setup(
    name="sentry-flake8",
    version="0.4.0",
    description="Sentry's custom flake8 checker plugin.",
    license="Apache 2.0",
    url="https://github.com/getsentry/sentry-flake8",
    author="Sentry",
    author_email="hello@sentry.io",
    install_requires=["flake8>=3.8.0,<3.9.0"],
    package_dir={"": "src"},
    extras_require={
        "tests": [
            "pytest==6.2.2",
        ]
    },  # last 2.7 and 3.7 compat version
    py_modules=["sentry_check"],
    entry_points={"flake8.extension": ["B = sentry_check:SentryCheck"]},
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
)
