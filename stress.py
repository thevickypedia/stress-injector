import resource


def stress():
    """Generates random bytes with the multiple of 1024 (~1GB)"""
    import numpy
    result = [numpy.random.bytes(1024 * 1024) for _ in range(1024)]
    return f'Injected stress in bytes: {len(result)}'


def size_converter(byte_size):
    """Converts bytes into appropriate readable size"""
    import math
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    integer = int(math.floor(math.log(byte_size, 1024)))
    power = math.pow(1024, integer)
    size = round(byte_size / power, 2)
    response = str(size) + ' ' + size_name[integer]
    return response


if __name__ == '__main__':
    print(stress())
    memory_utilized = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f'Actual memory consumed: {size_converter(memory_utilized)}')
