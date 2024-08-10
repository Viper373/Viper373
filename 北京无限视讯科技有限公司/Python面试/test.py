def addtest1(a: int, b: int):
    c = 5
    if a == b:
        return c
    elif a < b:
        return c - 3 * (b - a)
    else:
        return c + 3 * (a - b)


def addtest2(a: int, b: int):
    if (24 > a >= 0) and (60 > b >= 0):
        print(f"现在是{a}点{b}分")
        return 0
    else:
        print("this number max >= 0 && < 24")
        print("请重新输入")
        return -1
