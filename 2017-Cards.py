def V(c1, c2, c3, c4, drawn, rem):

    unfilled = sum(c for c in [c1, c2, c3, c4] if c == -1)
    if unfilled == 1:
        return (10*c1 + c2) * (10*c3 + c4)

    return max(
        (1/len(rem)) * V(c1, c2, c3, c4, rem.remove(c))
        for c in rem
    )
