from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.styles.fonts import FONT_FAMILY, SECTION_SIZE, FONT_WEIGHT_SEMIBOLD


class SectionHeader(QWidget):
    """A compact title and optional supporting line for content sections."""

    def __init__(self, title, subtitle=None, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.title = QLabel(title)
        self.title.setObjectName("SectionTitle")
        self.title.setFont(QFont(FONT_FAMILY, SECTION_SIZE, FONT_WEIGHT_SEMIBOLD))
        layout.addWidget(self.title)

        self.subtitle = None
        if subtitle:
            self.subtitle = QLabel(subtitle)
            self.subtitle.setObjectName("SectionSubtitle")
            self.subtitle.setWordWrap(True)
            layout.addWidget(self.subtitle)
