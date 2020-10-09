import platform


def stress():
    """Generates random bytes with the multiple of 1024 (~1GB)"""
    import numpy
    from tqdm import tqdm
    result = [numpy.random.bytes(1024 * 1024) for _ in tqdm(range(1024), desc='Generating random bytes', unit=' bytes',
                                                            leave=False)]
    return f'Injected stress in bytes: {(len(result)* 1024 * 1024)}'


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

    operating_system = platform.system()

    if operating_system == 'Darwin':
        import resource
        memory_utilized = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    elif operating_system == 'Windows':
        import psutil
        import os
        process = psutil.Process(os.getpid())
        memory_utilized = process.memory_info().peak_wset
    else:
        memory_utilized = None
    print(f'Actual memory consumed: {size_converter(memory_utilized)}')
