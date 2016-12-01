fs = []
for k in range(10):
    def f(x, k=k):
        x += k
        return x
    fs.append(f)

for f in fs:
    print f(0)

def plus(x, y):
    return x + y

def plusone(x):
    return plus(1, x)

