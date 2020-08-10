from setuptools import setup

setup(
    name="sentry-flake8",
    version="0.4.0",
    description="Sentry's custom flake8 checker plugin.",
    license="Apache 2.0",
    url="https://github.com/getsentry/sentry-flake8",
    author="Sentry",
    author_email="hello@sentry.io",
    install_requires=["flake8>=3.7.0,<3.8.0"],
    package_dir={"": "src"},
    extras_require={"tests": ["pytest==4.6.5",]},  # last 2.7 and 3.7 compat version
    py_modules=["sentry_check"],
    entry_points={"flake8.extension": ["B = sentry_check:SentryCheck"]},
)
