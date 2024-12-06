import unittest

from tests.utils import TestGenericKeys


class TestIntKeys(TestGenericKeys, unittest.TestCase):
    """Test a sorted dictionary with ``int`` keys."""

    def small_key(self):
        return self.rg.randrange(1000, 2000)

    def large_key(self):
        return self.rg.randrange(2000, 3000)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wrong_argument = "key must be of type <class 'int'>"

    def setUp(self):
        super().setUp(int)


if __name__ == "__main__":
    unittest.main()
