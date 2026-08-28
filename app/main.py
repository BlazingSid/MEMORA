import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MemoraWindow


def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "MEMORA"
    )

    # Load global theme

    with open(
        "app/styles/theme.qss",
        "r",
        encoding="utf-8",
    ) as file:

        app.setStyleSheet(
            file.read()
        )

    window = MemoraWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()