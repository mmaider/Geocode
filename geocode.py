import pygame
import requests
import sys
import os
import math

lat_step = 0.008
lon_step = 0.002
coords_to_geo_x = 0.0000428
coords_to_geo_y = 0.0000428


class Map(object):
    def __init__(self):
        self.lat = 37.653452
        self.lon = 55.721555
        self.z = 11
        self.type = "map"
        self.search_result = None
        self.use_postal_code = False

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP and self.z < 19:
                self.z += 1
            if event.key == pygame.K_PAGEDOWN and self.z > 1:
                self.z -= 1
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.lat -= lat_step * math.pow(2, 15 - self.z)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.lat += lat_step * math.pow(2, 15 - self.z)
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.lon += lon_step * math.pow(2, 15 - self.z)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.lon -= lon_step * math.pow(2, 15 - self.z)

    def screen_to_geo(self, pos):
        dy = 255 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx + coords_to_geo_x * math.pow(2, 15 - self.z)
        ly = self.lat + dy + coords_to_geo_y * math.cos(math.radians(self.lat) * math.pow(2, 15 - self.z))
        return lx, ly


def load_map(mapp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&z={z}&l={type}".format(mapp.lat, mapp.lon, z=mapp.z,
                                                                                     type=mapp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit()
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mapp = Map()
    while pygame.event.wait().type != pygame.QUIT:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        mapp.update(event)
        map_file = load_map(mapp)
        screen.blit(pygame.image.load(map_file), (0, 0))

        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()