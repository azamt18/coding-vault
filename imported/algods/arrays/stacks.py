def isValid(s: str) -> bool:
    stack = []
    map = {'(': ')', '{': '}', '[': ']'}
    # map = {')':'(','}':'{',']':'['}

    # ([])
    for c in s:
        if c in map: # if it is an opening bracket
            stack.append(c)  # insert map keys:    (, {, [
        else: # if it is a closing bracket
            if not stack:
                return False

            opening_bracket = stack.pop()
            if c != map[opening_bracket]:
                return False

    return not stack

res = isValid("()[]{}")
print(res)