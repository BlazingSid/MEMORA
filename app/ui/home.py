from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.database.memory_db import get_memories
from app.ui.widgets.memory_card import MemoryCard
from app.styles.fonts import FONT_FAMILY, FONT_WEIGHT_BOLD, TITLE_SIZE
from app.ui.widgets.chat_panel import ChatPanel
from app.ui.widgets.glass_card import GlassCard
from app.ui.widgets.memory_card import MemoryCard
from app.ui.widgets.search_bar import SearchBar
from app.ui.widgets.section_header import SectionHeader
from app.ui.widgets.stat_card import StatCard


class HomePage(QWidget):
    """MEMORA's responsive visual dashboard and existing action controls."""

    _COMPACT_LAYOUT_WIDTH = 800

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self._recent_memory_records = []
        self._recent_columns = None
        self.build_ui()
        self.refresh_recent_memories()
        self._update_responsive_layouts()

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
        content_layout.setSpacing(30)

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

        self.top_cards_layout = QBoxLayout(
            QBoxLayout.Direction.LeftToRight
        )
        self.top_cards_layout.setContentsMargins(0, 0, 0, 0)
        self.top_cards_layout.setSpacing(18)

        self.remember_card = GlassCard(elevated=True)
        self.remember_card.setObjectName("RememberCard")
        self.remember_card.setMinimumHeight(272)
        remember_layout = QVBoxLayout(self.remember_card)
        remember_layout.setContentsMargins(24, 23, 24, 24)
        remember_layout.setSpacing(16)
        remember_layout.addWidget(
            SectionHeader(
                "Capture a memory",
                "Save a thought, detail, or decision for later.",
            )
        )

        self.remember_bar = SearchBar("I learned...", "Remember")
        self.remember_bar.setObjectName("RememberBar")
        self.memory_input = self.remember_bar.input
        self.memory_input.setObjectName("MemoryInput")
        self.remember_button = self.remember_bar.action_button
        self.remember_button.setObjectName("RememberButton")
        remember_layout.addWidget(self.remember_bar)
        remember_layout.addStretch()

        capture_hint = QLabel("Press Enter to save a memory quickly.")
        capture_hint.setObjectName("CaptureHint")
        remember_layout.addWidget(capture_hint)

        self.chat_panel = ChatPanel()
        self.chat_panel.setMinimumHeight(272)
        self.question_input = self.chat_panel.question_input
        self.ask_button = self.chat_panel.ask_button
        self.answer_box = self.chat_panel.answer_box

        for card in (self.remember_card, self.chat_panel):
            size_policy = card.sizePolicy()
            size_policy.setHorizontalPolicy(QSizePolicy.Policy.Ignored)
            card.setSizePolicy(size_policy)

        self.top_cards_layout.addWidget(self.remember_card, 1)
        self.top_cards_layout.addWidget(self.chat_panel, 1)
        content_layout.addLayout(self.top_cards_layout)

        content_layout.addWidget(
            SectionHeader(
                "Recent memories",
                "Things you've recently taught MEMORA.",
            )
        )

        self.recent_memories_widget = QWidget()
        self.recent_memories_layout = QGridLayout(
            self.recent_memories_widget
        )
        self.recent_memories_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_memories_layout.setHorizontalSpacing(14)
        self.recent_memories_layout.setVerticalSpacing(12)
        content_layout.addWidget(self.recent_memories_widget)

        content_layout.addWidget(
            SectionHeader(
                "Memory insights",
                "A small view of the context in your workspace.",
            )
        )

        self.stats_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(14)

        self.total_memories_card = StatCard(
            "Memories",
            "0",
            "Saved memories",
        )
        self.today_memories_card = StatCard(
            "Today",
            "0",
            "Added today",
        )
        self.latest_memory_card = StatCard(
            "Recent",
            "--",
            "No memories yet",
        )

        for card in (
            self.total_memories_card,
            self.today_memories_card,
            self.latest_memory_card,
        ):
            self.stats_layout.addWidget(card, 1)

        content_layout.addLayout(self.stats_layout)
        content_layout.addStretch()

        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_responsive_layouts()

    def refresh_recent_memories(self):
        """Refresh dashboard values from the existing SQLite read API only."""

        memories = get_memories()
        self._recent_memory_records = memories[:4]

        self.total_memories_card.set_value(
            len(memories),
            "Saved memories",
        )

        today = date.today().isoformat()
        today_count = sum(
            1 for _, _, created_at in memories if str(created_at).startswith(today)
        )
        self.today_memories_card.set_value(today_count, "Added today")

        if memories:
            latest_timestamp = str(memories[0][2])
            date_part, separator, time_part = latest_timestamp.partition(" ")
            latest_value = time_part[:5] if separator else date_part
            latest_detail = f"Latest saved {date_part}" if separator else "Latest saved"
            self.latest_memory_card.set_value(latest_value, latest_detail)
        else:
            self.latest_memory_card.set_value("--", "No memories yet")

        self._rebuild_recent_memories()

    def _update_responsive_layouts(self):
        compact = self.width() < self._COMPACT_LAYOUT_WIDTH
        direction = (
            QBoxLayout.Direction.TopToBottom
            if compact
            else QBoxLayout.Direction.LeftToRight
        )

        if self.top_cards_layout.direction() != direction:
            self.top_cards_layout.setDirection(direction)

        if self.stats_layout.direction() != direction:
            self.stats_layout.setDirection(direction)

        columns = 1 if compact else 2
        if columns != self._recent_columns:
            self._recent_columns = columns
            self._rebuild_recent_memories()

    def _rebuild_recent_memories(self):
        while self.recent_memories_layout.count():
            item = self.recent_memories_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        columns = self._recent_columns or 1
        self.recent_memories_layout.setColumnStretch(0, 1)
        self.recent_memories_layout.setColumnStretch(1, 1 if columns == 2 else 0)

        if not self._recent_memory_records:
            self.recent_memories_layout.addWidget(
                self._build_empty_memory_card(),
                0,
                0,
                1,
                columns,
            )
            return

        for index, (_, content, created_at) in enumerate(
            self._recent_memory_records
        ):
            row, column = divmod(index, columns)
            self.recent_memories_layout.addWidget(
                MemoryCard(content, created_at),
                row,
                column,
            )

    @staticmethod
    def _build_empty_memory_card():
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

        return empty_card
