import pytest

from src.serve import create_app


@pytest.fixture
def app():
    return create_app()
