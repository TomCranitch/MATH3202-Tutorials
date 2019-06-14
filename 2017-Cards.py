
def V(C, rem):

    unfilled = min(C)
    if unfilled != -1:
        return (10 *C[0] + C[1]) * (10 *C[2] + C[3])

    expected = 0

    for r in rem:
        best = 10000
        move = -1

        for c in C:
            if C[c] == -1:

                a = C
                a.insert(c+1, r)
                a.pop(c)

                result = V(a, [i for i in rem if i != r])

                if result < best:
                    best = result
                    move = c

        expected += (1/len(rem)) * best

    return expected


print(V([-1, -1, -1, -1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
