"""
check for one-to-one key-value existence --> if pattern exists

given: s1, s2
output: true/false

examples:
    1. func("aca", "zwz") -> true
    2. func("llm", "ptp") -> false

constraints:
    * 0 <= s1.length, s2.length <= 10^5
    * s1[i], s2[i] are lowercase English letters

assumptions:
    * is their length equal? => yes, strings should be the same length for a perfect one-to-one mapping
    * is it a one-way pattern (from s1 to s2) or two-way (from s2 to s1)? => it is exactly one-to-one matching

"""
""" appr 1: building hashmap and check if there is a match/mismatch according to previous data 
    init assumption:
        tc: (alphabet size)
            * there are at most 26 English letters which are keys of the hashmap
        sc: (alphabet size) saying that there 26 English letters, so it is ~(26)
    better:
        tc: (N) N = entire length of input strings
        sc: (K) K = number of unique characters across both strings, in the worst case K is the size of character set (26 for lowercase English letters, or up to 256 for ASCII) 
"""
def pattern_exists_not_one_to_one(s1: str, s2: str) -> bool:
    # edge cases
    if not s1 and not s2:
        return True
    if not s1 or not s2:
        return False

    pattern_storage = {}
    for c1, c2 in zip(s1, s2):
        if c1 not in pattern_storage:
            pattern_storage[c1] = c2
            continue

        if pattern_storage[c1] != c2:
            return False

    return True

def one_to_one_match(s1: str, s2: str) -> bool:
    # edge cases
    if not s1 and not s2:
        return True
    if not s1 or not s2:
        return False
    if len(s1) != len(s2):
        return False

    first_to_second = {}
    second_to_first = {}
    for c1, c2 in zip(s1, s2):

        # a   c   a
        # c1
        # z   w   z
        # c2
        # {a:z, c:w}
        # {z:a, w:c}

        # check mapping from s1 to s2
        if c1 in first_to_second:
            if not first_to_second[c1] == c2:
                return False
        else:
            first_to_second[c1] = c2

        # check mapping from s2 to s1
        if c2 in second_to_first:
            if not second_to_first[c2] == c1:
                return False
        else:
            second_to_first[c2] = c1

        # a   b
        # c1
        # c   c
        # c2
        # {a: c, b:c}
        # {c: a, c:b}

        # one-to-one mapping validation

        # if c1 not in first_to_second:
        #     if c2 in second_to_first: # key already set to another key
        #         return False
        #     first_to_second[c1] = c2
        #
        # if c2 not in second_to_first:
        #     if c1 in first_to_second:
        #         return False
        #     second_to_first[c2] = c1

    return True

def one_to_one_match(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    map1_to_2 = {}
    map2_to_1 = {}
    
    for c1, c2 in zip(s1, s2):
        # check mapping from s1 to s2
        if c1 in map1_to_2:
            if map1_to_2[c1] != c2:
                return False
        else:
            map1_to_2[c1] = c2
        # check mapping from s2 to s1
        if c2 in map2_to_1:
            if map2_to_1[c2] != c1:
                return False
        else:
            map2_to_1[c2] = c1
    return True

def one_to_one_match(s1: str, s2: str) -> bool:
    if not s1 and not s2:
        return True
    if s1 and not s2:
        return False
    if not s1 and not s2:
        return False

    first_to_second = {}
    second_to_first = {}

    for char1, char2 in zip(first_to_second, second_to_first):
        # mapping from s1 to s2
        if char1 in first_to_second:
            if first_to_second[char1] != char2:
                return False
        else:
            first_to_second[char1] = char2


""" test cases """
assert one_to_one_match("aca", "zwz") == True
assert one_to_one_match("lln", "ptp") == False
assert one_to_one_match("", "") == True
assert one_to_one_match("a", "b") == True
assert one_to_one_match("ab", "bc") == True
assert one_to_one_match("ab", "cc") == False
assert one_to_one_match("ab", "bb") == False
assert one_to_one_match("abc", "dee") == False
assert one_to_one_match("abce", "bcd") == False
print("All test cases passed")