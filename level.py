import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, \
    QGridLayout


class LevelWindow(QWidget):
    def __init__(self, input_file, menu_window):
        super().__init__()
        self.setWindowTitle('Уровень')
        self.menu_window = menu_window
        self.input_file = input_file
        self.level = self.get_level_from_filename()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_title_label()
        self.create_buttons_layout()
        self.create_buttons()
        self.create_exit_and_restart()
        self.last_button = None


    def get_level_from_filename(self):
        # Получаем номер уровня из имени файла
        filename = self.input_file.split('/')[-1]  # Получаем только имя файла из пути
        level = filename.replace('input', '').replace('.txt', '')
        return level

    def create_title_label(self):
        # QLabel с номером уровня
        title_label = QLabel(f"Уровень {self.level}")
        self.layout.addWidget(title_label, alignment=Qt.AlignCenter)

    def create_buttons_layout(self):
        # Создаем сеточную разметку для кнопок
        self.buttons_layout = QGridLayout()
        self.layout.addLayout(self.buttons_layout)

    def create_buttons(self):
        with open(self.input_file, 'r') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        self.buttons = []

        for row_idx, row in enumerate(lines):
            row = row.split(' ')
            button_row = []
            for col_idx, char in enumerate(row):
                button = QPushButton()
                button.setFixedSize(50, 50)

                if char == '0':
                    button.setText(' ')
                    button.setStyleSheet('background-color: rgb(204, 204, 204);')
                elif char == '1':
                    button.setText('1')
                    button.setStyleSheet('background-color: rgb(255, 203, 151);')
                elif char == '2':
                    button.setText('2')
                    button.setStyleSheet('background-color: rgb(255, 174, 174);')
                elif char == '3':
                    button.setText('3')
                    button.setStyleSheet('background-color: rgb(168, 255, 168);')
                else:
                    button.setText('4')
                    button.setStyleSheet('background-color: rgb(159, 207, 255);')

                button.clicked.connect(self.button_clicked)
                button_row.append(button)
                self.buttons_layout.addWidget(button, row_idx, col_idx)

            self.buttons.append(button_row)

        self.layout.addStretch()

    def create_exit_and_restart(self):
        reload_button = QPushButton('Перезагрузить')
        reload_button.clicked.connect(self.reload_level)
        self.layout.addWidget(reload_button, alignment=Qt.AlignCenter)

        exit_button = QPushButton('Выход')
        exit_button.clicked.connect(self.exit_game)
        self.layout.addWidget(exit_button, alignment=Qt.AlignCenter)

    def button_clicked(self):

        clicked_button = self.sender()
        clicked_button.setCheckable(True)

        if self.last_button is None and clicked_button.text() != ' ':
            self.last_button = clicked_button

        if clicked_button.text() == 'X':
            temp_text = self.last_button.text()
            self.last_button.setText(clicked_button.text())
            clicked_button.setText(temp_text)
            self.last_button = None
            self.removeX()
            clicked_button.setStyleSheet('background-color: rgb(204, 204, 204);')
            num = 0
            clicked_button.setEnabled(False)
        elif clicked_button.text() == ' ':
            num = 0

        else:

            self.last_button = clicked_button
            num = int(clicked_button.text())
            self.removeX()
            clicked_button.setEnabled(True)


        row, col = self.get_button_position(clicked_button)

        self.addX(row, col, num)

        if self.check_win_condition():
            self.show_win_message()


    def removeX(self):
        for i in range(6):
            for j in range(6):
                butt = self.buttons[i][j]
                if butt.text() == 'X':
                    butt.setText(' ')
                    butt.setStyleSheet('background-color: rgb(204, 204, 204);')

    def addX(self, row, col, num):

        all_pos = [(row - num, col), (row + num, col),
                   (row, col - num), (row, col + num),
                   (row - num, col - num), (row + num, col + num),
                   (row + num, col - num), (row - num, col + num)]

        for r, c in all_pos:
            if len(self.buttons) > r >= 0 != num and 0 <= c < len(self.buttons[r]):
                button = self.buttons[r][c]
                if button.text() == ' ':
                    button.setText('X')

    def get_button_position(self, button):
        for row_idx, row in enumerate(self.buttons):
            if button in row:
                col_idx = row.index(button)
                return row_idx, col_idx

    def check_win_condition(self):
        for row in self.buttons:
            for button in row:
                if button.styleSheet() != 'background-color: rgb(204, 204, 204);':
                    return False
        return True

    def show_win_message(self):
        QMessageBox.information(self, 'УРА ДАУБИ', 'ПОБЕДААА')

    def reload_level(self):
        self.buttons_layout.removeWidget(self.buttons[0][0])
        for row in self.buttons:
            for button in row:
                self.buttons_layout.removeWidget(button)
                button.deleteLater()

        self.create_buttons()

    def exit_game(self):
        self.close()
        self.menu_window.show()


if __name__ == '__main__':
    app = QApplication([])
    menu_window = QWidget()
    menu_window.show()
    input_file = 'input.txt'
    level_window = LevelWindow(input_file, menu_window)
    level_window.show()
    app.exec_()
