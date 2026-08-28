from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.database.memory_db import save_memory
from app.database.vector_memory import add_memory
from app.core.llm_worker import LLMWorker
from app.ui.home import HomePage
from app.ui.memories import MemoriesPage
from app.ui.search import SearchPage
from app.ui.settings import SettingsPage
from app.ui.widgets.glass_card import GlassCard, apply_soft_shadow
from app.ui.widgets.nav_item import NavItem


class MemoraWindow(QMainWindow):
    """MEMORA's floating application shell and page coordinator."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MEMORA")
        self.resize(1200, 760)
        self.setMinimumSize(900, 620)

        self.build_ui()

    def build_ui(self):
        root = QWidget()
        root.setObjectName("ApplicationRoot")

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(18)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(244)
        apply_soft_shadow(sidebar, blur_radius=28, offset_y=7)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 22, 18, 18)
        sidebar_layout.setSpacing(6)

        brand_layout = QHBoxLayout()
        brand_layout.setContentsMargins(3, 0, 3, 0)
        brand_layout.setSpacing(10)

        brand_mark = QLabel("M")
        brand_mark.setObjectName("BrandMark")
        brand_mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_mark.setFixedSize(38, 38)

        brand_name = QLabel("MEMORA")
        brand_name.setObjectName("Logo")

        brand_layout.addWidget(brand_mark)
        brand_layout.addWidget(brand_name)
        brand_layout.addStretch()
        sidebar_layout.addLayout(brand_layout)
        sidebar_layout.addSpacing(33)

        self.home_button = NavItem("Home", "⌂")
        self.memories_button = NavItem("Memories", "◈")
        self.search_button = NavItem("Search", "⌕")
        self.settings_button = NavItem("Settings", "⚙")

        self.nav_buttons = [
            self.home_button,
            self.memories_button,
            self.search_button,
            self.settings_button,
        ]

        for button in self.nav_buttons[:3]:
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.settings_button)

        content_shell = GlassCard(elevated=True)
        content_shell.setObjectName("ContentShell")
        content_layout = QVBoxLayout(content_shell)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()
        self.pages.setObjectName("MainPages")

        self.home_page = HomePage(self)
        self.memories_page = MemoriesPage(self)
        self.search_page = SearchPage(self)
        self.settings_page = SettingsPage(self)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.memories_page)
        self.pages.addWidget(self.search_page)
        self.pages.addWidget(self.settings_page)
        content_layout.addWidget(self.pages)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content_shell, 1)
        self.setCentralWidget(root)

        for index, button in enumerate(self.nav_buttons):
            button.clicked.connect(
                lambda _checked=False, page_index=index: self.switch_page(
                    page_index
                )
            )

        # Existing HomePage public controls remain the integration boundary.
        self.home_page.remember_button.clicked.connect(self.remember)
        self.home_page.memory_input.returnPressed.connect(self.remember)
        self.home_page.ask_button.clicked.connect(self.ask_memora)
        self.home_page.question_input.returnPressed.connect(self.ask_memora)

        self.switch_page(0)

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.set_active(button_index == index)

    def remember(self):
        content = self.home_page.memory_input.text().strip()

        if not content:
            return

        memory_id = save_memory(content)
        add_memory(memory_id, content)
        self.home_page.memory_input.clear()
        self.home_page.refresh_recent_memories()

        # Refresh the existing memories listing after a successful save.
        old_page = self.memories_page
        self.pages.removeWidget(old_page)
        old_page.deleteLater()

        self.memories_page = MemoriesPage(self)
        self.pages.insertWidget(1, self.memories_page)

    def ask_memora(self):
        question = self.home_page.question_input.text().strip()

        if not question:
            return

        self.home_page.answer_box.setPlainText("MEMORA is thinking…")
        self.home_page.question_input.setEnabled(False)
        self.home_page.ask_button.setEnabled(False)

        self.llm_worker = LLMWorker(question)
        self.llm_worker.finished.connect(self.handle_llm_response)
        self.llm_worker.error.connect(self.handle_llm_error)
        self.llm_worker.start()

    def handle_llm_response(self, answer):
        self.home_page.answer_box.setPlainText(answer)
        self.home_page.question_input.setEnabled(True)
        self.home_page.ask_button.setEnabled(True)
        self.home_page.question_input.setFocus()

    def handle_llm_error(self, error):
        self.home_page.answer_box.setPlainText(
            f"MEMORA encountered an error:\n\n{error}"
        )
        self.home_page.question_input.setEnabled(True)
        self.home_page.ask_button.setEnabled(True)
        self.home_page.question_input.setFocus()
