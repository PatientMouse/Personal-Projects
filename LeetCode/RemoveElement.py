class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        index = 0
        for num in nums:
            if(num != val):
                nums[index] = num
                index = index + 1
        return index