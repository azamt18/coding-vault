from typing import List


def intervalIntersection(firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
    i, j = 0, 0
    res = []
    prev_target = 2
    target, comparable = None, None

    while i < len(firstList) and j < len(secondList):
        interval_a = firstList[i]
        interval_b = secondList[j]

        if max(interval_a[0], interval_b[0]) <= min(interval_a[1], interval_b[1]): # overlap
            overlapping_interval = [max(interval_a[0], interval_b[0]), min(interval_a[1], interval_b[1])]
            res.append(overlapping_interval)

        # adjust pointer
        if interval_a[1] <= interval_b[1]:
            i += 1
        else:
            j += 1

        # if prev_target == 2:
        #
        #     target = firstList[i]  # first list item
        #     comparable = secondList[j]  # second list item
        #     prev_target = 1
        #
        #     j = j + 1
        #
        # elif prev_target == 1:
        #
        #     target = secondList[j]  # second list item
        #     comparable = firstList[i]  # first list item
        #     prev_target = 2
        #
        #     i = i + 1
        #
        # if target[1] >= comparable[0]:  # if overlap exists with second list item
        #     overlapping_interval = [max(target[0], comparable[0]), min(target[1], comparable[1])]
        #     res.append(overlapping_interval)
        # else:
        #     res.append(target)
        #     res.append(comparable)

    return res

intervalIntersection([[0,2],[5,10],[13,23],[24,25]], [[1,5],[8,12],[15,24],[25,26]])


def countDays(days: int, meetings: List[List[int]]) -> int:
    if len(meetings) <= 1:
        return 0

    sorted_data = sorted(meetings, key=lambda x: x[0])
    # [[1,3], [5,7], [9,10]]

    # [[1,3], [2,4]] -> [[1,4]]
    final_data = [sorted_data[0]]
    print(final_data)
    for i in range(1, len(sorted_data)):
        # overlap condition
        # start = max(final_data[-1][0], sorted_data[i][0])
        # end = min(final_data[-1][1], sorted_data[i][1])
        print(final_data[-1])
        print(sorted_data[i])

        is_overlap = final_data[-1][1] >= sorted_data[i][0]

        if is_overlap:
            final_data[-1] = [min(final_data[-1][0], sorted_data[i][0]), max(final_data[-1][1], sorted_data[i][1])]
        else:
            final_data.append(sorted_data[i])

    count = 0
    prev_start, prev_end = final_data[0]
    for i in range(1, len(final_data)):
        current_start, current_end = final_data[i]

        available_days = (current_start - prev_end) - 1
        if available_days >= 1:
            count += available_days
        prev_start, prev_end = current_start, current_end

    # checking the last days
    if days - final_data[-1][1] >= 1:
        count += days - final_data[-1][1]

    return count
countDays(10, [[5,7],[1,3],[9,10]])