from functools import lru_cache


@lru_cache(maxsize=None)
def sol(C, P):
    if C == 1:
        return max(
            (P*3, 1),
            (P*5 + (1-P), 0)
        )

    return max(
        ((P * 3) + sol(C - 1, min(P + 0.1, 1))[0], 1),
        ((P * 5) + (1 - P) + sol(C - 1, max(P - 0.2, 0))[0], 0)
    )


print(sol(10, 0.6))
print(sol(9, 0.7))
print(sol(8, 0.8))
print(sol(7, 0.9))
print(sol(6, 1))
print(sol(5, 0.8))
print(sol(4, 0.9))
print(sol(3, 1))
print(sol(2, 0.8))
print(sol(1, 0.6))
