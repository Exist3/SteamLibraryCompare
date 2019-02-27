from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import sys
import steam_api_scrape


class LibraryCompare(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        label = QLabel("Hello World!")
        label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryCompare()
    app.exec()
