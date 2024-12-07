from __future__ import annotations
from typing import Iterator, TYPE_CHECKING
from importlib import import_module

if TYPE_CHECKING:
    from ..report_window import ReportWindow
    from QtWidgets import QWidget
    from QtCore import QSettings


class GeraSchema:
    def open(
        self, main_window: QWidget, settings: QSettings
    ) -> None | QWidget:
        raise NotImplementedError

    def open_filename(self, path: str) -> ReportWindow:
        raise NotImplementedError


def load_schema_cls(mod_name: str) -> type[GeraSchema]:
    mod_path = "." + mod_name
    mod = import_module(mod_path, package="gera.schemas")
    for obj in vars(mod).values():
        if (
            isinstance(obj, type)
            and issubclass(obj, GeraSchema)
            and obj is not GeraSchema
        ):
            return obj
    raise ValueError("Could not find schema class in {}".format(mod_path))


def iter_schemas() -> Iterator[tuple[str, str]]:
    from PyQt5.QtCore import QDir

    qdir = QDir(__file__)
    qdir.cdUp()
    dir_filter = qdir.Dirs | qdir.Files | qdir.NoDotAndDotDot
    for fi in qdir.entryInfoList(dir_filter, qdir.Name):
        if fi.baseName()[:2] == "__":
            continue
        if fi.suffix() == "py" or fi.isDir():
            name = fi.baseName()
            yield name, name.replace("_", " ").title()
