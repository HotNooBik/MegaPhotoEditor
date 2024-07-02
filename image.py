"""Файл с классом изображения"""
import cv2
import numpy


class Image:
    """
    Самостоятельно созданный класс для изображений, содержащий функции, необходимые для пунктов меню редактор
    """
    def __init__(self, file: str):
        """
        Args:
            file (str): путь до изображения, открытого для редактирования
        """
        # Текущее изображение, которое будет редактироваться
        self.img = cv2.imdecode(numpy.fromfile(file, dtype=numpy.uint8), -1)
        self.img_name = file.split("\\")[-1][0:file.split("\\")[-1].rfind('.')]
        self.img_format = file.split("\\")[-1][file.split("\\")[-1].rfind('.')+1:]
        self.img_path = file
        self.height, self.width, _ = self.img.shape

    def set_new_path(self, file: str):
        """
        Метод для установления нового пути до файла изображения

        Args:
            file (str): новый путь до изображения
        """
        self.img_name = file.split("\\")[-1][0:file.split("\\")[-1].rfind('.')]
        self.img_format = file.split("\\")[-1][file.split("\\")[-1].rfind('.') + 1:]
        self.img_path = file

    def save_image(self, file: str):
        """
        Метод для сохранения фотографии по переданному пути

        Args:
            file (str): путь, в котором будет сохранено изображение
        """
        img_format = "." + file.split("\\")[-1][file.split("\\")[-1].rfind('.') + 1:]
        cv2.imencode(img_format, self.img)[1].tofile(file)

    def make_negative(self):
        """
        Метод, делающий текущее изображение негативным
        """
        self.img = cv2.bitwise_not(self.img)

    def change_brightness(self, value: int):
        """
        Метод, изменяющий яркость текущего изображения

        Args:
            value (int): величина, на которую нужно изменить яркость изображения (от 255 до -255)
        """
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        self.img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    def make_red_channel(self):
        """
        Метод, превращающий текущее изображение в его красный канал
        """
        self.img[:, :, 0] = 0
        self.img[:, :, 1] = 0

    def make_green_channel(self):
        """
        Метод, превращающий текущее изображение в его зеленый канал
        """
        self.img[:, :, 0] = 0
        self.img[:, :, 2] = 0

    def make_blue_channel(self):
        """
        Метод, превращающий текущее изображение в его синий канал
        """
        self.img[:, :, 1] = 0
        self.img[:, :, 2] = 0

    def add_red_circle(self, coords: tuple, radius: int, thikness: int):
        """
        Метод, добавляющий красный круг на текущее изображение

        Args:
            coords (tuple): кортеж, содержащий координаты центра круга (X,Y) в пикселях
            radius (int): радиус круга в пикселях
            thikness (int): толщина линии окружности в пикселях
        """
        cv2.circle(self.img, coords, radius, (0, 0, 255), thikness)
