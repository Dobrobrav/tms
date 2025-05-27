from abc import ABC, abstractmethod

from tasks.domain.aggregate_root import AggregateRoot


class Repository(ABC):
    @abstractmethod
    def get(self) -> AggregateRoot:
        ...

    @abstractmethod
    def set(self, entity: AggregateRoot) -> None:
        ...
