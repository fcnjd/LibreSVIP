import atexit
import pathlib

from qmlease import slot
from qtpy.QtCore import QObject, Signal

import libresvip
from libresvip.core.config import ConflictPolicy, DarkMode, save_settings, settings


class ConfigItems(QObject):
    auto_set_output_extension_changed = Signal(bool)

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        atexit.register(save_settings)

    @slot(result=str)
    def get_version(self) -> str:
        return libresvip.__version__

    @slot(result=str)
    def get_conflict_policy(self) -> str:
        return settings.conflict_policy.value

    @slot(str, result=bool)
    def set_conflict_policy(self, policy: str) -> bool:
        try:
            conflict_policy = ConflictPolicy(policy)
            settings.conflict_policy = conflict_policy
            return True
        except ValueError:
            return False

    @slot(result=str)
    def get_theme(self) -> str:
        return settings.dark_mode.value

    @slot(str, result=bool)
    def set_theme(self, theme: str) -> bool:
        try:
            dark_mode = DarkMode(theme)
            settings.dark_mode = dark_mode
            return True
        except ValueError:
            return False

    @slot(str, result=bool)
    def get_bool(self, key) -> bool:
        value = getattr(settings, key)
        if key == "auto_set_output_extension":
            self.auto_set_output_extension_changed.emit(value)
        return value

    @slot(str, bool, result=bool)
    def set_bool(self, key, value) -> bool:
        if hasattr(settings, key):
            setattr(settings, key, value)
            return True
        return False

    @slot(result=str)
    def get_save_folder(self):
        return str(settings.save_folder.as_posix())

    @slot(str, result=bool)
    def set_save_folder(self, value) -> bool:
        path = pathlib.Path(value)
        if path.exists() and path.is_dir():
            settings.save_folder = path
            return True
        return False
