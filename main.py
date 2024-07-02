""" Точка старта программы"""
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QGraphicsView, \
    QGraphicsScene, QWidget, QFrame, QVBoxLayout
from image import Image
from widgets import DecBrightFrame, ColorChannelFrame, AddingCircleFrame
from PIL import Image as Images
from copy import deepcopy

import pathlib
import sys
import cv2
import datetime
import os


class StartWindow(QMainWindow):
    """
    Стартовое окно, появляющееся при запуске программы и предлагающее выбрать фото для редактирования, данное фото
    можно загрузить (указав путь до файла) или получить, сделав снимок с веб камеры пользователя.
    """
    def __init__(self):
        super().__init__()

        # Загружаем ui макет стартового окна и устанавливаем иконку приложения
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\start_menu.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))

        # Загружаем кнопку загрузки фото и кнопку для того, чтобы сделать снимок с камеры
        self.load_photo_button = self.findChild(QPushButton, "load_photo_btn")
        self.load_photo_button.clicked.connect(self.load_photo)
        self.take_photo_button = self.findChild(QPushButton, "take_photo_btn")
        self.take_photo_button.clicked.connect(self.take_photo)

        self.photo_file, self.main_window = None, None

    def load_photo(self):
        """
        Метод для загрузки выбранного пользователем изображения (путем указания пути до файла) и перехода
        к его редактированию.
        """
        # Открываем окно с выбором файлов-фотографий
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png)")
        if files:
            self.photo_file = files[0]
            try:
                # Проверка на то, чтобы данный файл не оказался битым или пустым (если данная строка не сработает,
                # то выдаст ошибку)
                Images.open(self.photo_file)

                # Запуск основного окна приложения - редактора
                self.close()
                current_date = datetime.date.today().isoformat()
                if current_date == "1995-10-04":
                    self.main_window = EditorWindow(f"{pathlib.Path(__file__).parent.absolute()}\\images\\Rei.jpg")
                else:
                    self.main_window = EditorWindow(self.photo_file)
                self.main_window.show()
            except Exception as ex:
                # Создаем и вызываем окно с сообщением об ошибке
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Произошла ошибка при загрузке фото!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setInformativeText("Возможно данный файл был поврежден.\n\n"+str(ex))
                error.exec_()

    def take_photo(self):
        """
        Метод для получения изображения с веб камеры пользователя и перехода к его редактированию
        """
        # Включаем первую камеру
        cap = cv2.VideoCapture(0)

        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(10):
            cap.read()

        # Делаем снимок
        result = cap.read()

        # Проверяем, получили ли мы фото с вебкамеры
        if not result[0]:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Произошла ошибка при работе с вебкамерой!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Проверьте, подключена ли камера к компьютеру.")
            error.exec_()
        else:
            path = f'{pathlib.Path(__file__).parent.absolute()}\\images\\data'
            # Записываем в файл
            cv2.imwrite(os.path.join(path, 'cam.png'), result[1])

        self.close()
        self.main_window = EditorWindow(f'{pathlib.Path(__file__).parent.absolute()}\\images\\data\\cam.png')
        self.main_window.show()
        # Отключаем камеру
        cap.release()


