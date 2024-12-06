import math


def int_ceil(num: float) -> int:
    """
    >>> int_ceil(10 / 3)
    4

    :param num:
    :return:
    """
    return math.ceil(num)


def decimal_ceil(num: float, places: int = 2) -> float:
    """
    >>> decimal_ceil(3.14159)
    3.15

    :param num:
    :param places:
    :return:
    """
    if places >= 0:
        scale = 10.0 ** places
        return math.ceil(num * scale) / scale
    else:
        raise ValueError(f"places：{places} 必须大于等于 0 ！")
