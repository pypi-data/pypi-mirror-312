from typing import Generic, TypeVar

T = TypeVar("T")


class Line(Generic[T]):
    number: int
    value: T

    def __init__(self, value: T, number: int):
        self.number = number
        self.value = value
