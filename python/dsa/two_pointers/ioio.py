def backspaceCompare(s: str, t: str) -> bool:
    n = len(s) - 1
    m = len(t) - 1
    skip_s = 0
    skip_t = 0

    #             *
    # x y w r r m p
    #                 *
    # x y w r r m u # p
    while n >= 0 and m >= 0:
        while n >= 0:
            if s[n] == '#':
                skip_s += 1
                n -= 1
            elif skip_s > 0:
                skip_s -= 1
                n -= 1
            else:
                break

        while m >= 0:
            if t[m] == '#':
                skip_t += 1
                m -= 1
            elif skip_t > 0:
                skip_t -= 1
                m -= 1
            else:
                break

        if n >= 0 and m >= 0 and s[n] != t[m]:
            return False

        if (n >= 0) != (m >= 0):
            return False

        n -= 1
        m -= 1

    return n == m
backspaceCompare("ab##", "c#d#")