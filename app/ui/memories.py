from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from app.database.memory_db import get_memories


class MemoriesPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            45, 40, 45, 30
        )

        title = QLabel(
            "Your Memories"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Everything MEMORA currently remembers."
        )

        subtitle.setObjectName(
            "Subtitle"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(25)

        memories = get_memories()

        if not memories:

            empty = QLabel(
                "No memories yet."
            )

            layout.addWidget(empty)

        else:

            for _, content, created_at in memories:

                memory = QLabel(
                    f"🧠  {content}\n"
                    f"    {created_at}"
                )

                memory.setWordWrap(True)

                layout.addWidget(
                    memory
                )

        layout.addStretch()