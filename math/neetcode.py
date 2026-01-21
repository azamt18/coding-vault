def myPow(x: float, n: int) -> float:
    c = 1 + 2
    x_n = 1
    is_negative_degree = n < 0
    degree = n

    if is_negative_degree:
        degree = n * (-1)

    for _ in range(degree):
        x_n = x_n * x

    if is_negative_degree:
        x_n = 1 / x_n

    return x_n
myPow(2, -3)