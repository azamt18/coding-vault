class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity: int):
        self.size = 0
        self.capacity = capacity
        self.map = [None] * self.capacity
        self.deleted = object()  # Special marker for deleted slots

    def insert(self, key: int, value: int) -> None:
        index = self.hash_function(key)
        while True:
            if self.map[index] is None or self.map[index] is self.deleted:
                self.map[index] = Pair(key, value)
                self.size += 1
                if self.getLoadFactor() >= 0.5:
                    self.resize()
                return
            elif self.map[index].key == key:
                self.map[index].value = value
                return
            index = (index + 1) % self.capacity

    def get(self, key: int) -> int:
        index = self.hash_function(key)
        while self.map[index] is not None:
            if self.map[index] is not self.deleted and self.map[index].key == key:
                return self.map[index].value
            index = (index + 1) % self.capacity
        return -1

    def remove(self, key: int) -> bool:
        index = self.hash_function(key)
        while self.map[index] is not None:
            if self.map[index] is not self.deleted and self.map[index].key == key:
                self.map[index] = self.deleted
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
        return False

    def getSize(self) -> int:
        return self.size

    def getCapacity(self) -> int:
        return self.capacity

    def getLoadFactor(self) -> float:
        return self.size / self.capacity

    def resize(self) -> None:
        old_map = self.map
        self.capacity *= 2
        self.map = [None] * self.capacity
        self.size = 0
        for pair in old_map:
            if pair and pair is not self.deleted:
                self.insert(pair.key, pair.value)

    def hash_function(self, key: int) -> int:
        return key % self.capacity