class EditorWindow(QWidget):
    """
    Класс окна-редактора, где пользователь может увидеть изображение и отредактировать его
    """
    def __init__(self, photo_file: str):
        """
        Args:
            photo_file (str): путь до изображения, открытого для редактирования
        """
        super().__init__()
        # Загружаем ui макет стартового окна, устанавливаем иконку приложения и его название
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\editor.ui", self)
        self.setWindowTitle("Mega PhotoEditor")
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))
        self.move(120, 10)

        # Создаем путь сохранения юзер даты (всех промежуточных изображений, создаваемых во время редактирования)
        self.USER_DATA_PATH = f"{pathlib.Path(__file__).parent.absolute()}\\images\\data\\"

        # Создаем экземпляр класса Image для работы с полученным фото, original_image необходим для возвращения к
        # исходной фотографии после отмены изменений
        self.current_image = Image(photo_file)
        self.original_image = Image(photo_file)

        # Вывод выбранной картинки на экран
        self.img_pixmap = QPixmap(photo_file)
        self.screen = self.findChild(QGraphicsView, "screen")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img_pixmap)
        self.screen.setScene(self.scene)

        # Кнопка выхода в меню
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back_to_menu)

        # Кнопка сохранения фотографии
        self.save_btn = self.findChild(QPushButton, "save")
        self.save_btn.clicked.connect(self.save_action)

        # Кнопка для просмотра цветового канала
        self.color_channel_btn = self.findChild(QPushButton, "color_channel")
        self.color_channel_btn.clicked.connect(self.color_channel_frame)

        # Кнопка для просмотра негатива
        self.negative_btn = self.findChild(QPushButton, "negative")
        self.negative_btn.clicked.connect(self.negative_img_update)

        # Кнопка для уменьшения яркости
        self.dec_bright_btn = self.findChild(QPushButton, "low_brightness")
        self.dec_bright_btn.clicked.connect(self.decrease_brightness_frame)

        # Кнопка для добавления красного круга
        self.add_circle_btn = self.findChild(QPushButton, "add_circle")
        self.add_circle_btn.clicked.connect(self.add_circle_frame)

        # Фрейм с кнопками основных функций
        self.main_frame = self.findChild(QFrame, "frame")
        self.editor_vbox = self.findChild(QVBoxLayout, "vbox4")

        # Основной layout редактора, где располагается фрейм с кнопками основных функций (кроме кнопки back_to_menu)
        self.main_vbox = self.findChild(QVBoxLayout, "vbox1")

        self.menu_window = None

    def back_to_menu(self):
        """
        Метод, возвращающий пользователя в стартовое окно для повторного выбора фото
        """
        self.close()
        self.menu_window = StartWindow()
        self.menu_window.show()

    def save_action(self):
        """
        Метод для сохранения отредактированной фотографии
        """
        try:
            file, _ = QFileDialog.getSaveFileName(self, 'Save File', f"{self.current_image.img_name}."
                                                                     f"{self.current_image.img_format}",
                                                  "Image Files (*.jpg *.png)")
            self.current_image.save_image(file)
            success = QMessageBox()
            success.setWindowTitle("Успешно")
            success.setText("Фотография была успешно сохранена!")
            success.setIcon(QMessageBox.Information)
            success.setStandardButtons(QMessageBox.Ok)
            success.exec_()
        except Exception as ex:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Произошла ошибка при сохранении файла!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Возможно при сохранении файла было указано неверное расширение файла. "
                                     "Нужно png или jpg.")
            error.exec_()

    def color_channel_frame(self):
        """
        Метод для замены фрейма с основными кнопками на фрейм с кнопками для просмотра цветовых каналов
        """
        try:
            color_channel_frame = ColorChannelFrame(self)
            self.main_frame.setParent(None)
            self.main_vbox.addWidget(color_channel_frame.frame)
        except Exception as ex:
            print(ex)

    def negative_img_update(self):
        """
        Метод для замены текущего изображения, отображаемой в редакторе, на негатив этого изображения
        """
        try:
            self.current_image.make_negative()
            data_file_path = self.USER_DATA_PATH + "negative." + self.current_image.img_format
            self.current_image.set_new_path(data_file_path)
            self.current_image.save_image(data_file_path)
            self.update_image()
            self.original_image = deepcopy(self.current_image)
        except Exception as ex:
            print(ex)

    def decrease_brightness_frame(self):
        """
        Метод для замены фрейма с основными кнопками на фрейм с кнопками для изменения яркости изображения
        """
        try:
            decrease_brightness_frame = DecBrightFrame(self)
            self.main_frame.setParent(None)
            self.main_vbox.addWidget(decrease_brightness_frame.frame)
        except Exception as ex:
            print(ex)

    def add_circle_frame(self):
        """
        Метод для замены фрейма с основными кнопками на фрейм с кнопками для добавления красного круга на изображение
        """
        try:
            adding_circle_frame = AddingCircleFrame(self)
            self.main_frame.setParent(None)
            self.main_vbox.addWidget(adding_circle_frame.frame)
        except Exception as ex:
            print(ex)

    def update_image(self):
        """
        Метод для обновления текущего изображения, находящегося в окне редактора, на изображение с примененными
        эффектами и изменениями
        """
        try:
            self.scene.removeItem(self.scene_img)
            self.img_pixmap = QPixmap(self.current_image.img_path)
            self.scene_img = self.scene.addPixmap(self.img_pixmap)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    # Создание приложения и вывод на экран стартового окна
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
