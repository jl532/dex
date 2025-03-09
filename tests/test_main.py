import random

from models.model import Model  # type: ignore


class TestModel:
    def test_add(self):
        a = random.random()
        b = random.random()
        expected = a + b
        assert Model.add(a, b) == expected

    def test_fiture(self, example_fixture):
        assert example_fixture == "example_fixture"
