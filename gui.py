import PyQt5
import steam_api_scrape
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QGroupBox, QFormLayout, QSizePolicy
import sys
from steam_api_scrape import account_id, get_friend_ids, get_steam_name, get_game_list


class LibraryCompare(QWidget):
    def __init__(self):
        super().__init__()

        self.buttons = []
        self.friends = []
        self.games_form = QFormLayout()

        self.init_ui()

    def get_buttons(self):
        return self.buttons

    def get_friends(self):
        return self.friends

    def get_games_form(self):
        return self.games_form

    def add_button(self, button):
        self.buttons.append(button)

    def add_friend(self, friend):
        self.friends.append(friend)

    def reset_games_form(self):
        while self.get_games_form().rowCount() > 0:
            self.games_form.removeRow(0)

    def init_ui(self):
        # Initialise Layouts
        layout = QHBoxLayout()
        col_1 = QVBoxLayout()
        col_2 = QVBoxLayout()
        layout.addLayout(col_1)
        layout.addLayout(col_2)

        # Initialise Widgets
        friends_groupbox = QGroupBox("Friends")
        friends_form = QFormLayout()
        compare_btn = QPushButton("Compare")
        friends_scroll = QScrollArea()
        games_scroll = QScrollArea()
        games_groupbox = QGroupBox("Shared Games")

        for i, value in enumerate(get_friend_ids(account_id)):
            self.add_friend(value)
            self.add_button(QPushButton(get_steam_name(value), checkable=True))
            friends_form.addRow(self.get_buttons()[i])

        # Widget Settings/Layout
        compare_btn.clicked.connect(self.compare_btn_pressed)
        games_groupbox.setLayout(self.get_games_form())
        games_scroll.setWidget(games_groupbox)
        games_scroll.setWidgetResizable(True)
        games_scroll.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        friends_groupbox.setLayout(friends_form)
        friends_scroll.setWidget(friends_groupbox)
        friends_scroll.setWidgetResizable(True)
        friends_scroll.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        col_1.addWidget(friends_scroll)
        col_1.addWidget(compare_btn)
        col_2.addWidget(games_scroll)

        # Window Settings
        self.setLayout(layout)
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Steam Library Comparison Tool')
        self.show()

    def compare_btn_pressed(self):
        games = set(get_game_list(account_id))
        self.reset_games_form()
        # Creates list containing only games shared by all chosen users
        for i, button in enumerate(self.get_buttons()):
            if button.isChecked():
                games = games.intersection(set(get_game_list(self.get_friends()[i])))
        # Displays list on screen
        for game in games:
            self.get_games_form().addRow(QLabel(game))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryCompare()
    app.exec()
