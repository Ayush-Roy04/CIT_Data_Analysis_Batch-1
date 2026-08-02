def num(a,b,c):
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c
print(num(5, 10, 3))
print(num(80, 30, 11))