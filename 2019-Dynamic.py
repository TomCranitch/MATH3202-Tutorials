E = [0, 14, 8, 17, 22, 12, 6]  # The 0th week is included so that E[t] corresponds to the expected sales in week t


# Stages            t           Weeks
# State             b           Number of books at the start of week t
# Value Function    V1_t(b)     Expected profit for weeks t through 6 if week t starts with b books
#                               Need to find V1_1(0) (That is the expected profit of weeks 1 through 6 if we start with no books)
def V1(t, b):
    if t == 6:
        return b, ("End",)

    return max(
        (
            12*min(E[t], b+10*a) - 50*a - 0.5*max(0, b + 10*a - E[t]) + V1(t+1, max(0, b + 10*a - E[t]))[0],
            (a,) + V1(t+1, max(0, b + 10*a - E[t]))[1]
        )
        for a in range(4)
    )


sol = V1(1, 0)

print("\n\n\033[1m Solution Prepared for 2019 MATH3202 Practical Exam Question 2(a). Minimum combined assignment and build cost is $" + str(sol[0]) + "\033[0m.\n")

print("The optimal solution is given by making the following purchases", ', '.join(map(str, [a for a in sol[1] if a != 'End'])))


# Stages            t           Weeks
# State             b, m        Number of books at the start of week t (given by b) and m=1 if a movie announcement is made on or before week t
# Value Function    V2_t(b, m)  Expected profit for weeks t through 6 if week t starts with b books and if the movie announcment is made on or before week t
#                               Need to find V2_1(0, 0) (That is the expected profit of weeks 1 through 6 if we start with no books and no announcment has been made)
# Note that the function returns a tuple containing the the expected profit for the remaining weeks as the first element
#   and another tuple as the second element which contains the buying pattern if no movie is ever announced or
#   the optimal buying pattern if a movie is announced on or before the current week (the buying pattern is no longer stocastic once the movie is announced)
def V2(t, b, m):
    if t == 6:
        return b, ('End',)

    if m == 1:
        return max(
            (
                12*min(2*E[t], b+10*a) - 50*a - 0.5*max(0, b + 10*a - 2*E[t]) + V2(t+1, max(0, b + 10*a - 2*E[t]), 1)[0],
                (a,) + V2(t+1, max(0, b + 10*a - 2*E[t], 1), 1)[1]
            )
            for a in range(4)
        )

    return max(
        (
            0.7 * (12*min(E[t], b+10*a) - 50*a - 0.5*max(0, b + 10*a - E[t]) + V2(t+1, max(0, b + 10*a - E[t]), 0)[0]) +
            0.3 * (12*min(2*E[t], b+10*a) - 50*a - 0.5*max(0, b + 10*a - 2*E[t]) + V2(t+1, max(0, b + 10*a - 2*E[t]), 1)[0]),
            (a,) + V2(t+1, max(0, b + 10*a - E[t]), 0)[1]
        )
        for a in range(4)
    )


sol = V2(1, 0, 0)

print("\n\n\033[1m Solution Prepared for 2019 MATH3202 Practical Exam Question 2(b). Minimum combined assignment and build cost is $" + str(sol)[0] + "\033[0m.\n")

print("The optimal solution if no movie is ever announced is given by making the following purchases", ', '.join(map(str, [a for a in sol[1] if a != 'End'])) + str(". Note that the optimal buying pattern for week 1 will remain the same irrespective of when (or if) the movie is announced."))
