from typing import Any

from .converter import Converter
from .converter_config import ALL, ConverterConfig

__all__ = ["IdentityConverter", "primitive_data_types"]

primitive_data_types = [
    "int",
    "float",
    "string",
    "bool",
]


class IdentityConverter(Converter):
    def _convert(self, input: Any, context: dict) -> Any:
        return input

    config = ConverterConfig(
        data_types=primitive_data_types,
        output_formats=ALL,
    )
