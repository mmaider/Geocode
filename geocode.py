import pygame
import requests
import sys
import os


class Map(object):
    def __init__(self):
        self.lat = 37.653452
        self.lon = 55.721555
        self.z = 11
        self.type = "map"
        self.search_result = None
        self.use_postal_code = False



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
        map_file = load_map(mapp)
        screen.blit(pygame.image.load(map_file), (0, 0))

        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()