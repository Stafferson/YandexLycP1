import json
import sqlite3
import sys
import urllib
from pprint import pprint

import requests
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from DBClass import DBClass

film_full_title = ""

film_id = ""
#film_imdb_rating = ""
#film_imdb_rating_count = ""
film_image_url = ""
film_title = ""

film_dict = {}

is_watched = "0"
is_saved = "0"
is_commented = "0"

class Film_screen(QWidget):
    con = ""
    cur = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global film_full_title
        global film_dict

        super(Film_screen, self).__init__()
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("Films App")

        print(film_full_title)

        api_link = "https://imdb-api.com/en/API/SearchMovie/k_907znyrc/" + film_full_title
        #self.get_info(search_type, film_title, api_link)
        print(api_link)
        response = requests.get(api_link)
        film_dict = json.loads(response.text)
        pprint(film_dict)

        self.label1 = QPushButton(self)
        self.label1.setGeometry(20, 20, 300, 150)
        self.label1.setText("Save to favorite")
        self.label1.clicked.connect(lambda: self.click("1"))

        self.label2 = QPushButton(self)
        self.label2.setGeometry(20, 190, 300, 150)
        self.label2.setText("Save to watched")
        self.label2.clicked.connect(lambda: self.click("2"))

        self.label3 = QPushButton(self)
        self.label3.setGeometry(20, 360, 300, 150)
        self.label3.setText("Add personal comment")
        self.label3.clicked.connect(lambda: self.click("3"))
        #########################################################3
        self.label4 = QPushButton(self)
        self.label4.setGeometry(20, 20, 300, 150)
        self.label4.setText("Already saved to favorite")
        self.label4.hide()

        self.label5 = QPushButton(self)
        self.label5.setGeometry(20, 190, 300, 150)
        self.label5.setText("Already saved to watched")
        self.label5.hide()

        self.label6 = QPushButton(self)
        self.label6.setGeometry(20, 360, 300, 150)
        self.label6.setText("Edit personal comment")
        #self.label6.clicked.connect(self.click_edit_comment)
        self.label6.hide()

        #db = DBClass()
        #db.connect("yandex_project_1")
        self.con = sqlite3.connect("yandex_project_1")
        self.cur = self.con.cursor()


    def click(self, button_type):
        if button_type == "1":
            query = "insert into film_favorite(film_id)"
        elif button_type == "2":
            print("2")
        elif button_type == "3":
            print("3")

    def click_edit_comment(self):
        print("edited")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Film_screen()
    ex.show()
    sys.exit(app.exec())