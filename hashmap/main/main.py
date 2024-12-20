import re
from typing import Any, Dict, List, Tuple


class InvalidConditionException(Exception):
    pass


class SpecialDict(dict):
    @property
    def iloc(self):
        class IlocHandler:
            def __init__(self, parent: "SpecialDict"):
                self.parent = parent

            def __getitem__(self, index: int) -> Any:
                sorted_keys = sorted(self.parent.keys())
                if index < 0 or index >= len(sorted_keys):
                    raise IndexError("Index out of range.")
                return self.parent[sorted_keys[index]]

        return IlocHandler(self)

    @property
    def ploc(self):
        class PlocHandler:
            def __init__(self, parent: "SpecialDict"):
                self.parent = parent

            def __getitem__(self, condition: str) -> Dict[str, Any]:
                conditions = self._parse_conditions(condition)
                result = {
                    key: value
                    for key, value in self.parent.items()
                    if (key_values := self._extract_numeric_values(key))
                    and self._validate_conditions(key_values, conditions)
                }
                return result

            def _extract_numeric_values(self, key: str) -> List[float]:
                if re.search(r'[a-zA-Z]', key):
                    return []
                clean_key = re.sub(r'[^\d.,-]', '', key)
                return [float(num) for num in clean_key.split(',') if num]

            def _parse_conditions(self, condition: str) -> List[Tuple[str, float]]:
                parsed_conditions = []
                for cond in condition.replace(" ", "").split(","):
                    match = re.match(r"([<>]=?|==|<>)(-?\d+(\.\d+)?)", cond)
                    if not match:
                        raise InvalidConditionException(f"Invalid condition: {cond}")
                    parsed_conditions.append((match.group(1), float(match.group(2))))
                return parsed_conditions

            def _validate_conditions(self, key_values: List[float], conditions: List[Tuple[str, float]]) -> bool:
                if len(key_values) != len(conditions):
                    return False

                operator_funcs = {
                    ">": lambda x, y: x > y,
                    ">=": lambda x, y: x >= y,
                    "<": lambda x, y: x < y,
                    "<=": lambda x, y: x <= y,
                    "==": lambda x, y: x == y,
                    "<>": lambda x, y: x != y,
                }

                return all(
                    operator_funcs[op](key_val, limit)
                    for key_val, (op, limit) in zip(key_values, conditions)
                )

        return PlocHandler(self)
