from collections import defaultdict
from typing import List


def group_anagrams(strs: List[str]) -> List[List[str]]:
    hashtable = defaultdict(list)
    for word in strs:
        count = [0] * 26
        for char in word:
            count[ord("z") - ord(char)] += 1
        hashtable[tuple(count)].append(word)
    return list(hashtable.values())


def test_group_anagrams_standard():
    input_data = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = group_anagrams(input_data)
    assert len(result) == 3


def test_group_anagrams_empty():
    assert group_anagrams([""]) == [[""]]
