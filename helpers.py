import math
from inspect import signature
import screeninfo

UNWANTED_PROPS = ["__name__", "__doc__", "__package__", "__loader__", "__spec__", "__file__"]
MATH_SYMBOLS_OPERATORS = [name for name, val in math.__dict__.items() if name not in UNWANTED_PROPS]

builtin_math_functions = {"abs": abs, "divmod": divmod, "max": max, "min": min, "pow": pow, "round": round, "sum": sum}
BUILTIN_MATH_OPERATIONS = [name for name in builtin_math_functions]

custom_math_functions = {
    "add": lambda a, b: a + b,
    "minus": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "fdiv": lambda a, b: a / b,
    "div": lambda a, b: a // b,
    "neg": lambda a: -a,
    "ln": lambda a: math.log(a, math.e),
    "mod": lambda a, b: a % b
}
CUSTOM_MATH_OPERATORS = [name for name in custom_math_functions.keys()]

MATH_ENV_ITEMS = [*MATH_SYMBOLS_OPERATORS, *BUILTIN_MATH_OPERATIONS, *CUSTOM_MATH_OPERATORS]


def math_funcs_param_inspector(func):
    if func.__name__ in ("log", "perm", "gcd", "lcm", "pow"):
        return 2

    if func.__name__ in ("hypot", "prod"):
        return math.inf

    try:
        sig = signature(func)
        params = sig.parameters
        params_len = len(params)

        return params_len
    except ValueError:
        return None


def math_symbols():
    return {name: math.__dict__[name] for name in MATH_SYMBOLS_OPERATORS if not callable(math.__dict__[name])}


def math_operators():
    return {**{name: math.__dict__[name] for name in MATH_SYMBOLS_OPERATORS if callable(math.__dict__[name])},
            **builtin_math_functions, **custom_math_functions}


def is_math_symbol(value):
    return math_symbols().get(value) is not None


def is_math_operator(value):
    return math_operators().get(value) is not None


def is_math_unary_operator(value):
    func = math_operators().get(value)
    return func is not None and math_funcs_param_inspector(func) == 1


def is_math_binary_operator(value):
    func = math_operators().get(value)
    return func is not None and math_funcs_param_inspector(func) == 2


def geometry_string(width, height):
    monitor = screeninfo.get_monitors()[0]
    x_offset = (monitor.width - width) // 2
    y_offset = (monitor.height - height) // 2
    return f"{width}x{height}+{x_offset}+{y_offset}"


def is_float(str_num):
    try:
        float(str_num)
        return True
    except ValueError:
        return False


def is_zero(str_num):
    return is_float(str_num) and float(str_num) == 0


def evaluate_math_exp(value):
    allowed_names = {**math_operators(), **math_symbols()}
    code = compile(value, "<string>", "eval")
    try:
        return eval(code, {"__builtins__": {}}, allowed_names)
    except (TypeError, SyntaxError, ZeroDivisionError, ValueError, NameError, RuntimeError):
        raise RuntimeError

