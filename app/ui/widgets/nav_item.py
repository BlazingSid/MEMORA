from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class NavItem(QPushButton):
    """Sidebar navigation button with a QSS-driven active state."""

    def __init__(self, label, icon, parent=None):
        super().__init__(f"{icon}   {label}", parent)

        self.setObjectName("NavItem")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)

    def set_active(self, active):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
