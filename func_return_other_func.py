"""
    函数可以做为另一个函数的返回值
"""

def fn():
    L = []
    while True:
        num = int(input("请输入一个正整数:"))
        if num < 0:
            break
        L.append(num)
    print(L)
    return L

print(max(fn()))
print(min(fn()))
print(len(fn()))