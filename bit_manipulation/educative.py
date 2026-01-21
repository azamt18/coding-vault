from typing import List


def bitwiseComplement(self, n: int) -> int:
    # bitwise, tc: (logn), sc: (logn)
    binary = bin(n)[2:] # remove '0b'
    arr = list(binary)
    for i in range(len(arr)):
        if arr[i] == '0':
            arr[i] = '1'
        else:
            arr[i] = '0'
    return int(''.join(arr), 2)

    # binary = bin(n) # '0b1010'
    # arr = binary[2:] # ['1010']
    # for i in range(len(arr)):
    #     el = arr[i]
    #     if el == '0':
    #         el = 0 ^ int(el)
    #     else:
    #         el = 1 ^ int(el)
    #     arr[i] = el
    # print(arr)
    # return int(''.join(arr), 2)

    # if n == 0:
    #     return 1
    #
    # bit_count = n.bit_length()
    # all_bits_set = (1 << bit_count) - 1
    # return n ^ all_bits_set


def flip_and_invert_image(image):
    # naive sln, tc: (mxn) for reverse + (mxn) for invert, sc: (1)
    # rows, cols = len(image), len(image[0])
    # for row in range(rows):
    #     image[row].reverse()
    # for row in range(rows):
    #     for col in range(cols):
    #         if image[row][col] == 0:
    #             image[row][col] = 1
    #         else:
    #             image[row][col] = 0
    # return image

    # xor with middle, tc: (mxn/2), sc: (1)
    # rows, cols = len(image), len(image[0])
    # for row in range(rows):
    #     mid = (cols + 1) // 2
    #     for col in range(mid):
    #         left = image[row][col] ^ 1
    #         right = image[row][cols-col-1] ^ 1
    #         image[row][col] = right
    #         image[row][cols-col-1] = left
    # return image

    # 1-x approach, tc: (mxn), sc: (n) for list comprehension of size n for each row
    for row in image:
        row[:] = [1 - x for x in reversed(row)]
    return image

""" https://leetcode.com/problems/single-number-iii/ """
def singleNumber(self, nums: List[int]) -> List[int]:
    bitwise_xor = 0
    for n in nums:
        bitwise_xor = bitwise_xor ^ n

    bitwise_mask = bitwise_xor & -bitwise_xor
    result = 0
    for n in nums:
        if n & bitwise_mask:
            result = result ^ n

    return [result, bitwise_xor ^ result]
