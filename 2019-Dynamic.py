E = [0, 14, 8, 17, 22, 12, 6]  # The 0th week is included so that E[t] corresponds to the expected sales in week t


def V1(t, b):
    if t == 6:
        return b

    return max(
        12*min(E[t], b+10*a) - 50*a - 0.5*max(0, b + 10*a - E[t]) + V1(t+1, max(0, b + 10*a - E[t]))
        for a in range(4)
    )


print(V1(1, 0))
