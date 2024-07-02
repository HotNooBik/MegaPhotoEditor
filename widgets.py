"""Файл с классами виджетов-фреймов с функциями редактора"""
import pathlib

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QSlider, QSpinBox
from copy import deepcopy


class DecBrightFrame(QWidget):
    """
    Класс фрейма с кнопкоми, необходимыми для изменения яркости изображения
    """
    def __init__(self, main):
        """
        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        super().__init__()
        # Загружаем ui макет
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\brightness_frame.ui", self)

        # Берем путь до юзер даты из main
        self.USER_DATA_PATH = main.USER_DATA_PATH

        # Инициализируем виджеты данного фрейма для работы с ними
        self.frame = self.findChild(QFrame, "frame")
        self.accept_btn = self.findChild(QPushButton, "accept")
        self.accept_btn.clicked.connect(lambda: self.save_current_image(main))
        self.slider = self.findChild(QSlider, "verticalSlider")
        self.slider.valueChanged.connect(lambda: self.change_brightness(main))

        self.brightness_value = 0

    def change_brightness(self, main):
        """
        Метод, реализующий процесс изменения яркости текущего изображения в редакторе

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        self.brightness_value = -1 * self.slider.value()
        main.current_image = deepcopy(main.original_image)
        main.current_image.change_brightness(self.brightness_value)

        # Сохраняем промежуточное изображение с изменной яркостью в юзер дату
        data_file_path = self.USER_DATA_PATH + "brightness." + main.current_image.img_format
        main.current_image.set_new_path(data_file_path)
        main.current_image.save_image(data_file_path)

        main.update_image()

    def save_current_image(self, main):
        """
        Метод для сохранения изменений яркости изображения

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        try:
            self.frame.setParent(None)
            main.main_vbox.addWidget(main.main_frame)
            main.original_image = deepcopy(main.current_image)
        except Exception as ex:
            print(ex)


class ColorChannelFrame(QWidget):
    """
    Класс фрейма с кнопкоми, необходимыми для просмотра цветовых каналов
    """
    def __init__(self, main):
        """
        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        super().__init__()
        # Загружаем ui макет
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\color_channel_frame.ui", self)

        # Берем путь до юзер даты из main
        self.USER_DATA_PATH = main.USER_DATA_PATH

        # Инициализируем виджеты данного фрейма для работы с ними
        self.frame = self.findChild(QFrame, "frame")
        self.accept_btn = self.findChild(QPushButton, "accept")
        self.accept_btn.clicked.connect(lambda: self.save_current_image(main))
        self.original_btn = self.findChild(QPushButton, "original")
        self.original_btn.clicked.connect(lambda: self.show_color_channel(main))
        self.red_btn = self.findChild(QPushButton, "red")
        self.red_btn.clicked.connect(lambda: self.show_color_channel(main, "red"))
        self.green_btn = self.findChild(QPushButton, "green")
        self.green_btn.clicked.connect(lambda: self.show_color_channel(main, "green"))
        self.blue_btn = self.findChild(QPushButton, "blue")
        self.blue_btn.clicked.connect(lambda: self.show_color_channel(main, "blue"))

    def show_color_channel(self, main, color=""):
        """
        Метод, реализующий процесс показа цветового канала изображения

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
            color (str): цветовой канал, который нужно вывести на экран (red, green или blue иначе оригинал)
        """
        main.current_image = deepcopy(main.original_image)
        if color == "red":
            main.current_image.make_red_channel()
            data_file_path = self.USER_DATA_PATH + "red." + main.current_image.img_format
        elif color == "green":
            main.current_image.make_green_channel()
            data_file_path = self.USER_DATA_PATH + "green." + main.current_image.img_format
        elif color == "blue":
            main.current_image.make_blue_channel()
            data_file_path = self.USER_DATA_PATH + "blue." + main.current_image.img_format
        else:
            data_file_path = main.current_image.img_path

        # Сохраняем промежуточное изображение с цветовым каналом в юзер дату
        main.current_image.set_new_path(data_file_path)
        main.current_image.save_image(data_file_path)

        main.update_image()

    def save_current_image(self, main):
        """
        Метод для сохранения текущего цветового канала

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        try:
            self.frame.setParent(None)
            main.main_vbox.addWidget(main.main_frame)
            main.original_image = deepcopy(main.current_image)
        except Exception as ex:
            print(ex)


class AddingCircleFrame(QWidget):
    """
    Класс фрейма с кнопкоми, необходимыми для добавления красного круга на изображение
    """
    def __init__(self, main):
        """
        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        super().__init__()
        # Загружаем ui макет
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\red_circle_frame.ui", self)

        # Берем путь до юзер даты из main
        self.USER_DATA_PATH = main.USER_DATA_PATH

        # Инициализируем виджеты данного фрейма для работы с ними и меняем максимальное значение у SpinBox исходя из
        # текущего изображения
        self.frame = self.findChild(QFrame, "frame")
        self.accept_btn = self.findChild(QPushButton, "accept")
        self.accept_btn.clicked.connect(lambda: self.save_current_image(main))
        self.reject_btn = self.findChild(QPushButton, "reject")
        self.reject_btn.clicked.connect(lambda: self.return_original_image(main))
        self.x_coord_box = self.findChild(QSpinBox, "x_coord")
        self.x_coord_box.setMaximum(main.current_image.width)
        self.y_coord_box = self.findChild(QSpinBox, "y_coord")
        self.y_coord_box.setMaximum(main.current_image.height)
        self.radius_box = self.findChild(QSpinBox, "radius")
        self.radius_box.setMaximum(main.current_image.height if main.current_image.height > main.current_image.width
                                   else main.current_image.width)
        self.thikness_box = self.findChild(QSpinBox, "thikness")
        self.x_coord_box.valueChanged.connect(lambda: self.show_red_circle(main))
        self.y_coord_box.valueChanged.connect(lambda: self.show_red_circle(main))
        self.radius_box.valueChanged.connect(lambda: self.show_red_circle(main))
        self.thikness_box.valueChanged.connect(lambda: self.show_red_circle(main))

    def show_red_circle(self, main):
        """
        Метод, реализующий процесс показа изображения с красным кругом

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        try:
            main.current_image = deepcopy(main.original_image)
            coords = (self.x_coord_box.value(), self.y_coord_box.value())
            radius = self.radius_box.value()
            thikness = self.thikness_box.value()
            main.current_image.add_red_circle(coords, radius, thikness)

            # Сохраняем промежуточное изображение с красным кругом в юзер дату
            data_file_path = self.USER_DATA_PATH + "redCircle." + main.current_image.img_format
            main.current_image.set_new_path(data_file_path)
            main.current_image.save_image(data_file_path)

            main.update_image()
        except Exception as ex:
            print(ex)

    def save_current_image(self, main):
        """
        Метод для сохранения текущего изображения с красным кругом

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        try:
            self.frame.setParent(None)
            main.main_vbox.addWidget(main.main_frame)
            main.original_image = deepcopy(main.current_image)
        except Exception as ex:
            print(ex)

    def return_original_image(self, main):
        """
        Метод для возвращения изображения в состояние до добавления красного круга

        Args:
            main (EditorWindow): экземпляр класса EditorWindow - окно редактора, где располагается данный фрейм
        """
        try:
            self.frame.setParent(None)
            main.main_vbox.addWidget(main.main_frame)
            main.current_image = deepcopy(main.original_image)
            main.update_image()
        except Exception as ex:
            print(ex)
