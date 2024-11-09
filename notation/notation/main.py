class PrefixToInfix:
    def __init__(self, ):
        self._pref = ""
        self._op1 = None
        self._op2 = None

    def convert(self, s: str):
        s = s.split()
        self._pref = s
        result = []
        for token in self._pref[::-1]:
            if token.isdigit():
                result.append(token)
            elif token in ["+", "-", "*", "/"]:
                if len(result) < 2:
                    return "Not enough operands for operator"
                self._op1 = result.pop()
                self._op2 = result.pop()
                result.append(f"({self._op1} {token} {self._op2})")
        if len(result) != 1:
            return "Incorrect number of operands or operators"
        return result.pop()
