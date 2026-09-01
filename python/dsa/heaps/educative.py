import heapq


def find_right_interval(intervals):
    starts, ends = [], []
    n = len(intervals)
    for i in range(n):
        # i[0] = start
        heapq.heappush(starts, (intervals[i][0], i))
        # i[1] = end
        heapq.heappush(ends, (intervals[i][1], i))

    result = [-1 for _ in range(n)]
    while ends:
        end, end_index = heapq.heappop(ends)

        popped_starts = []
        while starts:
            start, index = heapq.heappop(starts)
            if end <= start:
                result[end_index] = index
                heapq.heappush(starts, (start, index))
                break
            else:
                popped_starts.append((start, index))

        for ps in popped_starts:
            heapq.heappush(starts, (ps[0], ps[1]))

    return result
find_right_interval([[1,12],[2,9],[3,10],[13,14],[15,16],[16,17]])


def longest_diverse_string(a, b, c):
    heap = []
    heapq.heappush(heap, (-a, 'a'))
    heapq.heappush(heap, (-b, 'b'))
    heapq.heappush(heap, (-c, 'c'))

    res = ""
    while heap:
        count, char = heapq.heappop(heap)
        if count == 0:
            continue

        while len(res) >= 2 and char == res[-1] == res[-2] and heap:
            next_count, next_char = heapq.heappop(heap)
            if next_count == 0:
                break

            res += next_char
            heapq.heappush(heap, (next_count + 1, next_char))

        res += char
        heapq.heappush(heap, (count + 1, char))

    return res

longest_diverse_string(1, 1, 7)


def max_average_ratio(classes, extraStudents):
    pq = []
    n = len(classes)

    for i in range(n):
        curr_pass, curr_total = classes[i]
        potential_gain = ((curr_pass + 1) / (curr_total + 1) - (curr_pass / curr_total))
        heapq.heappush(pq, (-potential_gain, curr_pass, curr_total, i))

    for i in range(extraStudents):
        potential_gain, curr_pass, curr_total, index = heapq.heappop(pq)

        curr_pass += 1
        curr_total += 1
        potential_gain = ((curr_pass + 1) / (curr_total + 1) - (curr_pass / curr_total))

        heapq.heappush(pq, (-potential_gain, curr_pass, curr_total, index))

    total_pass_ratio = 0
    while pq:
        pass_ratio, curr_pass, curr_total, index = heapq.heappop(pq)
        total_pass_ratio += (curr_pass / curr_total)

    avg_pass_ratio = total_pass_ratio / n
    return avg_pass_ratio
max_average_ratio([[1,2],[3,5],[2,2]], 2)