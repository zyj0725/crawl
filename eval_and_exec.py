"""
    eval(experssion,globals,locals)和exec()
"""

s = 1
g = {"x":2,"y":3}
l = {"x":4,"y":5}
print(eval('s+2'))
print(eval('x+y',g))
print(eval('x+y',g,l))
print(eval('s+x',None,l))
# print(eval('s+x',g,None))     #报错
print(eval('h+x',g,{"h":6}))

x = 1
y = 1
num1 = eval("x+y")
print(num1)

def g():
    x = 2
    y = 2
    num3 = eval("x+y")
    print(num3)
    num2 = eval("x+y", globals())
    num2 = eval("x+y",globals(),locals())
    print(num2)

g()

