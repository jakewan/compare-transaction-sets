from setuptools import setup

__VERSION__ = "0.1.0"

setup(
    name="compare-transaction-sets",
    version=__VERSION__,
    author="Jacob Wan",
    author_email="jacobwan840@gmail.com",
    url="https://github.com/jakewan/compare-transaction-sets",
    packages=[
        "comparetransactionsets",
    ],
    entry_points={
        "console_scripts": ["compare-transaction-sets=comparetransactionsets.cli:main"],
    },
    python_requires=">=3.9",
    install_requires=[
        "appdirs",
        "requests",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    extras_require={
        "test": [
            "pytest",
            "responses",
            "flake8",
            "black",
            "isort",
        ]
    },
)
