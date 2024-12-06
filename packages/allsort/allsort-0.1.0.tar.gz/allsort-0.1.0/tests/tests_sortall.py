import unittest
from allsort.sortall import sortit


class TestSorter(unittest.TestCase):
    def test_sort_list(self):
        self.assertEqual(sortit([3, 1, 2]), [1, 2, 3])

    def test_sort_dict_by_values(self):
        self.assertEqual(sortit({'a': 2, 'b': 1}, key=1), {'b': 1, 'a': 2})

    def test_sort_set(self):
        self.assertEqual(sortit({3, 1, 2}), [1, 2, 3])

    def test_sort_tuple(self):
        self.assertEqual(sortit((3, 1, 2)), (1, 2, 3))

    def test_unsupported_type(self):
        with self.assertRaises(TypeError):
            sortit(42)


if __name__ == "__main__":
    unittest.main()
