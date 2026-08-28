import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from app.database.memory_db import save_memory, get_memories
from app.database.vector_memory import (
    add_memory,
    search_memory_documents,
)
from app.core.rag import ask_memora as rag_ask


class MemoraWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MEMORA")
        self.resize(1100, 700)

        self.build_ui()

    # =====================================================
    # BUILD UI
    # =====================================================

    def build_ui(self):

        root = QWidget()

        root_layout = QHBoxLayout(root)

        root_layout.setContentsMargins(
            0, 0, 0, 0
        )

        root_layout.setSpacing(0)

        # =================================================
        # SIDEBAR
        # =================================================

        sidebar = QFrame()

        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)

        sidebar_layout.setContentsMargins(
            20, 25, 20, 20
        )

        logo = QLabel("🧠  MEMORA")

        logo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(logo)

        sidebar_layout.addSpacing(30)

        # -------------------------
        # Navigation
        # -------------------------

        home_button = QPushButton(
            "◉   Home"
        )

        memories_button = QPushButton(
            "◇   Memories"
        )

        search_button = QPushButton(
            "⌕   Search"
        )

        settings_button = QPushButton(
            "⚙   Settings"
        )

        self.nav_buttons = [
            home_button,
            memories_button,
            search_button,
            settings_button,
        ]

        for button in self.nav_buttons:

            button.setMinimumHeight(42)

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            sidebar_layout.addWidget(
                button
            )

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(
            settings_button
        )

        # =================================================
        # CONTENT AREA
        # =================================================

        self.content = QFrame()

        self.content_layout = QVBoxLayout(
            self.content
        )

        self.content_layout.setContentsMargins(
            45, 40, 45, 30
        )

        # =================================================
        # ROOT
        # =================================================

        root_layout.addWidget(
            sidebar
        )

        root_layout.addWidget(
            self.content
        )

        self.setCentralWidget(root)

        # =================================================
        # CONNECT NAVIGATION
        # =================================================

        home_button.clicked.connect(
            self.show_home
        )

        memories_button.clicked.connect(
            self.show_memories
        )

        search_button.clicked.connect(
            self.show_search
        )

        settings_button.clicked.connect(
            self.show_settings
        )

        # Start on Home

        self.show_home()

    # =====================================================
    # CLEAR CONTENT
    # =====================================================

    def clear_content(self):

        while self.content_layout.count():

            item = self.content_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    # =====================================================
    # HOME
    # =====================================================

    def show_home(self):

        self.clear_content()

        header = QLabel(
            "Welcome back, Shahid"
        )

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

        self.content_layout.addWidget(
            header
        )

        self.content_layout.addWidget(
            subtitle
        )

        self.content_layout.addSpacing(30)

        # -------------------------
        # Remember
        # -------------------------

        remember_title = QLabel(
            "Remember something"
        )

        remember_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.content_layout.addWidget(
            remember_title
        )

        memory_input = QLineEdit()

        memory_input.setPlaceholderText(
            "I learned..."
        )

        memory_input.setMinimumHeight(45)

        remember_button = QPushButton(
            "🧠  Remember"
        )

        remember_button.setMinimumHeight(
            45
        )

        self.content_layout.addWidget(
            memory_input
        )

        self.content_layout.addWidget(
            remember_button
        )

        remember_button.clicked.connect(
            lambda: self.remember(
                memory_input
            )
        )

        memory_input.returnPressed.connect(
            lambda: self.remember(
                memory_input
            )
        )

        self.content_layout.addSpacing(30)

        # -------------------------
        # Ask
        # -------------------------

        ask_title = QLabel(
            "Ask MEMORA"
        )

        ask_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.content_layout.addWidget(
            ask_title
        )

        self.question_input = QLineEdit()

        self.question_input.setPlaceholderText(
            "What do you remember about..."
        )

        self.question_input.setMinimumHeight(
            45
        )

        ask_button = QPushButton(
            "💭  Ask MEMORA"
        )

        ask_button.setMinimumHeight(
            45
        )

        self.answer_box = QTextEdit()

        self.answer_box.setReadOnly(
            True
        )

        self.answer_box.setPlaceholderText(
            "MEMORA's answer will appear here..."
        )

        self.answer_box.setMinimumHeight(
            130
        )

        self.content_layout.addWidget(
            self.question_input
        )

        self.content_layout.addWidget(
            ask_button
        )

        self.content_layout.addWidget(
            self.answer_box
        )

        ask_button.clicked.connect(
            self.ask_memora
        )

        self.question_input.returnPressed.connect(
            self.ask_memora
        )

        self.content_layout.addStretch()

    # =====================================================
    # MEMORIES
    # =====================================================

    def show_memories(self):

        self.clear_content()

        title = QLabel(
            "Your Memories"
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        self.content_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Everything MEMORA currently remembers."
        )

        self.content_layout.addWidget(
            subtitle
        )

        self.content_layout.addSpacing(
            25
        )

        memories = get_memories()

        if not memories:

            empty = QLabel(
                "No memories yet."
            )

            self.content_layout.addWidget(
                empty
            )

            return

        for _, content, created_at in memories:

            memory = QLabel(
                f"🧠  {content}\n"
                f"    {created_at}"
            )

            memory.setWordWrap(True)

            memory.setStyleSheet("""
                padding: 14px;
                font-size: 14px;
            """)

            self.content_layout.addWidget(
                memory
            )

        self.content_layout.addStretch()

    # =====================================================
    # SEARCH
    # =====================================================

    def show_search(self):

        self.clear_content()

        title = QLabel(
            "Search Memories"
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        self.content_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Search by meaning, not just exact words."
        )

        self.content_layout.addWidget(
            subtitle
        )

        self.content_layout.addSpacing(
            25
        )

        search_input = QLineEdit()

        search_input.setPlaceholderText(
            "What are you looking for?"
        )

        search_input.setMinimumHeight(
            45
        )

        search_button = QPushButton(
            "⌕  Search"
        )

        search_button.setMinimumHeight(
            45
        )

        self.search_results_layout = (
            QVBoxLayout()
        )

        self.content_layout.addWidget(
            search_input
        )

        self.content_layout.addWidget(
            search_button
        )

        self.content_layout.addSpacing(
            25
        )

        self.content_layout.addLayout(
            self.search_results_layout
        )

        search_button.clicked.connect(
            lambda: self.perform_search(
                search_input
            )
        )

        search_input.returnPressed.connect(
            lambda: self.perform_search(
                search_input
            )
        )

        self.content_layout.addStretch()

    # =====================================================
    # PERFORM SEARCH
    # =====================================================

    def perform_search(
        self,
        search_input
    ):

        query = (
            search_input
            .text()
            .strip()
        )

        if not query:
            return

        # Clear previous results

        while (
            self.search_results_layout.count()
        ):

            item = (
                self.search_results_layout
                .takeAt(0)
            )

            widget = item.widget()

            if widget:
                widget.deleteLater()

        # Search ChromaDB

        results = search_memory_documents(
            query,
            n_results=10,
        )

        if not results:

            no_results = QLabel(
                "No relevant memories found."
            )

            self.search_results_layout.addWidget(
                no_results
            )

            return

        result_title = QLabel(
            f"{len(results)} relevant memories"
        )

        result_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
        """)

        self.search_results_layout.addWidget(
            result_title
        )

        for memory in results:

            label = QLabel(
                f"🧠  {memory}"
            )

            label.setWordWrap(True)

            label.setStyleSheet("""
                padding: 12px;
                font-size: 14px;
            """)

            self.search_results_layout.addWidget(
                label
            )

    # =====================================================
    # SETTINGS
    # =====================================================

    def show_settings(self):

        self.clear_content()

        title = QLabel(
            "Settings"
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        self.content_layout.addWidget(
            title
        )

        self.content_layout.addSpacing(
            20
        )

        info = QLabel(
            "MEMORA settings will be added here."
        )

        self.content_layout.addWidget(
            info
        )

        self.content_layout.addStretch()

    # =====================================================
    # SAVE MEMORY
    # =====================================================

    def remember(
        self,
        memory_input
    ):

        content = (
            memory_input
            .text()
            .strip()
        )

        if not content:
            return

        memory_id = save_memory(
            content
        )

        add_memory(
            memory_id,
            content
        )

        memory_input.clear()

    # =====================================================
    # ASK MEMORA
    # =====================================================

    def ask_memora(self):

        question = (
            self.question_input
            .text()
            .strip()
        )

        if not question:
            return

        self.answer_box.setPlainText(
            "MEMORA is thinking..."
        )

        answer = rag_ask(
            question
        )

        self.answer_box.setPlainText(
            answer
        )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

def main():

    app = QApplication(
        sys.argv
    )

    window = MemoraWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()