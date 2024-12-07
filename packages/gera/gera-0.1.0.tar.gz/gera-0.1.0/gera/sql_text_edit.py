# encoding: utf-8
from __future__ import annotations
from typing import Iterable
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import namedtuple

Rule = namedtuple("Rule", ("pattern", "format"))
Qt = QtCore.Qt


def rule(expr: str, foreground: int):
    pattern = QtCore.QRegExp(expr)
    format = QtGui.QTextCharFormat()
    pattern.setCaseSensitivity(Qt.CaseInsensitive)
    format.setForeground(foreground)
    return Rule(pattern, format)


class SQLHighlighter(QtGui.QSyntaxHighlighter):
    COMMENT_RULE = rule("--[^\n]*", Qt.darkYellow)
    KEYWORD_RULE = rule("\\b(OR|AND|ABS)\\b", Qt.darkMagenta)

    def __init__(self, *args):
        super(SQLHighlighter, self).__init__(*args)
        self._column_rule = rule("", Qt.darkBlue)
        self._rules = self.KEYWORD_RULE, self._column_rule, self.COMMENT_RULE

    def highlightBlock(self, text):
        for pattern, format in self._rules:
            if pattern.isEmpty():
                continue
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                if length == 0:
                    break
                self.setFormat(index, length, format)
                index = pattern.indexIn(text, index + length)

    def set_column_names(self, names):
        self._column_rule.pattern.setPattern("\\b(" + "|".join(names) + ")\\b")


class SqlTextEdit(QtWidgets.QTextEdit):
    _completer = None
    apply = QtCore.pyqtSignal()

    def __init__(self):
        super(SqlTextEdit, self).__init__()
        self._highlighter = SQLHighlighter(self.document())

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        c = self._completer
        if c and c.popup().isVisible():
            if event.key() in (
                Qt.Key_Enter,
                Qt.Key_Return,
                Qt.Key_Escape,
                Qt.Key_Tab,
                Qt.Key_Backtab,
            ):
                event.ignore()
                return

        if event.key() == Qt.Key_Return and event.modifiers() & (
            Qt.ControlModifier | Qt.AltModifier
        ):
            self.apply.emit()
            event.accept()
        else:
            is_shortcut = (
                event.modifiers() & Qt.ControlModifier
            ) and event.key() == Qt.Key_Space
            if not c or not is_shortcut:
                super(SqlTextEdit, self).keyPressEvent(event)
            ctrl_or_shift = event.modifiers() & (
                Qt.ControlModifier | Qt.ShiftModifier
            )
            if not c or (ctrl_or_shift and not event.text()):
                return

            # end_of_word = "~!@#$%^&*+{}|:\"<>?,./'[]\\-="
            has_modifier = (
                event.modifiers() != Qt.NoModifier
            ) and not ctrl_or_shift
            completion_prefix = self.textUnderCursor()

            if not is_shortcut and (
                has_modifier or not event.text() or len(completion_prefix) < 2
            ):
                # event.text()[1:] in end_of_word  # < - makes no sense
                c.popup().hide()
                return
            if completion_prefix != c.completionPrefix():
                c.setCompletionPrefix(completion_prefix)
                c.popup().setCurrentIndex(c.completionModel().index(0, 0))

            cr = self.cursorRect()
            cr.setWidth(
                c.popup().sizeHintForColumn(0)
                + c.popup().verticalScrollBar().sizeHint().width()
            )
            c.complete(cr)

    def setCompleter(self, completer: QtWidgets.QCompleter):
        if self._completer:
            pass  # Actually, must disconnect something
            # QtCore.QObject.disconnect(self._completer, None, self, None)
        self._completer = completer
        if not completer:
            return
        completer.setWidget(self)
        completer.setCompletionMode(completer.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.insertCompletion)

    def completer(self):
        raise Exception("ToDo")
        return self._completer

    def insertCompletion(self, completion: str):
        c = self._completer
        if c.widget() is not self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(c.completionPrefix())
        tc.movePosition(tc.Left)
        tc.movePosition(tc.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self) -> str:
        tc = self.textCursor()
        tc.select(tc.WordUnderCursor)
        if len(tc.selectedText()) > 0:
            tc.clearSelection()
            tc.movePosition(tc.Left)
            tc.select(tc.WordUnderCursor)
            return tc.selectedText()
        else:
            return ""

    def setColumnNames(self, names: list[str]):
        self._completer = QtWidgets.QCompleter(names, self)
        self._completer_tips_count = 0
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self._completer)
        self._highlighter.set_column_names(names)

    def setTips(self, tips: Iterable[str]):
        if self._completer is None:
            return
        model = self._completer.model()
        model.removeRows(
            model.rowCount() - self._completer_tips_count,
            self._completer_tips_count,
        )
        self._completer_tips_count = len(tips)
        model.insertRows(model.rowCount(), self._completer_tips_count)
        for row, text in enumerate(
            tips, model.rowCount() - self._completer_tips_count
        ):
            model.setData(model.index(row, 0), text)

    def focusInEvent(self, event: QtGui.QFocusEvent):
        if self._completer:
            self._completer.setWidget(self)
        super().focusInEvent(event)
