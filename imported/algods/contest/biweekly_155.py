from typing import List


def findCommonResponse(responses: List[List[str]]) -> str:
    sets_array = []

    for res in responses:
        hash_set = set()
        for i in res:
            hash_set.add(i)

        sets_array.append(hash_set)

    res_map = {}
    for arr in sets_array:
        for s in arr:
            if s in res_map:
                res_map[s] += 1
            else:
                res_map[s] = 1

    if res_map:
        max_count = max(res_map.values())
        max_keys = [k for k, v in res_map.items() if v == max_count]
        res = min(max_keys)  # lexicographically smallest among most common
    else:
        res = ""
    return res

# res = findCommonResponse([["good","ok","good","ok"],["ok","bad","good","ok","ok"],["good"],["bad"]])
res = findCommonResponse([["good","ok","good"],["ok","bad"],["bad","notsure"],["great","good"]])
print(res)