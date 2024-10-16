def fib(n):
    if n <= 2:
        return 1

    a, b, c = 1, 1, 2

    for _ in range(3, n + 1):
        a, b, c = b, c, b + c  # 更新变量
    return c

print(fib(100))
