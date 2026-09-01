from typing import List
from collections import defaultdict, deque


# topological sort, tc: (v) + (e) + (vlogv), sc: (v+e) + (v) + (v)
def eventualSafeNodes(nodes: List[List[int]]) -> List[int]:
    # build graph from adjacency list
    # find terminal nodes (hash set)
    # build nodes_state: 0=unvisited, 1=processing, 2=processed
    # check each node in graph directly for safety via dfs
    # if during the cycle found processing(1) - it's cycle
    # set node's state 1 at the beginning, 2 at the end
    # if safety check will succeed, append current node to result
    # sort final result in asc order

    # graph = defaultdict(list)  # sc(v+e)
    # t_nodes = set()
    # for i in range(len(nodes)):
    #     #     0     1     2   3   4  5 6
    #     # [[1,2],[2,3],[5],[0],[5],[],[]]
    #     # { 0: [1,2], 1: [2,3] }
    #
    #     graph[i].extend(nodes[i])
    #     if len(nodes[i]) == 0:
    #         # no outgoing edges -> terminal node
    #         # { 5 , 6 }
    #         t_nodes.add(i)

    # visited = set() # redundant, use nodes_state{} instead
    # t_nodes = { 5,6 }
    nodes_state = defaultdict(int)  # sc(v)
    for i in range(len(nodes)):
        nodes_state[i] = 0

    def dfs(node):
        # base case
        # if node in t_nodes:
        #     return True
        state = nodes_state[node]
        if state != 0: # 1 or 2
            if state == 1:
                # node is processing, cycle detected
                return False
            elif state == 2:
                # node is already processed
                return True

        # visited.add(node)
        nodes_state[node] = 1 # processing
        for ngh in nodes[node]:  # tc(e)
            if nodes_state[ngh] == 1:
                # cycle detected
                return False
            if not dfs(ngh):
                # one of neighbors is unsafe
                return False

        nodes_state[node] = 2
        return True

    result = []  # sc(v)
    for i in range(len(nodes)):  # tc(v)
        if dfs(i):
            result.append(i)

    # sort
    result.sort()  # tc(vlogv)
    return result

eventualSafeNodes([[1, 2], [2, 3], [5], [0], [5], [], []])


def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:

    graph = defaultdict(list)
    for i in range(numCourses):
        graph[i] = []
    for a, b in prerequisites:
        graph[b].append(a)

    in_degree = {node: 0 for node in graph}
    print(graph)
    print(in_degree)

    for node in graph:
        for ngh in graph[node]:
            in_degree[ngh] += 1

    queue = deque([])
    for node in in_degree:
        if in_degree[node] == 0:
            queue.append(node)

    top_order = []
    while queue:
        node = queue.popleft()
        top_order.append(node)
        for ngh in graph[node]:
            in_degree[ngh] -= 1
            if in_degree[ngh] == 0:
                queue.append(ngh)

    if len(top_order) != len(graph):
        return []

    return top_order
