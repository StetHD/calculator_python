from helpers import \
    is_math_operator, is_math_symbol, is_math_unary_operator, evaluate_math_exp, is_math_binary_operator


class Calculator:
    def __init__(self):
        self.__stack = []
        self.__operator = ""
        self.__prev = ""
        self.result = ""

    def __process_input(self, calc_input):
        if self.result == "Error":
            self.result = ""

        if not is_math_operator(calc_input) and (calc_input.isnumeric() or calc_input == ".") \
                and self.result.count(".") < 2:
            if is_math_operator(self.__prev) or self.__prev == "=":
                self.result = ""
                if self.__operator == "":
                    self.__stack = []
            self.result += calc_input
            self.__prev = calc_input
            return

        if not is_math_operator(self.__prev) and self.__prev != "=" and self.result != ""\
                and not is_math_symbol(self.__prev):
            self.__stack.append(self.result)

        if is_math_symbol(calc_input):
            try:
                self.result = str(evaluate_math_exp(calc_input))
                self.__stack.append(calc_input)
                self.__prev = calc_input
            except RuntimeError:
                self.result = "Error"
                self.__stack = []
                self.__operator = ""
                self.__prev = ""
            return

        if is_math_operator(calc_input) and len(self.__stack) > 0:
            if is_math_unary_operator(calc_input):
                try:
                    self.result = str(evaluate_math_exp(f"{calc_input}({self.__stack[-1]})"))
                    self.__stack[-1] = self.result
                    self.__prev = calc_input
                except RuntimeError:
                    self.result = "Error"
                    self.__stack = []
                    self.__operator = ""
                    self.__prev = ""
                return

            if is_math_binary_operator(calc_input):
                if len(self.__stack) == 1:
                    self.__operator = calc_input
                    self.__prev = calc_input
                    return

                if len(self.__stack) == 2:
                    try:
                        self.result = str(evaluate_math_exp(f"{self.__operator}({self.__stack[-2]}, {self.__stack[-1]})"))
                        self.__stack = []
                        self.__stack.append(self.result)
                        self.__operator = calc_input
                        self.__prev = calc_input
                    except RuntimeError:
                        self.result = "Error"
                        self.__stack = []
                        self.__operator = ""
                        self.__prev = ""
                    return

        if calc_input == "=" and len(self.__stack) == 2 and self.__operator != "":
            try:
                self.result = str(evaluate_math_exp(f"{self.__operator}({self.__stack[-2]}, {self.__stack[-1]})"))
                self.__stack = []
                self.__stack.append(self.result)
                self.__prev = calc_input
                self.__operator = ""
            except RuntimeError:
                self.result = "Error"
                self.__stack = []
                self.__operator = ""
                self.__prev = ""
            return

    def insert(self, calc_input: str):

        if calc_input == "C":
            self.result = ""
            self.__operator = ""
        if calc_input == "AC":
            self.__stack = []
            self.__operator = ""
        self.__process_input(calc_input)
