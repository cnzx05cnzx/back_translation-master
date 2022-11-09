import random

x = [i for i in range(10)]
print(x)
def fun(x):
    random.shuffle(x)
    print(x)

fun(x)
fun(x)
