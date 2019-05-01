from functools import lru_cache


@lru_cache()
def solve(t, s):
    if t == 2:
        if s < 1:
            return 0
        if s > 1:
            return 1
        if s == 1:
            return 0.45

    return max(
        0.45 * solve(t+1, s+1) + 0.55 * solve(t+1, s),
        0.9 * solve(t+1, s+0.5) + 0.1 * solve(t+1, s)
    )

print(solve(0, 0))
