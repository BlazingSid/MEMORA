from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class MemoryCard(QFrame):
    """A compact memory preview made from content returned by the existing DB."""

    def __init__(self, content, created_at, parent=None):
        super().__init__(parent)

        self.setObjectName("MemoryCard")
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMinimumHeight(118)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 17, 18, 17)
        layout.setSpacing(13)

        icon = QLabel("M")
        icon.setObjectName("MemoryIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(34, 34)
        layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(7)

        category = QLabel("MEMORY")
        category.setObjectName("MemoryCategory")
        text_layout.addWidget(category)

        self.content_label = QLabel(content)
        self.content_label.setObjectName("MemoryContent")
        self.content_label.setWordWrap(True)
        text_layout.addWidget(self.content_label)

        self.timestamp_label = QLabel(str(created_at))
        self.timestamp_label.setObjectName("MemoryTimestamp")
        text_layout.addWidget(self.timestamp_label)

        layout.addLayout(text_layout, 1)
