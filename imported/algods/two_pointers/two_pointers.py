# zryxeededexyz
#   l        r
def validPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    deleted_at_most_once = False
    while left < right:
        if s[left] != s[right]:
            # check the flag
            if deleted_at_most_once:
                return False

            # check next chars
            if s[left + 1] == s[right]:
                left += 1
                deleted_at_most_once = True
                continue
            if s[left] == s[right - 1]:
                right -= 1
                deleted_at_most_once = True
                continue

            return False

        left += 1
        right -= 1

    return True
