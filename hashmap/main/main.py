import re


class ConditionError(Exception):
    pass


class SpecialDict:
    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    @property
    def iloc(self):
        class IlocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, index):
                if not isinstance(index, int) or index < 0:
                    raise IndexError("Index должен быть неотрицательным целым числом.")
                sorted_keys = sorted(self.parent._data.keys(), key=str)
                if index >= len(sorted_keys):
                    raise IndexError("Индекс выходит за границы.")
                return self.parent._data[sorted_keys[index]]

        return IlocAccessor(self)

    @property
    def ploc(self):
        class PlocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, condition):
                parsed_conditions = self._parse_conditions(condition)
                filtered = {}
                for key, value in self.parent._data.items():
                    numeric_key = self._parse_key(key)
                    if numeric_key and len(numeric_key) == len(parsed_conditions):
                        if self._evaluate_conditions(numeric_key, parsed_conditions):
                            filtered[key] = value
                return filtered

            @staticmethod
            def _parse_conditions(condition):
                condition = re.sub(r"[^\d<>=., ]", "", condition)
                conditions = re.split(r",\s*", condition)
                parsed = []
                for cond in conditions:
                    match = re.fullmatch(r"([<>]=?|=|<>)(-?\d+(?:\.\d+)?)", cond)
                    if not match:
                        raise ConditionError(f"Неверное условие: {cond}")
                    operator, number = match.groups()
                    parsed.append((operator, float(number)))
                return parsed

            @staticmethod
            def _parse_key(key):
                if not re.fullmatch(r"[0-9.,\s-]+", key.replace("(", "").replace(")", "")):
                    return None
                try:
                    key = re.sub(r"[^\d.,-]", "", key)
                    return [float(x) for x in key.split(",")]
                except ValueError:
                    return None

            @staticmethod
            def _evaluate_conditions(key, conditions):
                for value, (operator, number) in zip(key, conditions):
                    if operator == "=" and value != number:
                        return False
                    elif operator == "<>" and value == number:
                        return False
                    elif operator == "<" and value >= number:
                        return False
                    elif operator == "<=" and value > number:
                        return False
                    elif operator == ">" and value <= number:
                        return False
                    elif operator == ">=" and value < number:
                        return False
                return True

        return PlocAccessor(self)
