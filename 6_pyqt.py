import requests
import sys
import os
import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap

lat_step = 0.008
lon_step = 0.002
coords_to_geo_x = 0.0000428
coords_to_geo_y = 0.0000428


class Map(QWidget):
    def __init__(self, *names):
        super().__init__()
        self.initUI()

        self.lat = 37.653452
        self.lon = 55.721555
        self.z = 11
        self.type = "map"
        self.search_result = None
        self.use_postal_code = False
        self.name = "map.png"
        self.pixmap = QPixmap(self.name)
        self.label.setPixmap(self.pixmap)
        self.load_map()
        self.show()

    def initUI(self):
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Задача 6')
        self.label = QLabel(self)
        self.label.resize(600, 450)
        self.label.move(0, 150)
        self.label.setFocusPolicy(Qt.StrongFocus)

        self.name_input = QLineEdit(self)
        self.name_input.move(10, 10)
        self.point = ''

        self.btn = QPushButton('Искать', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)
        self.btn.clicked.connect(self.add_point)

    def add_point(self):
        address = self.name_input.text()
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": address,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        coodrinates = toponym["Point"]["pos"]
        x, y = coodrinates.split()
        if self.point == '':
            self.point = '&pt={},{},pm2rdm'.format(x, y)
        else:
            self.point += '~{},{},pm2rdm'.format(x, y)
        self.lat = float(x)
        self.lon = float(y)
        self.load_map()

    def screen_to_geo(self, pos):
        dy = 255 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx + coords_to_geo_x * math.pow(2, 15 - self.z)
        ly = self.lat + dy + coords_to_geo_y * math.cos(math.radians(self.lat) * math.pow(2, 15 - self.z))
        return lx, ly

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.z < 19:
            self.z += 1
        if event.key() == Qt.Key_PageDown and self.z > 1:
            self.z -= 1
        if event.key() == Qt.Key_Left:
            self.lat -= lat_step * math.pow(2, 15 - self.z)
        if event.key() == Qt.Key_Right:
            self.lat += lat_step * math.pow(2, 15 - self.z)
        if event.key() == Qt.Key_Up:
            self.lon += lon_step * math.pow(2, 15 - self.z)
        if event.key() == Qt.Key_Down:
            self.lon -= lon_step * math.pow(2, 15 - self.z)
        if event.key() == Qt.Key_1:
            self.type = 'map'
            os.remove(self.name)
            self.name = "map.png"
        if event.key() == Qt.Key_2:
            self.type = 'sat'
            os.remove(self.name)
            self.name = "map.jpg"
        if event.key() == Qt.Key_3:
            self.type = 'sat%2Cskl'
            os.remove(self.name)
            self.name = "map.jpg"
        self.load_map()

    def closeEvent(self, QCloseEvent):
        self.close()
        os.remove(self.name)

    def load_map(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&z={z}&l={type}{pt}".format(
            self.lat, self.lon, z=self.z, type=self.type, pt=self.point)
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit()
        try:
            with open(self.name, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        self.pixmap = QPixmap(self.name)
        self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mapp = Map()
    sys.exit(app.exec_())
