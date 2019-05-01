from functools import lru_cache

probs = [
    [0.20, 0.25, 0.10],
    [0.30, 0.30, 0.30],
    [0.35, 0.33, 0.40],
    [0.38, 0.35, 0.45],
    [0.40, 0.38, 0.50]
]


@lru_cache(maxsize=2**13)
def solve(t, s):
    if t == 3:
        return 1, 0

    return min(((1 - probs[t][a]) * solve(t+1, s-a)[0], a) for a in range(s+1))

print(solve((0, 0), 4))


# TODO make this run
