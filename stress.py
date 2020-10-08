import math
import resource

import numpy

result = [numpy.random.bytes(1024 * 1024) for _ in range(1024)]

print(len(result))


def size_converter(byte_size):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(math.floor(math.log(byte_size, 1024)))
    power = math.pow(1024, integer)
    size = round(byte_size / power, 2)
    response = str(size) + ' ' + size_name[integer]
    return response


print(size_converter(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
