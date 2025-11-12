import importlib
import pkgutil
from pathlib import Path

from src.library_catalog.infrastructure.persistence.models.base import BaseModel, TimestampModel, UUIDModel

_package_path = Path(__file__).parent
_package_name = __name__

for _importer, _modname, _ispkg in pkgutil.iter_modules([str(_package_path)]):
    if not _ispkg and _modname != "base":
        importlib.import_module(f"{_package_name}.{_modname}")

__all__ = [
    "BaseModel",
    "TimestampModel",
    "UUIDModel",
]
