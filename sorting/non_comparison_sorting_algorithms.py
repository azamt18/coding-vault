

def counting_sort(arr):
    M, N = max(arr), len(arr)
    # 1. init aux array
    aux = [0] * (M + 1)
    # 2. store frequency
    for num in arr:
        aux[num] += 1
    # 3. calc prefix sum
    for i in range(1, len(aux)):
        aux[i] += aux[i - 1]
    # 4. create sorted arr
    sorted_arr = [0] * N
    # 5. traverse from right to left and update
    for num in reversed(arr): # range(N - 1, -1, -1):
        sorted_arr[aux[num] - 1] = num
        aux[num] -= 1

    return sorted_arr
res = counting_sort([3, -1])
print(res)