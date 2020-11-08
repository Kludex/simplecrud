from subprocess import check_call


def check_format() -> None:
    check_call(["black", "--check", "--diff", "crudfactory/", "tests/"])


def format() -> None:
    check_call(["black", "crudfactory/", "tests/"])


def lint() -> None:
    check_call(["flake8", "crudfactory/", "tests/"])
    check_call(["mypy", "crudfactory/", "tests/"])


def test() -> None:
    check_call(
        [
            "pytest",
            "tests/",
            "--cov=crudfactory",
            "--cov-report=term-missing:skip-covered",
            "--cov-report=xml",
        ]
    )
