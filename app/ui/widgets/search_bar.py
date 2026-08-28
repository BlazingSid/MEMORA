from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton


class SearchBar(QFrame):
    """A rounded input/action pair used for compact natural-language actions."""

    def __init__(self, placeholder, action_text, parent=None):
        super().__init__(parent)

        self.setObjectName("SearchBar")
        self.setProperty("focused", False)
        self.setMinimumHeight(58)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        self.input = QLineEdit()
        self.input.setObjectName("SearchBarInput")
        self.input.setPlaceholderText(placeholder)
        self.input.installEventFilter(self)

        self.action_button = QPushButton(action_text)
        self.action_button.setObjectName("SearchBarAction")
        self.action_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_button.setMinimumHeight(40)

        layout.addWidget(self.input, 1)
        layout.addWidget(self.action_button)

    def eventFilter(self, watched, event):
        if watched is self.input and event.type() in (
            QEvent.Type.FocusIn,
            QEvent.Type.FocusOut,
        ):
            self.setProperty(
                "focused",
                event.type() == QEvent.Type.FocusIn,
            )
            self.style().unpolish(self)
            self.style().polish(self)

        return super().eventFilter(watched, event)
