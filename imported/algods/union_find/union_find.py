from typing import List


class DisjointUnionSets:
    def __init__(self, n):
        self.rank = [0] * n
        self.parent = list(range(n))

    def find(self, i):
        root = self.parent[i]
        if root != self.parent[i]:
            self.parent[i] = self.find(root)
            return self.parent[i]
        return root

    def unionSets(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return

        # union by rank
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[y_root] < self.rank[x_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

if __name__ == '__main__':
    n = 5
    dus = DisjointUnionSets(n)
    dus.unionSets(0, 2)
    dus.unionSets(4, 2)
    dus.unionSets(3, 1)

    # Check if 4 is a friend of 0
    if dus.find(4) == dus.find(0):
        print('Yes')
    else:
        print('No')

    # Check if 1 is a friend of 0
    if dus.find(1) == dus.find(0):
        print('Yes')
    else:
        print('No')

class UnionFind:

    def __init__(self, n: int):
        self.parents = {}
        self.rank = {}

        for i in range(1, n + 1):
            self.parents[i] = i
            self.rank[i] = 0

    # find parent of n using path compression (reduces time complexity from O(n) to O(logn))
    def find(self, x: int) -> int:
        if x != self.parents[x]:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def isSameComponent(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    # union by height/rank
    # return false if already connected, true otherwise
    def union(self, x: int, y: int) -> bool:
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False

        # Union by rank to keep the tree balanced
        if self.rank[root_x] < self.rank[root_y]:
            self.parents[root_x] = root_y
        elif self.rank[root_y] < self.rank[root_x]:
            self.parents[root_y] = root_x
        else:
            self.parents[root_x] = root_y
            self.rank[root_y] += 1
        return True

    def getNumComponents(self) -> int:
        count = 0
        for x in self.parents:
            if self.parents[x] == x:
                count += 1
        return count

"""
    Approach
        1. Use Union-Find data structure with optimizations:
            - Union by rank to keep the tree balanced
            - Path compression to flatter the tree
        2. Process each edge (u, v):
            - If u and v are already in the same component, we've found a cycle
                and this is our redundant connection
            - Otherwise, union the components containing u and v

    DS: parents{} map, ranks{} map

    Time:  O(m * α(n)) where:
        - m is number of edges
        - α(n) is Inverse Ackerman function (that is a very-slow growing function and considered to be constant for all practical purposes) ==> O(m)
    
    Space: O(n) for the parent and rank maps, where:
        - n is number of nodes
"""
class Solution:
    def __init__(self):
        self.parents = {}
        self.ranks = {}

    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        # Initialize parents and ranks
        for i in range(1, n + 1):
            self.parents[i] = i
            self.ranks[i] = 0

        redundant_connection = []
        # union by height/rank
        for x, y in edges:
            # If union returns False, the edge creates a cycle
            if not self.union(x, y):
                redundant_connection = [x, y]

        return redundant_connection

    def find(self, n):
        if n != self.parents[n]:
            self.parents[n] = self.find(self.parents[n]) # Path compression
        return self.parents[n]

    # return false if already connected, true otherwise
    def union(self, x, y):
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return False

        # Union by rank to keep the tree balanced
        if self.ranks[x_root] < self.ranks[y_root]:
            self.parents[x_root] = y_root
        elif self.ranks[y_root] < self.ranks[x_root]:
            self.parents[y_root] = x_root
        else:
            self.parents[x_root] = y_root
            self.ranks[y_root] += 1
        return True
"""
Approach:
    1. Use Union-Find data structure to identify accounts that belong to the same person
    2. Two accounts belong to the same person if they share at least one email address
    3. Process accounts and emails to build the connections:
       - Map each email to an account index
       - When an email appears in multiple accounts, union those accounts
    4. After building connections, merge accounts by:
       - Finding the representative account for each group
       - Collecting and sorting all emails for each merged account

Time Complexity:
    - O(n * k * log(n * k)) where:
        - n is the number of accounts
        - k is the average number of emails per account
        - The log factor comes from email sorting
        - Union-Find operations are effectively constant time with optimizations

Space Complexity:
    - O(n * k) for storing:
        - UnionFind data structure: O(n)
        - email_to_account mapping: O(n * k)
        - merged_accounts dictionary: O(n * k)
"""
class UnionFind:
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.rank = [1] * n

    def find(self, x):
        while x != self.par[x]:
            self.par[x] = self.par[self.par[x]]
            x = self.par[x]
        return x

    def union(self, x1, x2):
        p1, p2 = self.find(x1), self.find(x2)
        if p1 == p2:
            return False
        if self.rank[p1] > self.rank[p2]:
            self.par[p2] = p1
            self.rank[p1] += self.rank[p2]
        else:
            self.par[p1] = p2
            self.rank[p2] += self.rank[p1]
        return True

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))

        email_to_account = {}
        for i, account in enumerate(accounts):
            for j in range(1, len(account)): # skip name (index 0)
                email = account[j]
                # if this email was seen before, union current account with the previous one
                if email in email_to_account:
                    uf.union(i, email_to_account[email])
                else:
                    email_to_account[email] = i

        # collect emails by representative count
        merged_accounts = {}
        for email, account_idx in email_to_account.items():
            # find the representative for this account
            root = uf.find(account_idx)

            if root not in merged_accounts:
                # initialize with account name
                merged_accounts[root] = [accounts[root][0]]

            # add email
            merged_accounts[root].append(email)

        # format the result
        result = []
        for account_idx, emails in merged_accounts.items():
            # sort emails
            name = emails[0]
            sorted_emails = sorted(emails[1:])
            result.append([name] + sorted_emails)

        return result
sol = Solution().accountsMerge(accounts=[["neet","neet@gmail.com","neet_dsa@gmail.com"],["alice","alice@gmail.com"],["neet","bob@gmail.com","neet@gmail.com"],["neet","neetcode@gmail.com"]])
print(sol)


