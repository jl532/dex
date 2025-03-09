import pytest


def pytest_configure(config):
    pass


@pytest.fixture(scope="session")
def example_fixture():
    return "example_fixture"
