from typing import List


def asteroidCollision(self, asteroids: List[int]) -> List[int]:
    # 2 4 -4 -1

    # stack

    # -4 vs 4 -> 0

    # -1 vs 2 -> 2
    # 2

    # 7 -3 9

    # -3 vs 7 -> 7
    # 7

    # 9
    # 7

    stack = []

    for ast in asteroids:
        while stack and (stack[-1] > 0 > ast):  # important! not (stack[-1] < 0 and ast > 0)
            # collision
            abs_top = abs(stack[-1])
            abs_ast = abs(ast)

            if abs_top == abs_ast:
                stack.pop()
                break

            elif abs_top > abs_ast:
                break

            elif abs_top < abs_ast:
                stack.pop()
        else:
            stack.append(ast)

            # if stack[-1] == ast:
            #     stack.append(ast)
            #     break
            #
            # if abs(stack[-1]) == abs(ast):
            #     stack.pop()
            #     break
            #
            # if stack[-1] > 0 and ast > 0:
            #     stack.append(ast)
            #     break
            # if stack[-1] < 0 and ast < 0:
            #     stack.append(ast)
            #     break
            #
            # if abs(stack[-1]) > abs(ast):
            #     # 4 vs -2
            #     continue
            # if abs(stack[-1]) < abs(ast):
            #     # 2 vs -4
            #     stack.pop()
            #     stack.append(ast)
            #     break

    return stack

