from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.styles.fonts import FONT_FAMILY, STAT_SIZE, FONT_WEIGHT_BOLD
from PySide6.QtGui import QFont


class StatCard(QFrame):
    """A restrained summary card for values available from the current UI data."""

    def __init__(self, label, value, detail, parent=None):
        super().__init__(parent)

        self.setObjectName("StatCard")
        self.setMinimumHeight(136)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(19, 18, 19, 18)
        layout.setSpacing(6)

        self.label = QLabel(label.upper())
        self.label.setObjectName("StatLabel")
        layout.addWidget(self.label)

        self.value = QLabel(str(value))
        self.value.setObjectName("StatValue")
        self.value.setFont(QFont(FONT_FAMILY, STAT_SIZE, FONT_WEIGHT_BOLD))
        layout.addWidget(self.value)

        self.detail = QLabel(detail)
        self.detail.setObjectName("StatDetail")
        self.detail.setWordWrap(True)
        layout.addWidget(self.detail)
        layout.addStretch()

    def set_value(self, value, detail=None):
        self.value.setText(str(value))
        if detail is not None:
            self.detail.setText(detail)
