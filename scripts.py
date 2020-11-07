from subprocess import check_call


def check_format() -> None:
    check_call(["black", "--check", "--diff", "crud_factory/", "tests/"])


def format() -> None:
    check_call(["black", "crud_factory/", "tests/"])


def lint() -> None:
    check_call(["flake8", "crud_factory/", "tests/"])
    check_call(["mypy", "crud_factory/", "tests/"])


def test() -> None:
    check_call(
        [
            "pytest",
            "tests/",
            "--cov=crud_factory",
            "--cov-report=term-missing:skip-covered",
            "--cov-report=xml",
        ]
    )


def coveralls() -> None:
    check_call(["coveralls"])
