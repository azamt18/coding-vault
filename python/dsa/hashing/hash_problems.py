from typing import List

class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:

    def __init__(self, capacity: int):
        self.size = 0
        self.capacity = capacity
        self.map = [None] * self.capacity

    def insert(self, key: int, value: int) -> None:
        index = self.__hash__(key)
        while True:
            if self.map[index] == None:
                self.map[index] = Pair(key, value)
                self.size += 1
                if self.getLoadFactor() >= 0.5:
                    self.resize()
                return
            elif self.map[index].key == key:
                self.map[index].value = value
                return
            index += 1
            index = index % self.capacity

    def get(self, key: int) -> int:
        index = self.__hash__(key)
        while self.map[index] != None:
            if self.map[index].key == key:
                return self.map[index].value
            index += 1
            index = index % self.capacity
        return -1

    def remove(self, key: int) -> bool:
        if not self.get(key):
            return False
        index = self.__hash__(key)
        while True:
            if self.map[index].key == key:
                self.map[index] = None
                self.size -= 1
                return True
            index += 1
            index = index % self.capacity

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

    def getLoadFactor(self):
        return self.getSize() / self.getCapacity()

    def resize(self) -> None:
        self.capacity = 2 * self.capacity
        new_map = []
        for i in range(self.capacity):
            new_map.append(None)

        old_map = self.map
        self.map = new_map
        self.size = 0
        for pair in old_map:
            if pair:
                self.insert(pair.key, pair.value)

    def __hash__(self, key) -> int:
        return key % self.capacity

# ["HashTable", 2, "getCapacity", "insert", 6, 7, "getCapacity", "insert", 1, 2, "getCapacity", "insert", 3, 4, "getCapacity", "getSize"]
# input ["HashTable", 4, "getSize", "insert", 2, 2, "getSize", "insert", 3, 3, "getSize"]
# expected [null,0,null,1,null,2]
# Example usage of HashTable
hash_table = HashTable(4)  # Initialize HashTable with capacity 4
print(hash_table.getSize())  # Output: 0

hash_table.insert(2, 2)  # Insert key=2, value=2
print(hash_table.getSize())  # Output: 1

hash_table.insert(3, 3)  # Insert key=3, value=3
print(hash_table.getSize())  # Output: 2

class LRUCache:

    def __init__(self, capacity: int):
        self.hash_map = {}
        self.capacity = capacity
        self.lru_key = 0

    def get(self, key: int) -> int:
        if key in self.hash_map:
            self.lru_key = key
            return self.hash_map[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if len(self.hash_map) == self.capacity:
            del self.hash_map[self.lru_key]
        self.hash_map[key] = value

# // call LRUCache with the following order: ["LRUCache", [2], "put", [1, 1], "put", [2, 2], "get", [1], "put", [3, 3], "get", [2], "put", [4, 4], "get", [1], "get", [3], "get", [4]]
# // expected: [null,null,null,1,null,-1,null,-1,3,4]
# lRUCache = LRUCache(2)
# lRUCache.put(1, 10)  # cache: {1=10}
# lRUCache.get(1)  # return 10
# lRUCache.put(2, 20)  # cache: {1=10, 2=20}
# lRUCache.put(3, 30)  # cache: {2=20, 3=30}, key=1 was evicted
# lRUCache.get(2)  # returns 20
# lRUCache.get(1)  # return -1 (not found)

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}
        res = []
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in hash_map:
                res.append(hash_map[diff])
                res.append(i)
                break
            if nums[i] not in hash_map:
                hash_map[nums[i]] = i
        return res

# nums = [2,7,11,15]
# target = 13
# solution = Solution()
# res = solution.twoSum(nums, target)
# print(res)