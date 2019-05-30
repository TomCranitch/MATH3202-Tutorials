from functools import lru_cache


@lru_cache(maxsize=99999999999)
def Vi(t, i, m):
    p = i-int(i)
    return p*V(t, int(i) + 1, m)[0] + (1-p)*V(t, int(i), m)[0]


@lru_cache(maxsize=99999999999999999)
def V(t, i, m):
    if i <= 0:
        return 0, 'Dead'
    if m == 1 and t == 150:
        return 2, 'Mate'
    if t == 150:
        return 1, 'Alone'

    if t >= 75:
        return Vi(t+1, i-3.6, m), 'Rest'

    return max(
        (Vi(t+1, i-3.6, m), 'Rest'),
        # Foraging
        (0.6 * (
            0.25 * Vi(t+1, i+32 - (8 - 0.007*i - 6.4), m) +
            0.50 * Vi(t+1, i+32 - (8 - 0.007*i - 0.0), m) +
            0.25 * Vi(t+1, i+32 - (8 - 0.007*i + 6.4), m)
        ) +
        0.4 * (
            0.25 * Vi(t+1, i - (8 - 0.007*i - 6.4), m) +
            0.50 * Vi(t+1, i - (8 - 0.007*i - 0.0), m) +
            0.25 * Vi(t+1, i - (8 - 0.007*i + 6.4), m)
        ), 'Forage'),
        # Singing
        (0.004 * (
            0.25 * Vi(t+1, i - (12 + 0.002*i - 6.4), 1) +
            0.50 * Vi(t+1, i - (12 + 0.002*i - 0.0), 1) +
            0.25 * Vi(t+1, i - (12 + 0.002*i + 6.4), 1)
        ) + 
        0.996 * (
            0.25 * Vi(t+1, i - (12 + 0.002*i - 6.4), m) +
            0.50 * Vi(t+1, i - (12 + 0.002*i - 0.0), m) +
            0.25 * Vi(t+1, i - (12 + 0.002*i + 6.4), m)
        ), 'Singing')
    )


# print(V(0, 50, 0))
print([V(i, 50, 0) for i in range(150)])
