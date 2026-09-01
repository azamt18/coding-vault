from leetcode import strStr

cases = [
    ("hello", "ll", 2),
    ("aaaa", "aaa", 0),
    ("", "", 0),
    ("", "a", -1),
    ("abc", "c", 2),
    ("abc", "d", -1),
    ("short", "longerneedle", -1),
    ("mississippi", "issip", 4),
]

all_ok = True
for h, n, expected in cases:
    res = strStr(None, h, n)
    ok = res == expected
    print(f"haystack={h!r}, needle={n!r} => got={res}, expected={expected}, {'OK' if ok else 'FAIL'}")
    if not ok:
        all_ok = False

if not all_ok:
    raise SystemExit(1)
print('\nAll tests passed')

