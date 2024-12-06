import unittest

from pysorteddict import SortedDict


class TestInvalidConstruction(unittest.TestCase):
    """Test invalid construction of a sorted dictionary."""

    @classmethod
    def setUpClass(cls):
        cls.missing_argument = "function missing required argument 'key_type' (pos 1)"
        cls.wrong_argument = "constructor argument must be a supported type"

    def test_construct_without_argument(self):
        with self.assertRaises(TypeError) as ctx:
            SortedDict()
        self.assertEqual(self.missing_argument, ctx.exception.args[0])

    def test_construct_with_object_instance(self):
        with self.assertRaises(TypeError) as ctx:
            SortedDict(object())
        self.assertEqual(self.wrong_argument, ctx.exception.args[0])


if __name__ == "__main__":
    unittest.main()
