import math
from inspect import signature
import screeninfo


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


def geometry_string(width, height):
    monitor = screeninfo.get_monitors()[0]
    x_offset = (monitor.width - width) // 2
    y_offset = (monitor.height - height) // 2
    return f"{width}x{height}+{x_offset}+{y_offset}"
