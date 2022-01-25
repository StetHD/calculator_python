import math
from inspect import signature


def math_funcs_param_inspector(func_name: str):

    if func_name in ("log", "perm"):
        return [i for i in range(1, 3)]

    if func_name in ("hypot", "prod"):
        return math.inf

    try:
        sig = signature(math.__dict__[func_name])
        params = sig.parameters
        params_len = len(params)

        return [i for i in range(params_len, params_len + 1)]
    except ValueError:
        return None
