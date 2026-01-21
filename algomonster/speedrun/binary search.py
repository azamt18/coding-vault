from collections import defaultdict

""" https://leetcode.com/problems/snapshot-array/ """
class SnapshotArray:
    # history of each index in the form pairs (snap_id, val)
    # tc: O(1) for set, O(1) for snap, O(n) for get (where n = number of snapshots for that index)
    # sc: O(k) where k = total number of set operations across all snapshots
    def __init__(self, length: int):
        self.histories = [[(-1,0)] for _ in range(length)]
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        self.histories[index].append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        last_val = 0
        for s, v in self.histories[index]:
            if s <= snap_id:
                last_val = v
            else:
                break
        return last_val

    # naive sln with hashmap of arrays
    # tc: (1) for set, (n) for snap, (1) for get
    # sc: (n x s), s = snapshots number
    # def __init__(self, length: int):
    #     self.length = length
    #     self.hashmap = defaultdict(list)
    #     self.current_snapshot = 0
    #     self.hashmap[self.current_snapshot] = [0] * self.length
    #
    # def set(self, index: int, val: int) -> None:
    #     curr_arr = self.hashmap[self.current_snapshot]
    #     if index < 0 or index > len(curr_arr):
    #         return
    #     curr_arr[index] = val
    #
    # def snap(self) -> int:
    #     snap_id = self.current_snapshot
    #     curr_arr = self.hashmap[self.current_snapshot]
    #
    #     self.current_snapshot += 1
    #     self.hashmap[self.current_snapshot] = curr_arr.copy()
    #     return snap_id
    #
    # def get(self, index: int, snap_id: int) -> int:
    #     if snap_id not in self.hashmap:
    #         return -1
    #     return self.hashmap[snap_id][index]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)