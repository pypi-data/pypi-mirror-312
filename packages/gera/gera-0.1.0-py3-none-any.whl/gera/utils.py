from __future__ import annotations
from PyQt5.QtGui import QIcon


def get_icon(name: str):
    return get_icon.__dict__.get(name) or _create_icon(name)


def _create_icon(name: str):
    icon = QIcon("gera:/%s.svg" % name)
    get_icon.__dict__[name] = icon
    return icon
