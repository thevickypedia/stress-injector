import numpy

result = [numpy.random.bytes(1024 * 1024) for _ in range(1024)]

print(len(result))
