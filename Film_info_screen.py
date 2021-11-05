import json
import sys
import urllib
from pprint import pprint

import requests
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

film_full_title = ""
search_type = -1

film_id = ""
film_imdb_rating = ""
film_imdb_rating_count = ""
film_image_url = ""
film_title = ""
film_ = ""

class Film_screen(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global film_full_title
        global search_type

        super(Film_screen, self).__init__()
        self.setGeometry(0, 0, 1500, 1000)
        self.setWindowTitle("Films App")

        print(film_full_title)
        print(search_type)

        api_link = "https://imdb-api.com/en/API/SearchMovie/k_907znyrc/" + film_full_title
        #self.get_info(search_type, film_title, api_link)
        print(api_link)

        response = requests.get(api_link)
        film_dict = json.loads(response.text)
        pprint(film_dict)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Film_screen()
    ex.show()
    sys.exit(app.exec())