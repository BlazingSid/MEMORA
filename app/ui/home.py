from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.database.memory_db import get_memories
from app.styles.fonts import FONT_FAMILY, FONT_WEIGHT_BOLD, TITLE_SIZE
from app.ui.widgets.chat_panel import ChatPanel
from app.ui.widgets.glass_card import GlassCard
from app.ui.widgets.memory_card import MemoryCard
from app.ui.widgets.search_bar import SearchBar
from app.ui.widgets.section_header import SectionHeader
from app.ui.widgets.stat_card import StatCard


class HomePage(QWidget):
    """The dashboard page while preserving MemoraWindow's existing controls."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.build_ui()
        self.refresh_recent_memories()

    def build_ui(self):
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("PageScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        content.setObjectName("HomeContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(42, 38, 42, 42)
        content_layout.setSpacing(28)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        heading_layout = QVBoxLayout()
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(6)

        title = QLabel("Welcome back, Shahid")
        title.setObjectName("PageTitle")
        title.setFont(QFont(FONT_FAMILY, TITLE_SIZE, FONT_WEIGHT_BOLD))

        subtitle = QLabel("Your private memory space is ready when you are.")
        subtitle.setObjectName("Subtitle")

        heading_layout.addWidget(title)
        heading_layout.addWidget(subtitle)
        header_layout.addLayout(heading_layout)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        remember_card = GlassCard(elevated=False)
        remember_card.setObjectName("RememberCard")
        remember_layout = QVBoxLayout(remember_card)
        remember_layout.setContentsMargins(23, 21, 23, 22)
        remember_layout.setSpacing(16)
        remember_layout.addWidget(
            SectionHeader(
                "Capture a memory",
                "Save a thought, detail, or decision for later.",
            )
        )

        self.remember_bar = SearchBar(
            "Add something MEMORA should remember…",
            "Remember",
        )
        self.remember_bar.setObjectName("RememberBar")
        self.memory_input = self.remember_bar.input
        self.memory_input.setObjectName("MemoryInput")
        self.remember_button = self.remember_bar.action_button
        self.remember_button.setObjectName("RememberButton")
        remember_layout.addWidget(self.remember_bar)
        content_layout.addWidget(remember_card)

        self.chat_panel = ChatPanel()
        self.question_input = self.chat_panel.question_input
        self.ask_button = self.chat_panel.ask_button
        self.answer_box = self.chat_panel.answer_box
        content_layout.addWidget(self.chat_panel)

        content_layout.addWidget(
            SectionHeader(
                "Recent memories",
                "Your latest saved context, ready when you need it.",
            )
        )

        self.recent_memories_widget = QWidget()
        self.recent_memories_layout = QVBoxLayout(self.recent_memories_widget)
        self.recent_memories_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_memories_layout.setSpacing(12)
        content_layout.addWidget(self.recent_memories_widget)

        content_layout.addWidget(
            SectionHeader(
                "Memory activity",
                "A quiet overview of the context in this workspace.",
            )
        )

        activity_layout = QHBoxLayout()
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(14)

        self.total_memories_card = StatCard(
            "Memories stored",
            "0",
            "Your saved context",
        )
        activity_layout.addWidget(self.total_memories_card, 1)

        reflection_card = GlassCard()
        reflection_card.setObjectName("ReflectionCard")
        reflection_layout = QVBoxLayout(reflection_card)
        reflection_layout.setContentsMargins(19, 18, 19, 18)
        reflection_layout.setSpacing(7)

        reflection_label = QLabel("MAKE IT USEFUL")
        reflection_label.setObjectName("StatLabel")
        reflection_layout.addWidget(reflection_label)

        reflection_title = QLabel("Small details become useful context.")
        reflection_title.setObjectName("ReflectionTitle")
        reflection_title.setWordWrap(True)
        reflection_layout.addWidget(reflection_title)

        reflection_note = QLabel(
            "Capture the things you would rather not have to remember twice."
        )
        reflection_note.setObjectName("StatDetail")
        reflection_note.setWordWrap(True)
        reflection_layout.addWidget(reflection_note)
        reflection_layout.addStretch()

        activity_layout.addWidget(reflection_card, 1)
        content_layout.addLayout(activity_layout)
        content_layout.addStretch()

        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)

    def refresh_recent_memories(self):
        """Refresh UI-only summaries from the existing memory database API."""

        memories = get_memories()
        self.total_memories_card.set_value(
            len(memories),
            "Your saved context",
        )

        while self.recent_memories_layout.count():
            item = self.recent_memories_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not memories:
            empty_card = QFrame()
            empty_card.setObjectName("EmptyMemoryCard")

            empty_layout = QVBoxLayout(empty_card)
            empty_layout.setContentsMargins(20, 18, 20, 18)
            empty_layout.setSpacing(5)

            empty_title = QLabel("Your memory space is waiting.")
            empty_title.setObjectName("EmptyStateTitle")
            empty_layout.addWidget(empty_title)

            empty_detail = QLabel(
                "Capture your first detail above and it will appear here."
            )
            empty_detail.setObjectName("EmptyStateDetail")
            empty_detail.setWordWrap(True)
            empty_layout.addWidget(empty_detail)

            self.recent_memories_layout.addWidget(empty_card)
            return

        for _, content, created_at in memories[:3]:
            self.recent_memories_layout.addWidget(
                MemoryCard(content, created_at)
            )
