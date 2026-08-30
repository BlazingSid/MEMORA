from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from app.ui.utils.time_utils import relative_time


class MemoryCard(QFrame):

    def __init__(
        self,
        content: str,
        timestamp: str,
        parent=None,
    ):
        super().__init__(parent)

        self.setObjectName("MemoryCard")

        self.setMinimumHeight(130)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20, 18, 20, 16
        )

        layout.setSpacing(10)

        # ---------------------------------
        # Header
        # ---------------------------------

        header = QHBoxLayout()

        icon = QLabel("🧠")

        icon.setObjectName(
            "MemoryIcon"
        )

        header.addWidget(icon)

        label = QLabel("MEMORY")

        label.setObjectName(
            "MemoryLabel"
        )

        header.addWidget(label)

        header.addStretch()

        time = QLabel(
            relative_time(timestamp)
        )

        time.setObjectName(
            "MemoryTime"
        )

        header.addWidget(time)

        layout.addLayout(header)

        # ---------------------------------
        # Content
        # ---------------------------------

        text = QLabel(content)

        text.setObjectName(
            "MemoryContent"
        )

        text.setWordWrap(True)

        text.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        layout.addWidget(text)

        layout.addStretch()