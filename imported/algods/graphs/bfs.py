from collections import deque, defaultdict
from typing import List


def bfs_adj_list(graph, start_node):
    queue = deque()
    visited = set()

    queue.append(start_node)
    visited.add(start_node)

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)


# Example usage
adj_list_graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5, 6],
    3: [1],
    4: [1],
    5: [2],
    6: [2]
}
# print("BFS using Adjacency List:")
# bfs_adj_list(adj_list_graph, 0)

def bfs_adj_matrix(graph, start_node):
    queue = deque()
    visited = set()

    queue.append(start_node)
    visited.add(start_node)

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        for neighbor, is_connected in enumerate(graph[node]):
            if is_connected and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

# Example usage
adj_matrix_graph = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0]
]
# print("\nBFS using Adjacency Matrix:")
# bfs_adj_matrix(adj_matrix_graph, 0)


def checkIfPrerequisite(numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
    result = []

    # step 1: build graph on prerequisites
    adjList = {}
    # adjList = defaultdict(list)
    for startNode, endNode in prerequisites:
        adjList[startNode] = adjList.get(startNode, []) + [endNode]

    isReachable = [[False for _ in range(numCourses)] for _ in range(numCourses)]

    def bfs(startNode):
        queue = deque([startNode])

        while queue:
            node = queue.popleft()
            isReachable[startNode][node] = True
            if node in adjList:
                for nei in adjList[node]:
                    queue.append(nei)

    for node, neis in adjList.items():
        bfs(node)
    print(isReachable, 'isReachable')

    for start, end in queries:
        result.append(isReachable[start][end])

    return result
res = checkIfPrerequisite(3, [[1,2],[1,0],[2,0]], [[1,0],[1,2]])
print(res)