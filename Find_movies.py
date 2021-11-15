import json
import os
import sqlite3
import threading
from pprint import pprint

import requests
import sys

from PyQt5 import QtCore

import Film_info_screen

from PyQt5.QtWidgets import *

import Main_Screen
import global_vars
from Main_Screen import *

class Find_movies(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global imdb_dict
        global res
        super().__init__()
        self.setGeometry(0, 0, 600, 1000)
        self.setWindowTitle("Films App")
        self.w = None

        self.label1 = QListWidget(self)
        self.label1.setGeometry(20, 220, 560, 600)
        #con = sqlite3.connect("yandex_project_1.sqlite")
        #cur = con.cursor()
        #query = "SELECT film_id from film_favorite"
        #res = cur.execute(query).fetchall()
        #print("GAY11111111111111111111!")
        #pprint(res)
        #print(len(res))

        """
        if (len(res) == 0):
            for i in range(10):
                self.label1.addItem("Add some movies first")
        else:
            self.any_favorite = True
            for i in range(len(res)):
                api_link = "https://imdb-api.com/en/API/Title/" + global_vars.var_API + "/" + res[i][0]
                #api_link = "https://imdb-api.com/en/API/Title/k_8fn0w7v6/tt0110413"
                print(api_link)
                #self.get_info(search_type, film_title, api_link)
                response = requests.get(api_link)
                fav_film_dict = json.loads(response.text)
                pprint(fav_film_dict)
                self.label1.addItem(fav_film_dict["fullTitle"])
                print(fav_film_dict["fullTitle"])
                self.label1.itemClicked.connect(self.click)
        """

        self.label2 = QPushButton(self)
        self.label2.setGeometry(180, 840, 200, 120)
        self.label2.setText("Go back")
        self.label2.clicked.connect(self.back)

        self.label3 = QLineEdit(self)
        self.label3.setGeometry(20, 20, 560, 100)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)

        self.label4 = QPushButton(self)
        self.label4.setGeometry(250, 140, 100, 60)
        self.label4.setText("Search")
        self.label4.clicked.connect(self.find_movie)

    def click(self, item):
        Film_info_screen.film_full_title = item.text()
        self.w = Film_info_screen.Film_screen()
        self.w.show()
        self.hide()

    def find_movie(self):
        api_link = "https://imdb-api.com/en/API/Title/" + global_vars.var_API + "/" + self.label3.text()
        # print(api_link)
        # print("!!!!!!!!!")
        # print("12")
        # print(res[i][0])
        # api_link = "https://imdb-api.com/en/API/Title/k_8fn0w7v6/tt0110413"
        # print(api_link)
        # self.get_info(search_type, film_title, api_link)
        response = requests.get(api_link)
        film_dict = json.loads(response.text)
        pprint(film_dict)
        if (film_dict["fullTitle"] == None):
            #print("EYSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            self.label4.setText("Try again")
        #else:

    def back(self):
        if self.w is None:
            #print("1123")
            self.w = Main_Screen.Main_Screen()
            self.w.show()
            self.close()
        else:
            self.w.close()
            self.w = None
        #self.w = Main_Screen()
        #self.w.show()
        ##self.hide()
        #self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Find_movies()
    ex.show()
    sys.exit(app.exec())