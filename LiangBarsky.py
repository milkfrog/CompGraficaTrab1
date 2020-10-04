from sympy import Matrix

def clipLine(clipWindow, line):

    print("Will clip: " + str(line))
    print("With clipping window: " + str(clipWindow))

    p = [-(line[1, 0] - line[0, 0]),
           line[1, 0] - line[0, 0],
         -(line[1, 1] - line[0, 1]),
           line[1, 1] - line[0, 1]]

    q = [line[0, 0] - clipWindow[0, 0],
         clipWindow[1, 0] - line[0, 0],
         line[0, 1] - clipWindow[1, 1],
         clipWindow[1, 1] - line[0, 1]]

    t = {}
    t2 = 1
    t1 = 0

    count_parallel = 0

    print("p:")
    print(p)
    print("q:")
    print(q)

    for i in range(0, 4):
        if p[i] > 0:
            t[i] = q[i] / p[i]
            t2 = min(t2, t[i])
        elif p[i] < 0:
            t[i] = q[i] / p[i]
            t1 = max(t1, t[i])
        elif q[i] < 0:
            print("Line outside the clipping window.")
            return None
        else:
            print("Line parallel to clipping window.")
            count_parallel += 1

    if t1 ==0 and t2 == 0:
        print("Line totally inside the clipping window.")
        return line
    elif t1 < t2:
        print("Line clipped.")
        return Matrix([[line[0, 0] + t1 * p[1], line[0, 1] + t1 * p[3]],
                       [line[0, 0] + t2 * p[1], line[0, 1] + t2 * p[3]]])
    else:
        print("Idk why things got this far...")
        return None