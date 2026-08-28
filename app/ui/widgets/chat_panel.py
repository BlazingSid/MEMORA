from PySide6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout

from app.ui.widgets.glass_card import GlassCard
from app.ui.widgets.search_bar import SearchBar
from app.ui.widgets.section_header import SectionHeader


class ChatPanel(GlassCard):
    """A compact conversational surface that keeps the existing controls."""

    def __init__(self, parent=None):
        super().__init__(parent, elevated=True)
        self.setObjectName("ChatPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 23, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(
            SectionHeader(
                "Ask MEMORA",
                "Search your memories using natural language.",
            )
        )

        self.search_bar = SearchBar(
            "What do you remember about...",
            "Ask",
        )
        self.search_bar.setObjectName("AskBar")
        self.question_input = self.search_bar.input
        self.question_input.setObjectName("QuestionInput")
        self.ask_button = self.search_bar.action_button
        self.ask_button.setObjectName("AskButton")
        layout.addWidget(self.search_bar)

        answer_surface = QFrame()
        answer_surface.setObjectName("AnswerSurface")
        answer_layout = QVBoxLayout(answer_surface)
        answer_layout.setContentsMargins(16, 15, 16, 15)
        answer_layout.setSpacing(8)

        assistant_label = QLabel("MEMORA")
        assistant_label.setObjectName("AssistantLabel")
        answer_layout.addWidget(assistant_label)

        self.answer_box = QTextEdit()
        self.answer_box.setObjectName("AnswerBox")
        self.answer_box.setReadOnly(True)
        self.answer_box.setPlaceholderText(
            "Ask a question and MEMORA will search your memories."
        )
        self.answer_box.setMinimumHeight(82)
        self.answer_box.setMaximumHeight(112)
        answer_layout.addWidget(self.answer_box)

        layout.addWidget(answer_surface)
