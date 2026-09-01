import heapq
from collections import defaultdict, deque
from typing import List, Dict


def network_delay_time(times, n, k):
    adj_dict = defaultdict(list)
    for src, dest, time in times:
        adj_dict[src].append((dest, time))

    pq = []  # (time, src)
    heapq.heappush(pq, (0, k))

    visited = set()
    visited.add(k)
    delay, counter = 0, 0

    distances = {node: float('inf') for node in range(1, n + 1)}
    distances[k] = 0

    while pq:
        current_time, current_node = heapq.heappop(pq)

        if current_time > distances[current_node]: # already found a better way
            continue

        # process neighbors
        for neighbor, time in adj_dict[current_node]:
            new_time = current_time + time

            if new_time < distances[neighbor]: # found a better path
                distances[neighbor] = new_time
                heapq.heappush(pq, (new_time, neighbor))

    # max time
    max_time = max(distances.values())

    return max_time if max_time < float('inf') else -1
network_delay_time([[1, 2, 1], [2, 3, 1], [3, 4, 1]], 4, 1)


# n = 5
# edges = [[0,1,10], [0,2,3], [1,3,2], [2,1,4], [2,3,8], [2,4,2], [3,4,5]]
# src = 0
def shortestPath(n: int, edges: List[List[int]], src: int) -> Dict[int, int]:
    adj_dict = defaultdict(list)
    for s, d, w in edges:
        adj_dict[s].append([d, w])
        # adj_dict = {0: [[1,10], [2,3]], 1: [3,2]}

    pq = []
    heapq.heappush(pq, (0, src))  # (weight, src)
    shortest = {}

    while pq:
        current_weight, current_node = heapq.heappop(pq)  # (0, 0)
        if current_node in shortest:
            continue

        shortest[current_node] = current_weight
        # shortests: {0:0},

        for neighbor, weight in adj_dict[current_node]:  # [(1,10), (2,3)]
            if neighbor not in shortest:
                heapq.heappush(pq, (current_weight + weight, neighbor))

    return shortest
shortestPath(5, [[0,1,10], [0,2,3], [1,3,2], [2,1,4], [2,3,8], [2,4,2], [3,4,5]], 0)


# https://leetcode.com/problems/cheapest-flights-within-k-stops/
# n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1
def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    adj_dict = defaultdict(list)
    for s, d, p in flights:
        adj_dict[s].append([d, p])

    # adj_dict = {0: [1, 100], 1: [2, 100], 2: [0, 100], 1: [3, 600], 2: [3, 200]}

    # prices = {node: float('inf') for node in range(n)}
    # prices[src] = current_price
    prices = [float('inf')] * n
    prices[src] = 0
    # prices = {0: 0, 1: inf, 2: inf, 3: inf}

    # to process nodes level by level (by number of stops)
    dq = deque([(src, 0)]) # (node, cost)
    stops = 0

    while dq and stops <= k:
        # Process all nodes at current stop level
        size = len(dq)
        for _ in range(size):
            current_node, current_cost = dq.popleft()

            # Try all neighbors
            for neighbor, price in adj_dict[current_node]:
                new_cost = current_cost + price
                if new_cost < prices[neighbor]:
                    prices[neighbor] = new_cost
                    dq.append((neighbor, new_cost))

        stops += 1

    return prices[dst] if prices[dst] < float('inf') else -1
findCheapestPrice(4, [[0,1,200],[1,2,100],[1,3,300],[2,3,100]], 0, 3, 1)

"""
    Design
        - edges -> adj_dict
        - city_map = {city: [neighbors within weight less than or equal to distanceThreshold]}
        - return max(min(len(city_map.values())))
    Timeline
        - understanding the problem at 19:50
        - starting design at 20:05
"""
# https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/
# n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
def findTheCity(n: int, edges: List[List[int]], distanceThreshold: int) -> int:
    adj_dict = defaultdict(list)
    for s, d, w in edges:
        adj_dict[s].append((d, w))
        adj_dict[d].append((s, w))
        # adj_dict = {0: [(1,3)], 1: [(2,1), (3,4)], 2: [(3,1)]}

    # dq = deque()
    # print(next(iter(adj_dict)))
    # dq.append((next(iter(adj_dict)), 0))
    # city_map = {i: [] for i in range(n)}

    minimum_cities = n
    result_city = -1

    # try each city as a source
    for source in range(n):
        # use Dijkstra's to find the shortest paths
        distances = [float('inf')] * n
        distances[source] = 0
        pq = [(0, source)] # (distance, node)

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_dist > distances[current_node]:
                continue

            # process neighbors
            for neighbor, dist in adj_dict[current_node]:
                new_dist = current_dist + dist

                if new_dist <= distanceThreshold and new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        # count reachable cities
        # reachable = sum(1 for d in distances if d <= distanceThreshold) - 1
        reachable = 0
        for d in distances:
            if d <= distanceThreshold:
                reachable += 1
        reachable -= 1 # exclude the city itself

        if reachable < minimum_cities or (reachable == minimum_cities and source > result_city):
            minimum_cities = reachable
            result_city = source

    return result_city


findTheCity(4, [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], 4)