from __future__ import annotations
from typing import Callable
from PyQt5 import QtCore, QtSql, QtWidgets
from .sql_text_edit import SqlTextEdit

Qt = QtCore.Qt


class CustomTableView(QtWidgets.QTableView):
    def __init__(self, sql_text_edit: SqlTextEdit):
        super().__init__(
            sortingEnabled=True,
            selectionBehavior=QtWidgets.QTableView.SelectRows
            | QtWidgets.QTableView.SelectColumns,
            selectionMode=QtWidgets.QTableView.ContiguousSelection,
            alternatingRowColors=True,
            contextMenuPolicy=Qt.ActionsContextMenu,
            editTriggers=QtWidgets.QTableView.EditKeyPressed,
        )
        header = self.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        header.addAction(
            QtWidgets.QAction(
                "&Copy whole column", self, triggered=self._copy_columns
            )
        )
        self._sql_text_edit = sql_text_edit

    def _copy_columns(self):
        model = self.horizontalHeader().selectionModel()
        self.verticalHeader()
        col_idxs = [idx.column() for idx in model.selectedIndexes()]
        model = self.model()
        data = []
        # header_model = self.horizontalHeader().model()
        data.append(
            [model.headerData(col_idx, Qt.Horizontal) for col_idx in col_idxs]
        )
        for row in range(model.rowCount()):
            data.append(
                [str(model.index(row, col_idx).data()) for col_idx in col_idxs]
            )
        text = "\n".join("\t".join(row) for row in data)
        QtWidgets.QApplication.clipboard().setText(text)

    def selectionChanged(self, selected, deselected):
        tips: set[str] = set()
        for index in selected.indexes():
            val = index.data()
            try:
                if len(val) > 1:
                    tips.add(val)
            except TypeError:  # int
                pass
        self._sql_text_edit.setTips(tips)
        super().selectionChanged(selected, deselected)


class ReportWindow(QtWidgets.QSplitter):
    def __init__(
        self,
        title: str,
        report_to_db: Callable[[QtSql.QSqlDatabase], list[str]],
        view_ready: Callable[[CustomTableView], None],
    ):
        super().__init__(Qt.Vertical, windowTitle=title)
        self.setMinimumSize(1, 1)
        self._db_id = "db-" + str(id(self))
        self._db = self._create_db(self._db_id)
        keys = report_to_db(self._db)
        (
            where_widget,
            self._sql_text_edit,
            apply_button,
            self._error_label,
        ) = self._create_where_widget()
        self._sql_table_view = self._create_sql_table(self._db)
        view_ready(self._sql_table_view)
        self.addWidget(self._sql_table_view)
        self.addWidget(where_widget)
        self._sql_text_edit.setColumnNames(keys)
        self._sql_text_edit.apply.connect(self._apply)
        apply_button.clicked.connect(self._apply)
        self.setSizes([1000, 1])
        self._sql_table_view.resizeColumnsToContents()
        if self._sql_table_view.model().rowCount():
            self._sql_table_view.selectRow(0)

    def _apply(self):
        sql = self._sql_text_edit.toPlainText()
        sql_model = self._sql_table_view.model()
        sql_model.setFilter(sql)
        err = ""
        if sql_model.lastError().isValid():
            err = "SQL error: " + sql_model.lastError().databaseText()
            sql_model.select()
        self._error_label.setText(err)

    @staticmethod
    def _create_db(connection_name: str):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE", connection_name)
        db.setDatabaseName(":memory:")
        if not db.open():
            raise Exception("Can't open sqlite database in memory")
        return db

    def _create_sql_table(self, db: QtSql.QSqlDatabase):
        """
        Create table view
        """
        table_view = CustomTableView(self._sql_text_edit)
        sql_model = QtSql.QSqlTableModel(self, db)
        sql_model.setTable("report")
        sql_model.select()
        table_view.setModel(sql_model)
        return table_view

    @staticmethod
    def _create_where_widget():
        SP = QtWidgets.QSizePolicy
        sql_text_edit = SqlTextEdit()
        action_layout = QtWidgets.QHBoxLayout()
        error_label = QtWidgets.QLabel(styleSheet="QLabel{color:darkRed;}")
        error_label.setSizePolicy(SP.Expanding, SP.Preferred)
        apply_button = QtWidgets.QPushButton(
            "Apply", toolTip="Ctrl+Enter / Alt+Enter"
        )
        action_layout.addWidget(error_label)
        action_layout.addWidget(apply_button)

        where_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(where_widget)
        layout.addWidget(QtWidgets.QLabel("Where:"))
        layout.addWidget(sql_text_edit)
        layout.addLayout(action_layout)

        return where_widget, sql_text_edit, apply_button, error_label
