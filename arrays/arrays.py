from typing import List


def replaceElements(arr: List[int]) -> List[int]:
    max_el = -1
    # max_el = max(6, 18)
    #  18   6   6    6   1   -1
    # [17,  18, 5,  4,  6,  1]
    for i in range(len(arr) - 1, -1, -1):
        if i == len(arr) - 1:
            arr[i] = max_el
        else:
            max_el = max(max_el, arr[i + 1])
            arr[i] = max_el
    return arr

res = replaceElements([17,18,5,4,6,1])
print(res)