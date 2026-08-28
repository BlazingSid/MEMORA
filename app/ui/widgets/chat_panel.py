from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.ui.widgets.glass_card import GlassCard
from app.ui.widgets.search_bar import SearchBar
from app.ui.widgets.section_header import SectionHeader


class ChatPanel(GlassCard):
    """The Home page's conversational surface, retaining the existing controls."""

    def __init__(self, parent=None):
        super().__init__(parent, elevated=True)
        self.setObjectName("ChatPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 23, 24, 24)
        layout.setSpacing(18)

        layout.addWidget(
            SectionHeader(
                "Ask MEMORA",
                "Ask a question about the memories saved in this workspace.",
            )
        )

        answer_surface = QFrame()
        answer_surface.setObjectName("AnswerSurface")
        answer_layout = QVBoxLayout(answer_surface)
        answer_layout.setContentsMargins(16, 15, 16, 15)
        answer_layout.setSpacing(8)

        assistant_label = QLabel("MEMORA")
        assistant_label.setObjectName("AssistantLabel")
        answer_layout.addWidget(assistant_label)

        from PySide6.QtWidgets import QTextEdit

        self.answer_box = QTextEdit()
        self.answer_box.setObjectName("AnswerBox")
        self.answer_box.setReadOnly(True)
        self.answer_box.setPlaceholderText(
            "Ask a question and MEMORA will answer from your saved memories."
        )
        self.answer_box.setMinimumHeight(136)
        answer_layout.addWidget(self.answer_box)

        layout.addWidget(answer_surface)

        self.search_bar = SearchBar(
            "What do you remember about…",
            "Ask",
        )
        self.search_bar.setObjectName("AskBar")
        self.question_input = self.search_bar.input
        self.question_input.setObjectName("QuestionInput")
        self.ask_button = self.search_bar.action_button
        self.ask_button.setObjectName("AskButton")
        layout.addWidget(self.search_bar)
