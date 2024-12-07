from __future__ import annotations
from PyQt5 import QtCore, QtGui, QtWidgets
from .mdi_area import MdiArea
from .utils import get_icon
from .schemas import iter_schemas, load_schema_cls

Qt = QtCore.Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, schema: str, files: list[str]):
        # enable `get_icon`
        QtCore.QDir.addSearchPath(
            "gera",
            QtCore.QFileInfo(f"{__file__}/../resources").absoluteFilePath(),
        )
        super().__init__(
            windowTitle="GERA - General ERror Analyzer",
            windowIcon=get_icon("gera"),
        )
        self._setup_ui()
        self._load_settings()
        if schema == "ldj":
            for path in files:
                cls = load_schema_cls("ldj")
                report_window = cls().open_filename(path)
                if report_window:
                    self._mdi_area.add(report_window, True)

    def _setup_ui(self):
        self.resize(1000, 770)
        self.setStyleSheet(
            """QMainWindow::separator, QSplitter::handle {
                background:rgba(0,0,0,50);
                width:4px;
                height:4px;
            } """
        )
        # main_splitter splits left_frame and mdi_area
        menu_button = self._create_menu_button()
        self._mdi_area = MdiArea(self, menu_button)
        self._mdi_area.subWindowActivated.connect(self._sub_window_changed)

        self.setCentralWidget(self._mdi_area)

    def _create_menu_button(self):
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        menu_button = QtWidgets.QPushButton(
            maximumSize=QtCore.QSize(24, 24),
            icon=get_icon("menu"),
            flat=True,
            sizePolicy=size_policy,
            shortcut="Alt+M",
        )
        menu = QtWidgets.QMenu()
        self._open_actions = []
        for name, title in iter_schemas():
            open_act = QtWidgets.QAction(
                get_icon("open"),
                "&Open - " + title,
                self,
                triggered=self._on_open,
            )
            open_act.setData(name)
            self._open_actions.append(open_act)
        menu.addActions(self._open_actions)
        menu_button.setMenu(menu)
        return menu_button

    def _on_open(self):
        self._default_open = module_name = self.sender().data()
        for act in self._open_actions:
            act.setShortcut(
                "Ctrl+O" if act is self.sender() else QtGui.QKeySequence()
            )
        cls = load_schema_cls(module_name)
        settings = self.get_settings()
        try:
            report_window = cls().open(self, settings)
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Error opening a file:\n\n"
                + repr(e)
                + "\n\nprobably invalid file",
            )
            import traceback

            traceback.print_exception(e)
            return
        if report_window is not None:
            self._mdi_area.add(report_window, True)

    def _sub_window_changed(self, window):
        if window is not None:
            try:
                on_activate = window.widget().on_activate
            except AttributeError:
                return
            on_activate()

    def _load_settings(self):
        settings = self.get_settings()
        default = QtCore.QByteArray()
        self.restoreGeometry(settings.value("geometry", default))
        self.restoreState(settings.value("windowState", default))
        self._default_open = settings.value("default_open", "")
        for act in self._open_actions:
            if act.data() == self._default_open:
                act.setShortcut(Qt.CTRL + Qt.Key_O)

    def closeEvent(self, event: QtGui.QCloseEvent):
        """User closes GERA. By default, the event is accepted."""
        self._mdi_area.closeAllSubWindows()
        if self._mdi_area.subWindowList():
            event.ignore()
        else:
            self._save_settings()

    def _save_settings(self):
        """Called from closeEvent."""
        settings = self.get_settings()

        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("default_open", self._default_open)

    @staticmethod
    def get_settings():
        return QtCore.QSettings("iitpvisionlab", "GERA")
