import json
import os
import sqlite3
import threading
from pprint import pprint

import requests
import sys
import Film_info_screen

from PyQt5.QtWidgets import *

import global_vars

counter = 10


class Liked_movies(QWidget):

    any_favorite = False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global imdb_dict
        super(Liked_movies, self).__init__()
        self.setGeometry(0, 0, 600, 1000)
        self.setWindowTitle("Films App")

        self.label1 = QListWidget(self)
        self.label1.setGeometry(20, 20, 560, 960)

        con = sqlite3.connect("yandex_project_1.sqlite")
        cur = con.cursor()
        query = "SELECT film_id from film_favorite"
        res = cur.execute(query).fetchall()
        #print(len(res))

        if (len(res) == 0):
            for i in range(10):
                self.label1.addItem("Add some movies first")
        else:
            self.any_favorite = True
            for i in range(len(res)):
                api_link = "https://imdb-api.com/en/API/Title/" + global_vars.var_API + "/" + res[i][0]
                #api_link = "https://imdb-api.com/en/API/Title/k_8fn0w7v6/tt0110413"
                #print(api_link)
                # self.get_info(search_type, film_title, api_link)
                response = requests.get(api_link)
                fav_film_dict = json.loads(response.text)
                pprint(fav_film_dict)
                self.label1.addItem(fav_film_dict["fullTitle"])
                #print(fav_film_dict["fullTitle"])
                self.label1.itemClicked.connect(self.click)

    def click(self, item):
        Film_info_screen.film_full_title = item.text()
        w = Film_info_screen.Film_screen()
        w.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Liked_movies()
    ex.show()
    sys.exit(app.exec())