from typing import List


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)  # 4 (dest = 3)
        result = []

        def dfs(index, tmp):  # 2 [ 0, 1 ]
            tmp.append(index)  # [0, 1, 2]

            # check for destination
            if index == n - 1:
                result.append(tmp.copy())
                return

            for neighbor in graph[index]:  # get_neighbors(index): # graph[0] => [1, 2]

                dfs(neighbor, tmp)  # 2 [ 0, 1 ]

                tmp.pop() # [ 0 , 1 ]

        dfs(0, [])

        return result
sol = Solution().allPathsSourceTarget([[1,2],[3],[3],[]])
print(sol)