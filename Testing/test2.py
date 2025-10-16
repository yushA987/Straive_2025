import pytest

from calculator import Calculator

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(5, 10) == 15
    assert calc.add(10, 10) == 90

def test_subtract(calc):
    assert calc.subtract(100, 90) == 10
    assert calc.subtract(80, 20) == 60

