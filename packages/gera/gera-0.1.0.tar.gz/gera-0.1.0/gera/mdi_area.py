from __future__ import annotations
from PyQt5 import QtCore, QtGui, QtWidgets
from .utils import get_icon

Qt = QtCore.Qt


class TabRenamer(QtCore.QObject):
    def eventFilter(self, tab_bar, event):
        if (
            event.type() == event.MouseButtonDblClick
            and event.button() == QtCore.Qt.LeftButton
        ):
            tab_idx = tab_bar.tabAt(event.pos())
            if tab_idx >= 0:
                text, ok = QtWidgets.QInputDialog.getText(
                    tab_bar,
                    "Tab Name",
                    "?",
                    QtWidgets.QLineEdit.Normal,
                    tab_bar.tabText(tab_idx),
                )
                if ok and text:
                    tab_bar.setTabText(tab_idx, text)
            return True
        return False


def action_for(self, **mod):
    def action(text, *args, **kwargs):
        if args:
            kwargs["triggered"] = args[0]
        kwargs.update(mod)
        return QtWidgets.QAction(self.tr(text), self, **kwargs)

    return action


class MdiArea(QtWidgets.QMdiArea):
    def __init__(self, parent, button):
        super(MdiArea, self).__init__(
            parent,
            objectName="mdi_area",
            viewMode=QtWidgets.QMdiArea.TabbedView,
        )
        self._button = button
        button.setParent(self)

        # Setting elide mode
        self._tab_bar = tab_bar = self.findChild(QtWidgets.QTabBar)
        tab_bar.setElideMode(Qt.ElideMiddle)
        tab_bar.setMovable(True)
        tab_bar.setTabsClosable(True)
        tab_bar.currentChanged.connect(self._add_button_space)
        tab_bar.tabCloseRequested.connect(self._add_button_space)
        self.subWindowActivated.connect(self._add_button_space)
        self._renamer = TabRenamer()
        tab_bar.installEventFilter(self._renamer)

        # Actions
        action = action_for(self)
        close_all_act = action("Close &All", self.closeAllSubWindows)

        close_others_act = action("Close &Others", self.close_others)

        self.fullscreen_act = action(
            "&Fullscreen",
            icon=get_icon("fullscreen"),
            checkable=True,
            toggled=self.fullscreen,
            shortcut="Ctrl+F11",
        )

        tile_act = action("&Tile", self.tileSubWindows, icon=get_icon("tile"))

        tile_vert_act = action(
            "&Tile Vertical",
            self.tile_vertical,
            icon=get_icon("tile_v"),
            shortcut="Ctrl+Alt+Left",
        )

        tile_horz_act = action(
            "&Tile Horizontal",
            self.tile_horizontal,
            icon=get_icon("tile_h"),
            shortcut="Ctrl+Alt+Up",
        )

        tile_vert_rev_act = action(
            "&Tile Vertical Reverse",
            self.tile_vertical_rev,
            icon=get_icon("tile_v"),
            shortcut="Ctrl+Alt+Right",
        )

        tile_horz_rev_act = action(
            "&Tile Horizontal Reverse",
            self.tile_horizontal_rev,
            icon=get_icon("tile_h"),
            shortcut="Ctrl+Alt+Down",
        )

        cascade_act = action(
            "&Cascade", self.cascadeSubWindows, icon=get_icon("cascade")
        )

        next_act = action(
            "Ne&xt",
            self.activateNextSubWindow,
            shortcut=QtGui.QKeySequence.NextChild,
            icon=get_icon("next"),
        )

        previous_act = action(
            "Pre&vious",
            self.activatePreviousSubWindow,
            shortcut=QtGui.QKeySequence.PreviousChild,
            icon=get_icon("prev"),
        )

        separator_act = QtWidgets.QAction(self)
        separator_act.setSeparator(True)
        self.menu_actions = [
            close_all_act,
            close_others_act,
            self.fullscreen_act,
            separator_act,
            tile_act,
            tile_vert_act,
            tile_horz_act,
            tile_vert_rev_act,
            tile_horz_rev_act,
            cascade_act,
            separator_act,
            next_act,
            previous_act,
        ]
        self.addActions(self.menu_actions)  # so shortcuts work
        self._add_button_space()

    def _add_button_space(self):
        geometry = self._tab_bar.geometry()
        if geometry.x() == 0:
            btn_geometry = self._button.geometry()
            x = btn_geometry.width()
            geometry.setX(x)
            self._tab_bar.setGeometry(geometry)
            if geometry.height() == 0:
                self.setViewportMargins(0, btn_geometry.height(), 0, 0)

    def close_others(self):
        w = self.currentSubWindow()
        for window in self.subWindowList():
            if window is not w:
                window.close()

    def fullscreen(self, state):
        if state:  # go fullscreen
            self.splitter = self.parent()
            self._splitter_state = self.splitter.saveState()
            self.setParent(self.splitter.parent())
            self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
            self.showFullScreen()
        else:
            self.setParent(self.splitter)
            self.splitter.restoreState(self._splitter_state)
            self.splitter = None
            self.showNormal()

    def add(self, window, new=False, icon=None):
        if (
            not new
            and QtWidgets.QApplication.keyboardModifiers() != Qt.AltModifier
            and self.activeSubWindow() is not None
        ):
            self.closeActiveSubWindow()
        window.setAttribute(Qt.WA_DeleteOnClose)
        sub_window = self.addSubWindow(window)
        sub_window.setAttribute(Qt.WA_DeleteOnClose)
        sub_window.systemMenu().addActions(self.menu_actions)
        sub_window.destroyed.connect(self.should_exit_fullscren)

        if icon:
            sub_window.setWindowIcon(get_icon(icon))
        window.showMaximized()
        self._add_button_space()

    def tile_vertical_rev(self):
        self.tile_vertical(True)

    def tile_horizontal_rev(self):
        self.tile_horizontal(True)

    def tile_horizontal(self, reverse):
        windows = self.subWindowList()  # len(windows) != 0 always!
        height = self.viewport().height() / len(windows)
        x = 0
        if reverse:
            windows.reverse()
        for window in windows:
            window.showNormal()
            window.resize(self.width(), height)
            window.move(0, x)
            x += height

    def tile_vertical(self, reverse):
        windows = self.subWindowList()  # len(windows) != 0 always!
        width = self.width() / len(windows)
        x = 0
        if reverse:
            windows.reverse()
        height = self.viewport().height()
        for window in windows:
            window.showNormal()
            window.resize(width, height)
            window.move(x, 0)
            x += width

    def closeEvent(self, event):
        # Alt+F4 in fullscreen
        self.fullscreen_act.setChecked(False)
        event.ignore()

    def resizeEvent(self, event):
        super(MdiArea, self).resizeEvent(event)
        self._add_button_space()

    def should_exit_fullscren(self, _):
        if not self.subWindowList():
            self.fullscreen_act.setChecked(False)

    def keyPressEvent(self, event):
        # Not as action as `Ambiguous shortcut overload: Esc`
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.fullscreen_act.setChecked(False)
        else:
            return QtWidgets.QMdiArea.keyPressEvent(self, event)

    def eventFilter(self, obj, event):
        # Trick to not steal focus from QDialog window
        if (
            event.type() in (event.KeyPress, event.KeyRelease)
            and event.modifiers() & Qt.ControlModifier
        ):
            parent = obj
            for _level in range(6):
                parent = parent.parent()
                if parent is None:
                    break
                if isinstance(parent, QtWidgets.QDialog):
                    return False
        return super(MdiArea, self).eventFilter(obj, event)
