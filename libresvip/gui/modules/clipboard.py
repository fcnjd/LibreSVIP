from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement, QmlSingleton

from __feature__ import snake_case, true_property  # isort:skip # noqa: F401

QML_IMPORT_NAME = "LibreSVIP"
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0


@QmlElement
@QmlSingleton
class Clipboard(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.clipboard = QGuiApplication.clipboard()

    @Slot(str, result=bool)
    def set_clipboard(self, text):
        self.clipboard.set_text(text)
        return True
