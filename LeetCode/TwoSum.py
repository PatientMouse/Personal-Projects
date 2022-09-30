class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        copy = nums.copy()
        copy.sort(reverse=True)
        sol = []
        while len(copy)>1:
            current = copy[0]
            copy.remove(current)
            y = target - current
            if y in copy:
                sol.append(nums.index(current))
                if nums.index(current) is nums.index(y):
                    nums.remove(current)
                    index = nums.index(y) +1
                    sol.append(index)
                    return sol
                sol.append(nums.index(y))
                return sol