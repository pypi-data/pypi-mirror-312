from __future__ import annotations
from argparse import Namespace, ArgumentParser
import sys


def application():
    from PyQt5.QtWidgets import QApplication

    a = QApplication(sys.argv)

    try:
        from gera.main_window import MainWindow

        main_window = MainWindow(**vars(parse_args()))
    except Exception:
        import traceback

        traceback.print_exc(file=sys.stdout)
        print("press <Enter> to exit")
        input()
        return (None, None)

    main_window.show()
    return a, main_window


def main():
    a, _main_window = application()
    sys.exit(a and a.exec_())


def parse_args() -> Namespace:
    parser = ArgumentParser("GERA runner")

    parser.add_argument("files", nargs="*", help="files to open")
    parser.add_argument(
        "--schema",
        choices=["ldj"],
    )

    return parser.parse_args()
