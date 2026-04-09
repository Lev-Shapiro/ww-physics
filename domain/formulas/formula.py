from abc import ABC, abstractmethod
import typing as t

class Formula(ABC):
    @staticmethod
    @abstractmethod
    def calculate(*args: t.Any, **kwargs: t.Any):
        raise NotImplementedError("Subclasses must implement this method")