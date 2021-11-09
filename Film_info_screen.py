import json
import os
import sqlite3
import sys
import threading
import urllib
from pprint import pprint

import requests
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import *

import time

import global_vars
from DBClass import DBClass
from Main_Screen import Main_Screen

film_full_title = ""

film_id = ""
#film_imdb_rating = ""
#film_imdb_rating_count = ""
film_image_url = ""
film_title = ""

film_dict = {}

countR = True

is_watched = False
is_saved = False
is_commented = False

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

        api_link = "https://imdb-api.com/en/API/SearchMovie/" + global_vars.var_API + "/" + film_full_title
        #print(api_link)
        #self.get_info(search_type, film_title, api_link)
        response = requests.get(api_link)
        film_dict = json.loads(response.text)
        #print(film_dict)

        film_id = (film_dict["results"])[0]["id"]
        film_title = (film_dict["results"])[0]["title"]
        film_image_url = (film_dict["results"])[0]["image"]
        #print("!!!!!!!!!")
        #print(film_id)
        #print(film_title)
        #print(film_image_url)
        #print("!!!!!!!!!")

        image = QImage()
        image.loadFromData(requests.get(film_image_url).content)
        image = (QPixmap(image)).scaled(800, 400)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(image))
        image_label.show()

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
        #print("1!!!!!!!!!")

        #########################################################

        self.label4 = QPushButton(self)
        self.label4.setGeometry(20, 20, 300, 150)
        self.label4.setText("Delete from favorite")
        self.label4.clicked.connect(lambda: self.click("7"))
        self.label4.hide()

        self.label5 = QPushButton(self)
        self.label5.setGeometry(20, 190, 300, 150)
        self.label5.setText("Delete from watched")
        self.label5.clicked.connect(lambda: self.click("8"))
        self.label5.hide()

        self.label6 = QPushButton(self)
        self.label6.setGeometry(20, 360, 300, 150)
        self.label6.setText("Edit personal comment")
        self.label6.clicked.connect(lambda: self.click("3"))
        self.label6.hide()
        #print("2!!!!!!!!!")

        #########################################################3

        self.label7 = QLineEdit(self)
        self.label7.setGeometry(340, 360, 300, 150)
        self.label7.hide()

        self.label8 = QPushButton(self)
        self.label8.setGeometry(400, 530, 180, 100)
        self.label8.setText("Save comment")
        self.label8.hide()
        self.label8.clicked.connect(lambda: self.click("4"))
        '''
        self.label9 = QPushButton(self)
        self.label9.setGeometry(20, 880, 180, 100)
        self.label9.setText("Go Back")
        self.label9.clicked.connect(lambda: self.click("6"))
        print("3!!!!!!!!!")
        '''

        #########################################################

        self.label10 = QPushButton(self)
        self.label10.setGeometry(1280, 20, 200, 150)
        self.label10.setText("Download information in txt")
        self.label10.clicked.connect(lambda: self.click("9"))
        #print("4!!!!!!!!!")

        thread1 = threading.Thread(target=self.thread_function("gay"))
        thread1.start()

    def thread_function(self, name):
        global is_commented
        global is_watched
        global is_saved

        con = sqlite3.connect("yandex_project_1.sqlite")
        cur = con.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM film_favorite WHERE film_id = '" + film_id + "');"
        res = cur.execute(query).fetchall()
        #print(res)
        if str(res[0][0]) == "1":
            self.label1.hide()
            self.label4.show()
            is_saved = True
        query = "SELECT EXISTS(SELECT 1 FROM film_watched WHERE film_id = '" + film_id + "');"
        res = cur.execute(query).fetchall()
        #print(query)
        #print(res)
        if str(res[0][0]) == "1":
            self.label2.hide()
            self.label5.show()
            is_watched = True
        query = "SELECT EXISTS(SELECT 1 FROM film_comments WHERE film_id = '" + film_id + "');"
        res = cur.execute(query).fetchall()
        #print(query)
        #print(res)
        if str(res[0][0]) == "1":
            self.label3.hide()
            self.label6.show()
            is_commented = True
            #self.label8.clicked.connect(lambda: self.click("4_edit"))
            query = "SELECT film_comment from film_comments where film_id = '" + film_id + "'"
            res = cur.execute(query).fetchall()
            #print("##########################")
            #print(query)
            #print(res)
            self.label7.setText(res[0][0])
            #print("##########################")

    def click(self, button_type):
        global con
        global cur
        global countR

        global is_commented
        global is_watched
        global is_saved

        if button_type == "1":
            try:
                query = "insert into film_favorite(film_id) values('" + film_id + "')"
                cur.execute(query)
                con.commit()
                self.label1.hide()
                self.label4.show()
            except:
                self.label1.setText("Something wrong occured")

        elif button_type == "2":
            try:
                query = "insert into film_watched(film_id) values('" + film_id + "')"
                cur.execute(query)
                con.commit()
                self.label2.hide()
                self.label5.show()
            except:
                self.label2.setText("Something wrong occured")

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

        elif button_type == "4":
            if is_commented:
                if self.label7.text() != "":
                    #print("SOIDET")
                    query = "update film_comments set film_comment = '" + self.label7.text() + "' where film_id = '" + film_id + "'"
                    print(query)
                    cur.execute(query)
                    con.commit()
                    self.label3.hide()
                    self.label6.show()
                    self.label8.hide()
                    self.label7.hide()
                else:
                    self.label8.setText("Write message, please")
                    #time.sleep(2)
                    #self.label8.setText("Save comment")
            else:
                try:
                    query = "insert into film_comments(film_id, film_comment) values('" + film_id + "', '" + self.label7.text() + "')"
                    cur.execute(query)
                    con.commit()
                    self.label3.hide()
                    self.label6.show()
                    self.label8.hide()
                    self.label7.hide()
                except:
                    self.label7.setText("Something wrong occured")


        #elif button_type == "5" была похоронена

        elif button_type == "6":
            w = Main_Screen.show()
            self.hide()

        elif button_type == "7":
            #print("pressed 7")
            query = "delete from film_favorite where film_id = '" + film_id + "'"
            #print(query)
            cur.execute(query)
            con.commit()
            self.label4.hide()
            self.label1.show()

        elif button_type == "8":
            #print("pressed 8")
            query = "delete from film_watched where film_id = '" + film_id + "'"
            #print(query)
            cur.execute(query)
            con.commit()
            self.label5.hide()
            self.label2.show()

        elif button_type == "9":
            #print("download info")
            path = QFileDialog.getSaveFileName(self, filter="*.txt")
            #print(path)
            file = open(path[0], mode="w")
            file.truncate(0)
            file.write(film_id + "\n" + film_full_title)
            file.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Film_screen()
    ex.show()
    sys.exit(app.exec())