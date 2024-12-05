from typing import Generic, Iterator

from colt import Registrable

from .types import T_Example


class DataSource(Generic[T_Example], Registrable):
    def load(self) -> Iterator[T_Example]:
        raise NotImplementedError


class DataSink(Generic[T_Example], Registrable):
    def save(self, data: Iterator[T_Example]) -> None:
        raise NotImplementedError
