'''
from PyQt5.QtWidgets import *

import Film_info_screen
import Main_Screen


class Firstwindow(QMainWindow, Main_Screen.Main_Screen):
    def __init__(self, parent=None):
        super(Firstwindow, self).__init__(parent)
        self.setupUi(self)
        self.label5.clicked.connect(self.hide)


class Secondwindow(QDialog, Film_info_screen.Film_screen):
    def __init__(self, parent=None):
        super(Secondwindow, self).__init__(parent)
        self.setupUi(self)
        self.label5.clicked.connect(self.hide)


class Manager:
    def __init__(self):
        self.first = Firstwindow()
        self.second = Secondwindow()

        self.first.label5.clicked.connect(self.second.show)
        self.second.label5.clicked.connect(self.first.show)

        self.first.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    manager = Manager()
    sys.exit(app.exec_())
'''