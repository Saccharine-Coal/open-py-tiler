from core.math import points

def add(tuple_1: tuple, tuple_2: tuple) -> tuple:
    return tuple(a + b for a, b in zip(tuple_1, tuple_2))

def mult(tuple_1, factor) -> tuple:
    return tuple(val * factor for val in tuple_1)

def operation_conditions_met(tuple_1: tuple, tuple_2: tuple) -> bool:
    conditions_met = isinstance(tuple_1, tuple) and isinstance(tuple_2, tuple)
    conditions_met = conditions_met and (len(tuple_1) == len(tuple_2))
    return conditions_met
