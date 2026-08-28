from PySide6.QtCore import QThread, Signal

from app.core.rag import ask_memora


class LLMWorker(QThread):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, question):
        super().__init__()

        self.question = question

    def run(self):

        try:
            answer = ask_memora(
                self.question
            )

            self.finished.emit(answer)

        except Exception as e:

            self.error.emit(
                str(e)
            )