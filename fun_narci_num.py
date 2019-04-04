'''
    算出100~999之间的水仙花数(Narcissistic number)
    水仙花数是指百位的3次方 加上 十位的3次方 加上 个位的3次方等于原数的整数
'''

def is_narci_num(n):
    if (n // 100) ** 3 + ((n % 100) // 10 ) ** 3 + ((n % 10) ** 3) == n:
        return True
    return False

def count_narci_num():
    L = []
    for n in range(100,1000):
        if is_narci_num(n):
            print(n)
            L.append(n)
    return len(L)

count_num = count_narci_num()
print("100-999的水仙花数为:",count_num,"个")

