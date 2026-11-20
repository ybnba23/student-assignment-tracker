from abc import ABC, abstractmethod


class ICRUD[T](ABC):
    @abstractmethod
    def list(self) -> list[T]: ...

    @abstractmethod
    def add(self, entity: T) -> None: ...

    @abstractmethod
    def replace(self, index: int, entity: T) -> bool: ...

    @abstractmethod
    def delete(self, index: int) -> bool: ...
