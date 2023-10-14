import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

from level import LevelWindow


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Цифровой кузнечик')
        self.layout = QVBoxLayout()
        self.label = QLabel('Цифровой кузнечик')
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        for level in range(1, 3):
            level_button = QPushButton(f'Уровень {level}')
            level_button.clicked.connect(lambda _, lvl=level: self.start_level(lvl))
            self.layout.addWidget(level_button)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.close)
        self.layout.addWidget(exit_button)


        self.setLayout(self.layout)

    def start_level(self, level):
        file_name = f"inputs/input{level}.txt"
        self.level_window = LevelWindow(file_name, self)
        self.level_window.show()
        return self.level_window



if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    menu_window.show()
    sys.exit(app.exec_())

