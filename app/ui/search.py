from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from app.database.vector_memory import (
    search_memory_documents,
)


class SearchPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.build_ui()

    def build_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            45, 40, 45, 30
        )

        title = QLabel(
            "Search Memories"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Search by meaning, not just exact words."
        )

        subtitle.setObjectName(
            "Subtitle"
        )

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(25)

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "What are you looking for?"
        )

        self.search_input.setMinimumHeight(
            46
        )

        self.search_button = QPushButton(
            "⌕  Search"
        )

        self.search_button.setObjectName(
            "PrimaryButton"
        )

        self.search_button.setMinimumHeight(
            46
        )

        self.layout.addWidget(
            self.search_input
        )

        self.layout.addWidget(
            self.search_button
        )

        self.layout.addSpacing(25)

        self.results_layout = QVBoxLayout()

        self.layout.addLayout(
            self.results_layout
        )

        self.search_button.clicked.connect(
            self.perform_search
        )

        self.search_input.returnPressed.connect(
            self.perform_search
        )

        self.layout.addStretch()

    def perform_search(self):

        query = (
            self.search_input
            .text()
            .strip()
        )

        if not query:
            return

        while self.results_layout.count():

            item = (
                self.results_layout
                .takeAt(0)
            )

            if item.widget():
                item.widget().deleteLater()

        results = search_memory_documents(
            query,
            n_results=10,
        )

        if not results:

            label = QLabel(
                "No relevant memories found."
            )

            self.results_layout.addWidget(
                label
            )

            return

        title = QLabel(
            f"{len(results)} relevant memories"
        )

        title.setObjectName(
            "SectionTitle"
        )

        self.results_layout.addWidget(
            title
        )

        for memory in results:

            label = QLabel(
                f"🧠  {memory}"
            )

            label.setWordWrap(True)

            self.results_layout.addWidget(
                label
            )