from typing import Dict, List # this adds type hints for List and Dict

def get_dict_keys(age_dict: Dict[str, int]) -> List[str]:

    result = []

    for key in age_dict:        
        result.add(key)

    return result

def get_dict_values(age_dict: Dict[str, int]) -> List[int]:
    result = []
    for key, value in age_dict:
        result.add(value)
    return result

# do not modify below this line
dict_1 = {"John": 25, "Doe": 30, "Jane": 22}
dict_2 = {"NeetCode": 24, "NeetCode2": 25, "NeetCode3": 26}

print(get_dict_keys(dict_1))
print(get_dict_keys(dict_2))

print(get_dict_values(dict_1))
print(get_dict_values(dict_2))


from typing import Dict # this adds type hinting for Dict

def count_characters(word: str) -> Dict[str, int]:
    # result = {}
    # for char in word:
    #     if char in result:
    #         result[char] += 1
    #     else:
    #         result[char] = 1
    # return result
    # alternative using dict.get()
    result = {}
    for char in word:
        result[char] = result.get(char, 0) + 1
    return result




# don't modify below this line
print(count_characters("hello"))
print(count_characters("world"))
print(count_characters("hello world"))
print(count_characters("this is a longer sentence"))
