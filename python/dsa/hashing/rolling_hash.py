def rolling_hash(s, window_size):
    if len(s) < window_size:
        return None

    base = 256 # using ASCII values
    mod = 10**7 + 7

    # calc init hash value
    hash_value = 0
    for i in range(window_size):
        hash_value = (hash_value * base + ord(s[i])) % mod

    yield hash_value

    # calc hash val for subsequent windows
    for i in range(window_size, len(s)):
        # remove the contribution of outgoing char
        hash_value = (hash_value - ord(s[i - window_size]) * pow(base, window_size - 1, mod)) % mod

        # add the contribution of incoming char
        hash_value = (hash_value * base + ord(s[i])) % mod

        yield hash_value
    return None


s = "abcdefghijklmnop"
window_size = 3

for hash_val in rolling_hash(s, window_size):
    print(hash_val)