from enum import Enum


class MultiEnum(Enum):

  def __new__(cls, *values):
    obj = object.__new__(cls)
    obj._value_ = values[0]
    for other_value in values[1:]:
      cls._value2member_map_[other_value] = obj

    obj._all_values = values
    return obj

  def __repr__(self):
    return f"{self.__class__.__name__}.{self._name_}: {', '.join([str(v) for v in self._all_values])}"


class DType(MultiEnum):
  A = "a", 9
  B = "b", 10
