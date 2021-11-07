from PyQt5.QtSql import QSqlDatabase


class DBClass():
    def createDB(self):
        #query = "create database yandex_project_1"
        db = QSqlDatabase.addDatabase("QSQLITE")
        #db.setDatabaseName("yandex_project_1.sqlite")
        db.open()