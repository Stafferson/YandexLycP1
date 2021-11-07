import sqlite3

from PyQt5.QtSql import QSqlDatabase


class DBClass():

    con = ""
    cur = ""

    def createDB(self):
        #query = "create database yandex_project_1"
        db = QSqlDatabase.addDatabase("QSQLITE")
        #db.setDatabaseName("yandex_project_1.sqlite")
        db.open()

    def connect(self, dbname):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    #def getFilm_fav(self, param):
