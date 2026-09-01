def strStr(self, haystack: str, needle: str) -> int:
    # approach 1: string function, tc: (n1 * n2), sc: (1)
    # if needle not in haystack:
    #     return -1
    # return haystack.index(needle)

    # approach 2: naive approach of sliding window
    # window, needle as a window, haystack is to iterate with a window size of needle
    # the problem is about smaller window is inside a large window
    # tc: (n * m), sc: (n)
    # window1, window2 = haystack, needle
    # window_size = len(window2)
    # begin, end = 0, 0
    # for i in range(len(window1)):
    #     if window1[i : i+window_size] == window2:
    #         return i
    # return -1

    """ this didn't work
            while end < len(window1):

                found = False
                # for i in range(window_size): <- replace by while window1[end] == window2[i] and i < window_size
                i = 0
                # while i < window_size and window1[end] == window2[i]: <- replace by false condition
                if window1[end] == window2[i]:
                    begin = end
                    while i < window_size and window1[end] == window2[i]:
                        end += 1
                        i += 1
                if  window1[end] == window2[i]:

                # while window1[end] != window2[i]:
                #     begin += 1

                # if end - begin == window_size:
                #     found = True
                # if found:
                #     begin = end - window_size
                #     return begin
                end += 1

            return -1
            """

    s1, s2 = haystack, needle

    # Add edge case for empty needle
    if not s2:
        return 0

    # false positive
    # aaaa
    # aaa
    if len(s1) < len(s2):
        return -1

    # top     1234567
    # bottom    345
    top, bottom = 0, 0
    idx = -1
    while top < len(s1):
        if s1[top] != s2[bottom]:
            top += 1
            continue
        else:
            #     t
            # leetcode
            #     b
            # leeto
            idx = top
            while top < len(s1) and bottom < len(s2) and s1[top] == s2[bottom]:
                top += 1
                bottom += 1

            if bottom == len(s2):
                # completed
                return idx
            # reset - fix the bug here
            top = idx + 1  # Move to next position after the start of failed match
            bottom = 0
            idx = -1
    return idx
