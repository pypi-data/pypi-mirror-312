class SubarrayUtils:
    @staticmethod
    def max_subarray_sum(arr):
        """Find the maximum sum of a contiguous subarray using Kadane's Algorithm."""
        max_ending_here = max_so_far = arr[0]
        for num in arr[1:]:
            max_ending_here = max(num, max_ending_here + num)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far

    @staticmethod
    def min_subarray_sum(arr):
        """Find the minimum sum of a contiguous subarray."""
        min_ending_here = min_so_far = arr[0]
        for num in arr[1:]:
            min_ending_here = min(num, min_ending_here + num)
            min_so_far = min(min_so_far, min_ending_here)
        return min_so_far

    @staticmethod
    def max_circular_subarray_sum(arr):
        """
        Find the maximum sum of a circular subarray.
        Uses the relationship:
        max_circular = max(max_subarray, total_sum - min_subarray)
        """
        total_sum = sum(arr)
        max_normal = SubarrayUtils.max_subarray_sum(arr)
        min_normal = SubarrayUtils.min_subarray_sum(arr)

        # If all elements are negative, max_circular would incorrectly be zero
        if max_normal < 0:
            return max_normal

        max_circular = max(max_normal, total_sum - min_normal)
        return max_circular

    @staticmethod
    def min_circular_subarray_sum(arr):
        """
        Find the minimum sum of a circular subarray.
        Uses the relationship:
        min_circular = min(min_subarray, total_sum - max_subarray)
        """
        total_sum = sum(arr)
        min_normal = SubarrayUtils.min_subarray_sum(arr)
        max_normal = SubarrayUtils.max_subarray_sum(arr)

        # If all elements are positive, min_circular would incorrectly be zero
        if min_normal > 0:
            return min_normal

        min_circular = min(min_normal, total_sum - max_normal)
        return min_circular
