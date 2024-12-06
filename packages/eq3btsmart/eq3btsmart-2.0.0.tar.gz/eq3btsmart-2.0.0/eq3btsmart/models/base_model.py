from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from eq3btsmart.structures import Eq3Struct


@dataclass
class BaseModel[StructType: Eq3Struct](ABC):
    @classmethod
    @abstractmethod
    def from_struct(cls: type[Self], struct: StructType) -> Self:
        """Convert the structure to a model."""

    @classmethod
    @abstractmethod
    def struct_type(cls: type[Self]) -> type[StructType]:
        """Return the structure type associated with the model."""

    @classmethod
    def from_bytes(cls: type[Self], data: bytes) -> Self:
        """Convert the data to a model."""
        return cls.from_struct(cls.struct_type().from_bytes(data))
