# encoding: utf-8
from __future__ import annotations
from typing import Any, Iterator, Iterable, TypedDict, Literal
import os
from . import GeraSchema
from ..report_window import CustomTableView
from PyQt5 import QtCore, QtWidgets, QtSql
from ..dbutils import create_table_statement, batch, SEP
import json
import string
from collections import ChainMap

Qt = QtCore.Qt


Type = type[int | float | str]


def dict_to_keys(
    d: dict[str, Any], up: tuple[str, ...] = ()
) -> Iterator[tuple[tuple[str, ...], Type]]:
    for key, value in d.items():
        tuple_key = up + (key,)
        if isinstance(value, dict):
            yield from dict_to_keys(value, tuple_key)
        else:
            yield tuple_key, type(value)


class GeraActionBase(TypedDict):
    # first action is always activated on doubleclick
    name: str


class GeraCopyAction(GeraActionBase):
    action: Literal["copy"]
    text: str


class GeraExecuteAction(GeraActionBase):
    action: Literal["execute"]
    args: list[str]


GeraActions = list[GeraCopyAction | GeraExecuteAction]


class LDJSchema(GeraSchema):
    _gera_info: GeraActions | None

    def open(self, main_window: QtWidgets.QWidget, settings: QtCore.QSettings):
        key = self.__class__.__name__ + "_last_opened_path"
        last_opened_path = settings.value(key, "")
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            main_window,
            "Open LDJ Report",
            last_opened_path,
            "LDJ Report (*.ldj);;All files (*.*)",
        )
        if file_name:
            settings.setValue(key, file_name)
            return self.open_filename(file_name)

    def open_filename(self, path: str):
        from ..report_window import ReportWindow

        report_window = ReportWindow(
            path,
            lambda db: self._report_to_db(db, path),
            self.on_view_ready,
        )
        return report_window

    def _gera_info_to_actions(
        self,
        info: GeraActions,
        view: CustomTableView,
    ) -> list[QtWidgets.QAction]:
        ret: list[QtWidgets.QAction] = []
        for command in info:
            match command["action"]:
                case "copy":
                    text = command["text"]
                    triggered = lambda *_, text=text: self._on_copy_action(
                        view, text
                    )
                    ret.append(
                        QtWidgets.QAction(
                            f"Copy {command['name']}",
                            view,
                            triggered=triggered,
                        )
                    )
                case "execute":
                    args = command["args"]
                    triggered = lambda *_, args=args: self._on_execute_action(
                        view, args
                    )
                    ret.append(
                        QtWidgets.QAction(
                            f"Execute {command['name']}",
                            view,
                            triggered=triggered,
                        )
                    )
            if command is info[0]:
                view.activated.connect(triggered)
        return ret

    def _cur_row_as_dict(self, view: CustomTableView) -> None | dict[str, Any]:
        model = view.model()
        index = view.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        return {
            model.headerData(col_idx, Qt.Horizontal): model.index(
                row, col_idx
            ).data()
            for col_idx in range(model.columnCount())
        }

    def _on_copy_action(self, view: CustomTableView, text: str) -> None:
        data = self._cur_row_as_dict(view)
        if data is not None:
            vformat = string.Formatter().vformat
            QtWidgets.QApplication.clipboard().setText(
                vformat(text, None, ChainMap(data, os.environ))
            )

    def _on_execute_action(
        self, view: CustomTableView, args: list[str]
    ) -> None:
        data = self._cur_row_as_dict(view)
        if data is not None:
            vformat = string.Formatter().vformat
            args = [
                vformat(arg, None, ChainMap(data, os.environ)) for arg in args
            ]
            print("executing", " ".join(args))
            process = QtCore.QProcess()
            process.setProgram(args[0])
            process.setArguments(args[1:])
            if not process.startDetached():
                QtWidgets.QMessageBox.warning(
                    view, "gera", f"failed to run\n{args}"
                )

    def _iter_report(
        self, report: Iterable[dict[str, Any]], rows: list[tuple[str, ...]]
    ) -> Iterator[list[Any]]:
        for data in report:
            ret: list[Any] = []
            for row in rows:
                value = data
                for key in row:
                    value = value.get(key)
                if not isinstance(value, (float | int | str)):
                    value = repr(value)
                ret.append(value)
            yield ret

    @staticmethod
    def get_columns_and_types(lines: Iterable[dict[str, Any]]):
        all_keys: set[tuple[str, ...]] = set()
        all_types: dict[tuple[str, ...], set[Type]] = {}

        for datum in lines:
            for key, type in dict_to_keys(datum):
                all_keys.add(key)
                if key in all_types:
                    all_types[key].add(type)
                else:
                    all_types[key] = {type}

        all_keys_sorted = sorted(all_keys)

        def best_type(types: set[Type]) -> Type:
            if float in types:
                return float
            if int in types:
                return int
            return str

        best_types = [best_type(all_types[key]) for key in all_keys_sorted]
        all_keys_str = [SEP.join(path) for path in all_keys_sorted]
        return all_keys_sorted, all_keys_str, best_types

    def _report_to_db(self, db: QtSql.QSqlDatabase, report_filename: str):
        data: list[dict[str, Any]] = []
        with open(report_filename, "rb") as f:
            for line in f:
                data.append(json.loads(line))
        if data and "_gera_" in data[0]:
            self._gera_info = data[0].pop("_gera_")
        else:
            self._gera_info = None

        all_keys, all_keys_str, best_types = self.get_columns_and_types(data)

        row = dict(zip(all_keys_str, best_types))
        statement = create_table_statement(row, column_order=all_keys_str)
        QtSql.QSqlQuery(statement, db)
        assert db.tables() == ["report"], db.tables()

        q = QtSql.QSqlQuery(db)
        sql = "INSERT INTO report VALUES ({})".format(
            ",".join("?" * len(all_keys_str))
        )
        q.prepare(sql)

        for seq in batch(self._iter_report(data, all_keys)):
            values: list[list[Any]] = [[] for _ in all_keys_str]
            for entry in seq:
                for val, l in zip(entry, values):
                    l.append(val)

            for pos, value in enumerate(values):
                q.bindValue(pos, value)
            if not q.execBatch():
                print("execBatch:", q.lastError().text())

        q = QtSql.QSqlQuery("SELECT COUNT(*) CNT FROM report", db)
        q.first()
        print("inserted", q.value(0))
        return all_keys_str

    def on_view_ready(self, view: CustomTableView):
        if self._gera_info:
            view.addActions(self._gera_info_to_actions(self._gera_info, view))
