import json
from pprint import pprint

import requests
import sys
import Film_info_screen
from PyQt5.uic.properties import QtGui
import Film_info_screen

from PyQt5.QtWidgets import *

counter = 10
imdb_dict = {}


class Main_Screen(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global imdb_dict
        # super(Main_Screen, self).__init__()
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("Films App")

        self.label1 = QPushButton(self)
        self.label1.setGeometry(20, 20, 300, 150)
        self.label1.setText("My liked films")

        self.label2 = QPushButton(self)
        self.label2.setGeometry(20, 190, 300, 150)
        self.label2.setText("My comments about films")

        self.label3 = QPushButton(self)
        self.label3.setGeometry(20, 360, 300, 150)
        self.label3.setText("My watched movies")

        self.label4 = QPushButton(self)
        self.label4.setGeometry(20, 530, 300, 150)
        self.label4.setText("My statistics")

        self.label5 = QListWidget(self)
        self.label5.setGeometry(500, 20, 500, 800)
        url = "https://imdb-api.com/en/API/Top250Movies/k_907znyrc"
        response = requests.get(url)
        imdb_dict = json.loads(response.text)
        pprint(imdb_dict)
        for i in range(counter):
            self.label5.addItem((imdb_dict["items"])[i]["fullTitle"])
        self.label5.addItem("Load next 10 films")
        self.label5.verticalScrollBar().valueChanged.connect(self.scrolled)
        self.label5.itemClicked.connect(self.click)

        url_image = 'https://m.media-amazon.com/images/M/MV5BYzJmMWE5NjAtNWMyZS00NmFiLWIwMDgtZDE2NzczYWFhNzIzXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_UX128_CR0,3,128,176_AL_.jpg'

        from PyQt5.QtGui import QImage
        self.image = QImage()
        self.image.loadFromData(requests.get(url_image).content)

        self.label6 = QLabel()
        self.label6.setGeometry(20, 530, 300, 150)
        self.label6.setScaledContents(True)
        from PyQt5.QtGui import QPixmap
        self.label6.setPixmap(QPixmap(self.image))
        self.label6.setGeometry(900, 900, 300, 300)
        self.grid = QGridLayout()
        #self.grid.addWidget(self.label6, 0, 0)
        self.setLayout(self.grid)
        self.label6 = QPushButton(self)
        self.label6.setGeometry(670, 840, 160, 50)
        self.label6.setText("Top ")
        self.label6.clicked.connect(self.click)

        self.label7 = QPushButton(self)
        self.label7.setGeometry(670, 840, 160, 50)
        self.label7.setText("Load more")
        self.label7.clicked.connect(self.click)

        self.label8 = QPushButton(self)
        self.label8.setGeometry(670, 840, 160, 50)
        self.label8.setText("Load more")
        self.label8.clicked.connect(self.click)

        self.label9 = QPushButton(self)
        self.label9.setGeometry(670, 840, 160, 50)
        self.label9.setText("Load more")
        self.label9.clicked.connect(self.click)


    def scrolled(self, value):
        if value == self.label5.verticalScrollBar().maximum():
            print("TOP!!!")

    def click(self, item):
        global imdb_dict
        global counter
        if item.text() == "Load next 10 films":
            if counter == 240:
                counter += 10
                self.label5.clear()
                for i in range(250):
                    self.label5.addItem((imdb_dict["items"])[i]["fullTitle"])
            else:
                counter += 10
                for i in range(counter - 1, counter - 11, -1):
                    self.label5.insertItem(counter - 10, (imdb_dict["items"])[i]["fullTitle"])
        else:
            Film_info_screen.film_full_title = item.text()
            Film_info_screen.search_type = 1
            self.w = Film_info_screen.Film_screen()
            self.w.show()
            ex.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main_Screen()
    ex.show()
    sys.exit(app.exec())