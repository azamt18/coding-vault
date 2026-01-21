# https://leetcode.com/problems/repeated-dna-sequences/
import heapq


def findRepeatedDnaSequences(s):
    # encode sequence
    to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    encoded_sequence = [to_int[c] for c in s]
    n = len(encoded_sequence)

    # compute polynomial hash
    k = 10  # dna sequence length
    a = 4  # unique elements

    if n <= k:
        return []

    h = 0
    a_k = 1  # a^k for hash updates

    seen_hashes, output = set(), set()

    # compute initial hash
    for i in range(k):
        h = h * a + encoded_sequence[i]
        a_k = a_k * a

    seen_hashes.add(h)

    # sliding window
    for start in range(1, n - k + 1):
        # for start in range(k, len(encoded_sequence) - 1):
        # new_hash = (old_hash x 4) - (leftmost digit x 4^10) + new_digit
        h = (h * a) - (encoded_sequence[start - 1] * a_k) + (encoded_sequence[start + k - 1])

        if h in seen_hashes:
            output.add(s[start: start + k])
        else:
            seen_hashes.add(h)

    return list(output)
findRepeatedDnaSequences("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")

# https://leetcode.com/problems/sliding-window-maximum/description/
def find_max_sliding_window(nums, w):
    window, output = [], []
    heap = []

    for i in range(w):
        window.append(nums[i])
        heapq.heappush(heap, -nums[i])

    output.append(heap[0])

    for i in range(w, len(nums)):
        window.append(nums[i])
        window.pop(0)

        # how to update deque after removing oldest element

        output.append(-heap[0])

    return output

# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
def find_longest_substring(input_str):
    last_seen_at = {}
    window_start, window_end = 0, 0
    max_length = 0

    while window_end < len(input_str):
        if input_str[window_end] not in last_seen_at:
            last_seen_at[input_str[window_end]] = window_end
        else:
            if last_seen_at[input_str[window_end]] >= window_start:
                # max_length = max(max_length, window_end - window_start + 1)
                window_start = last_seen_at[input_str[window_end]] + 1
            last_seen_at[input_str[window_end]] = window_end

        max_length = max(max_length, window_end - window_start + 1)
        window_end += 1

    return max_length


def min_sub_array_len(target, nums):
    window_start, window_end = 0, 0
    curr_sum = 0
    min_length = float("inf")

    while window_end < len(nums):
        curr_sum += nums[window_end]
        # if curr_sum >= target:
        while curr_sum >= target:
            min_length = min(min_length, window_end - window_start + 1)
            curr_sum -= nums[window_start]
            window_start += 1

        window_end += 1

    return min_length if min_length < float("inf") else 0