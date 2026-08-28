from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton


class NavItem(QPushButton):
    """Sidebar navigation button with a QSS-driven active state."""

    def __init__(self, label, icon, parent=None):
        super().__init__(parent)

        self.setObjectName("NavItem")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(52)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 14, 0)
        layout.setSpacing(10)

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("NavIcon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )

        self.label = QLabel(label)
        self.label.setObjectName("NavLabel")
        self.label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )

        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)
        layout.addStretch()

    def set_active(self, active):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
