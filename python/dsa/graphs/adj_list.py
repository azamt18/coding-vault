"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
from collections import deque
from typing import Optional

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        graph_node = set()
        new_node = Node(node.val, set())
        graph_node.add(new_node)

        visited = set()
        visited.add(new_node)

        q = deque()
        q.append(new_node)

        while q:
            for _ in range(len(q)):
                cur = q.popleft()

                if cur in visited:
                    continue

                for neighbor in cur.neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)

        return graph_node

#// call cloneGraph with the following input: adjList = [[2], [1, 3], [2]]

# expected output: [[2], [1, 3], [2]]


