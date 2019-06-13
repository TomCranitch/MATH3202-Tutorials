from functools import lru_cache

x = [155, 120, 140, 100, 155]


@lru_cache(maxsize=None)
def V(t, s):
    if t == 5:
        return 0, 0

    return min(
        (200*(abs(a)**2) + 2000*max(s+a-x[t], 0) + V(t+1, s+a)[0], a)
        for a in range(x[t] - s, 56)
    )


prev_result = 155
for i in range(0, 5):
    print(V(i, prev_result))
    prev_result += V(i, prev_result)[1]

