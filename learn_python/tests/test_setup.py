import pytest

@pytest.mark.django_db
def test_setup_is_working():
    # Simple test to check if pytest + Django DB works
    assert 1 + 1 == 2
