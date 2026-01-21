from collections import Counter


def removeDuplicates(s: str, k: int) -> str:
    counter = Counter(s)

    def contains_duplicates(counter, k):
        result = []
        for letter, count in counter.items():
            if count >= k:
                result.append(letter)
        return result

    while True:
        duplicate_letters = contains_duplicates(counter, k)
        if not duplicate_letters:
            break

        for key in duplicate_letters:
            del counter[key]

    final_str_arr = []
    for letter, count in counter.items():
        final_str_arr.append(letter * count)

    return ''.join(final_str_arr)


removeDuplicates("pbbcggttciiippooaais", 2)