from abc import ABC, abstractmethod

from tasks.domain.aggregate_root import AggregateRoot


class Repository(ABC):
    @abstractmethod
    def get(self, entity_id: int) -> AggregateRoot:
        ...

    @abstractmethod
    def set(self, entity: AggregateRoot) -> None:
        ...
