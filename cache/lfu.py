import random
from collections import defaultdict, OrderedDict


class RandomizedSet:

    def __init__(self):
        self.hash_set = set()

    def insert(self, val: int) -> bool:
        if val in self.hash_set:
            return False
        self.hash_set.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.hash_set:
            return False
        self.hash_set.remove(val)
        return True

    def getRandom(self) -> int:
        if len(self.hash_set) == 0:
            return 0

        return random.choice(list(self.hash_set))

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
randomizedSet = RandomizedSet()
randomizedSet.insert(1) # Inserts 1 to the set. Returns true as 1 was inserted successfully.
randomizedSet.remove(2) # Returns false as 2 does not exist in the set.
randomizedSet.insert(2) # Inserts 2 to the set, returns true. Set now contains [1,2].
randomizedSet.getRandom() # getRandom() should return either 1 or 2 randomly.
randomizedSet.remove(1) # Removes 1 from the set, returns true. Set now contains [2].
randomizedSet.insert(2) # 2 was already in the set, so return false.
randomizedSet.getRandom() # Since 2 is the only number in the set, getRandom() will always return 2.

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {}  # Maps key -> (value, frequency)
        self.freq_to_keys = defaultdict(OrderedDict)  # Maps frequency -> OrderedDict of keys

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1

        value, freq = self.key_to_val_freq[key]
        # Update frequency
        self._update_freq(key, value, freq)
        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.key_to_val_freq:
            # Update existing key
            _, freq = self.key_to_val_freq[key]
            self._update_freq(key, value, freq)
        else:
            # Evict if at capacity
            if len(self.key_to_val_freq) == self.capacity:
                self._evict()

            # Insert new key
            self.key_to_val_freq[key] = (value, 1)
            self.freq_to_keys[1][key] = None
            self.min_freq = 1

    def _update_freq(self, key: int, value: int, freq: int) -> None:
        # Remove key from current frequency group
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Add key to the next frequency group
        self.key_to_val_freq[key] = (value, freq + 1)
        self.freq_to_keys[freq + 1][key] = None

    def _evict(self):
        # Evict the least frequently used key
        key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
        if not self.freq_to_keys[self.min_freq]:
            del self.freq_to_keys[self.min_freq]
        del self.key_to_val_freq[key]



# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

lfu = LFUCache(2)
lfu.put(1, 1) #  cache=[1,_], cnt(1)=1
lfu.put(2, 2) #  cache=[2,1], cnt(2)=1, cnt(1)=1
lfu.get(1)      # return 1
                 # cache=[1,2], cnt(2)=1, cnt(1)=2
lfu.put(3, 3) #  2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
                 # cache=[3,1], cnt(3)=1, cnt(1)=2
lfu.get(2)      # return -1 (not found)
lfu.get(3)      # return 3
                 # cache=[3,1], cnt(3)=2, cnt(1)=2
lfu.put(4, 4) #  Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
                 # cache=[4,3], cnt(4)=1, cnt(3)=2
lfu.get(1)      # return -1 (not found)
lfu.get(3)      # return 3
                 # cache=[3,4], cnt(4)=1, cnt(3)=3
lfu.get(4)      # return 4
                 # cache=[4,3], cnt(4)=2, cnt(3)=3