from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QGroupBox, QFormLayout
import sys
from steam_api_scrape import account_id, get_friend_ids, get_steam_name


class LibraryCompare(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        friends_groupbox = QGroupBox("Friends")
        friends_form = QFormLayout()

        friends = []
        buttons = []
        for i, value in enumerate(get_friend_ids(account_id)):
            friends.append(value)
            buttons.append(QPushButton(get_steam_name(value), checkable=True))
            friends_form.addRow(buttons[i])

        friends_groupbox.setLayout(friends_form)
        friends_scroll = QScrollArea()
        friends_scroll.setWidget(friends_groupbox)
        friends_scroll.setWidgetResizable(True)
        friends_scroll.setFixedHeight(400)

        row_1 = QHBoxLayout()
        row_1.addWidget(friends_scroll)

        self.setLayout(row_1)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Steam Library Comparison Tool')
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryCompare()
    app.exec()
