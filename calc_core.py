import math
from helpers import math_funcs_param_inspector

UNWANTED_PROPS = ["__name__", "__doc__", "__package__", "__loader__", "__spec__", "__file__"]


class Calculator:
    def __init__(self):
        self.history = []
        self.stack = []
        self.current = "0.0"
        self.methods = {name: (val, math_funcs_param_inspector(name)) for name, val in math.__dict__.items() if
                        callable(val)}
        self.__math_symbols = {name: val for name, val in math.__dict__.items() if not callable(val)
                               and name not in UNWANTED_PROPS}

    def insert(self, calc_input: str):
        try:
            self.history.append(float(calc_input))
            self.stack.append(float(calc_input))
        except ValueError:
            pass


def eval_math(input_string: str):
    allowed_names = {name: val for name, val in math.__dict__.items() if name not in UNWANTED_PROPS}
    allowed_names.update({"abs": abs, "divmod": divmod, "max": max, "min": min, "pow": pow, "round": round, "sum": sum})
    code = compile(input_string, "<string>", "eval")
    return eval(code, {"__builtins__": {}}, allowed_names)


print(float(eval_math("prod([1, 3, 5 ])")))
print(float(eval_math("sum([1, 3, 5 ])")))
print(float(eval_math("sum((1, 3, 5, 10))")))
print(float(eval_math("log(e)")))
print(float(eval_math("log(10, 10)")))
print(float(eval_math("log10(10)")))
print(float(eval_math("12112.1212+1212")))
print([name for name, val in math.__dict__.items() if name not in UNWANTED_PROPS])