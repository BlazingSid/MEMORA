from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class SettingsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            45, 40, 45, 30
        )

        title = QLabel(
            "Settings"
        )

        title.setObjectName(
            "PageTitle"
        )

        layout.addWidget(title)

        layout.addSpacing(20)

        info = QLabel(
            "MEMORA settings will be added here."
        )

        layout.addWidget(info)

        layout.addStretch()