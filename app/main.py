import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from app.database.memory_db import save_memory, get_memories
from app.database.vector_memory import add_memory

class MemoraWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MEMORA")
        self.resize(1100, 700)

        self.build_ui()

    def build_ui(self):
        root = QWidget()

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 25, 20, 20)

        logo = QLabel("🧠  MEMORA")

        logo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(30)

        for text in [
            "◉   Home",
            "◇   Memories",
            "⌕   Search",
        ]:
            button = QPushButton(text)
            button.setMinimumHeight(42)
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        settings_button = QPushButton("⚙   Settings")
        settings_button.setMinimumHeight(42)

        sidebar_layout.addWidget(settings_button)

        # =========================
        # MAIN CONTENT
        # =========================

        content = QFrame()

        content_layout = QVBoxLayout(content)

        content_layout.setContentsMargins(
            45, 40, 45, 30
        )

        header = QLabel("Welcome back, Shahid")

        header.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        subtitle = QLabel(
            "Give MEMORA something to remember."
        )

        subtitle.setStyleSheet("""
            font-size: 15px;
        """)

        content_layout.addWidget(header)
        content_layout.addWidget(subtitle)

        content_layout.addSpacing(30)

        # =========================
        # MEMORY INPUT
        # =========================

        memory_input = QLineEdit()

        memory_input.setPlaceholderText(
            "I learned..."
        )

        memory_input.setMinimumHeight(45)

        remember_button = QPushButton(
            "🧠  Remember"
        )

        remember_button.setMinimumHeight(45)

        content_layout.addWidget(memory_input)
        content_layout.addWidget(remember_button)

        content_layout.addSpacing(35)

        # =========================
        # RECENT MEMORIES
        # =========================

        memories_title = QLabel(
            "Recent Memories"
        )

        memories_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        content_layout.addWidget(memories_title)

        self.memory_list = QVBoxLayout()

        content_layout.addLayout(
            self.memory_list
        )

        content_layout.addStretch()

        # =========================
        # EVENTS
        # =========================

        remember_button.clicked.connect(
            lambda: self.remember(memory_input)
        )

        memory_input.returnPressed.connect(
            lambda: self.remember(memory_input)
        )

        # =========================
        # FINAL ASSEMBLY
        # =========================

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content)

        self.setCentralWidget(root)

        self.load_memories()

    def remember(self, memory_input):

        content = memory_input.text().strip()

        if not content:
            return

        memory_id = save_memory(content)

        add_memory(memory_id, content)

        memory_input.clear()

        self.load_memories()

    def load_memories(self):

        while self.memory_list.count():

            item = self.memory_list.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        memories = get_memories()

        for _, content, created_at in memories[:10]:

            memory = QLabel(
                f"🧠  {content}\n"
                f"    {created_at}"
            )

            memory.setWordWrap(True)

            memory.setStyleSheet("""
                padding: 12px;
                font-size: 14px;
            """)

            self.memory_list.addWidget(memory)


def main():

    app = QApplication(sys.argv)

    window = MemoraWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()