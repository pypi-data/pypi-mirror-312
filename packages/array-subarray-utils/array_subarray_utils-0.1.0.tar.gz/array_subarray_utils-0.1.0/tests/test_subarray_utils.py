import unittest
from array_subarray_utils import SubarrayUtils

class TestSubarrayUtils(unittest.TestCase):
    def test_max_subarray_sum(self):
        self.assertEqual(SubarrayUtils.max_subarray_sum([5, -3, 5]), 10)
        self.assertEqual(SubarrayUtils.max_subarray_sum([-2, -3, -1]), -1)

    def test_min_subarray_sum(self):
        self.assertEqual(SubarrayUtils.min_subarray_sum([5, -3, 5]), -3)
        self.assertEqual(SubarrayUtils.min_subarray_sum([-2, -3, -1]), -6)

    def test_max_circular_subarray_sum(self):
        self.assertEqual(SubarrayUtils.max_circular_subarray_sum([5, -3, 5]), 12)
        self.assertEqual(SubarrayUtils.max_circular_subarray_sum([-2, -3, -1]), -1)

    def test_min_circular_subarray_sum(self):
        self.assertEqual(SubarrayUtils.min_circular_subarray_sum([5, -3, 5]), -3)
        self.assertEqual(SubarrayUtils.min_circular_subarray_sum([-2, -3, -1]), -6)

if __name__ == "__main__":
    unittest.main()
