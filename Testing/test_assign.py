import pytest
from classify import Classify  # replace 'your_module' with the actual module name


@pytest.fixture
def classifier():
    return Classify()


def test_classify_even(classifier):
    assert classifier.classifyy(4) == "even"

def test_classify_divisible_by_3(classifier):
    assert classifier.classifyy(9) == "divisible by 3"

def test_classify_other(classifier):
    assert classifier.classifyy(7) == "other"

def test_classify_edge_cases(classifier):
    assert classifier.classifyy(0) == "even"
    assert classifier.classifyy(-6) == "even"
    assert classifier.classifyy(-9) == "divisible by 3"
