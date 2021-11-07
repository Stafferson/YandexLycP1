import json
import os
import sqlite3
import sys
import threading
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

countR = True

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
        global film_id
        global film_title
        global film_image_url
        global con
        global cur

        super(Film_screen, self).__init__()
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("Films App")

        con = sqlite3.connect("yandex_project_1.sqlite")
        cur = con.cursor()

        api_link = "https://imdb-api.com/en/API/SearchMovie/k_907znyrc/" + film_full_title
        #self.get_info(search_type, film_title, api_link)
        response = requests.get(api_link)
        film_dict = json.loads(response.text)

        thread1 = threading.Thread(target=self.thread_function)
        thread1.start()

        film_id = (film_dict["results"])[0]["id"]
        film_title = (film_dict["results"])[0]["title"]
        film_image_url = (film_dict["results"])[0]["image"]

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
        self.label4.setText("Delete from favorite")
        self.label4.hide()

        self.label5 = QPushButton(self)
        self.label5.setGeometry(20, 190, 300, 150)
        self.label5.setText("Delete from watched")
        self.label5.hide()

        self.label6 = QPushButton(self)
        self.label6.setGeometry(20, 360, 300, 150)
        self.label6.setText("Edit personal comment")
        #self.label6.clicked.connect(self.click_edit_comment)
        self.label6.hide()

        self.label7 = QLineEdit(self)
        self.label7.setGeometry(340, 360, 300, 150)
        self.label7.hide()

        self.label8 = QPushButton(self)
        self.label8.setGeometry(400, 530, 180, 100)
        self.label8.setText("Save comment")
        self.label8.hide()
        self.label8.clicked.connect(lambda: self.click("4"))



    def click(self, button_type):
        global con
        global cur
        global countR


        if button_type == "1":
            query = "insert into film_favorite(film_id) values('" + film_id + "')"
            cur.execute(query)
            con.commit()
            self.label1.hide()
            self.label4.show()
        elif button_type == "2":
            query = "insert into film_watched(film_id) values('" + film_id + "')"
            cur.execute(query)
            con.commit()
            self.label2.hide()
            self.label5.show()

        elif button_type == "3":
            if (countR):
                self.label7.show()
                self.label8.show()
                countR = False
            else:
                self.label7.hide()
                self.label8.hide()
                countR = True

            #query = "select * from film_favorite"
            #result = cur.execute(query).fetchall()
            #print(result)
            #query = "select * from film_comments"
            #result = cur.execute(query).fetchall()
            #print(result)
            #query = "select * from film_watched"
            #result = cur.execute(query).fetchall()
            #print(result)

        else:
            query = "insert into film_comments(film_id, film_comment) values('" + film_id + "', '" + self.label7.text() + "')"
            cur.execute(query)
            con.commit()
            self.label3.hide()
            self.label6.show()

    def click_edit_comment(self):
        global con
        global cur

        print("edited")

    def thread_function(name):
        con = sqlite3.connect("yandex_project_1.sqlite")
        cur = con.cursor()

        query = "SELECT EXISTS(SELECT 1 FROM film_favorite WHERE film_id='" + film_id + "1');"
        res = cur.execute(query).fetchall()
        print(res)
        query = "SELECT EXISTS(SELECT 1 FROM film_watched WHERE film_id='" + film_id + "1');"
        res = cur.execute(query).fetchall()
        print(res)
        query = "SELECT EXISTS(SELECT 1 FROM film_comments WHERE film_id='" + film_id + "1');"
        res = cur.execute(query).fetchall()
        print(res)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Film_screen()
    ex.show()
    sys.exit(app.exec())