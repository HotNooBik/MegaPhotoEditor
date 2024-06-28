import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QLabel, QGraphicsView, \
    QGraphicsScene, QWidget
from image import Image
from PIL import Image as Images

import pathlib
import sys
import cv2


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\EditorMenu.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))

        # Загружаем виджеты
        self.load_photo_button = self.findChild(QPushButton, "load_photo_btn")
        self.load_photo_button.clicked.connect(self.load_photo)
        self.take_photo_button = self.findChild(QPushButton, "take_photo_btn")
        self.take_photo_button.clicked.connect(self.take_photo)

        self.photo_file, self.main_window = None, None

    def load_photo(self):
        # Открываем окно с выбором файлов
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png)")
        if files:
            self.photo_file = files[0]
            try:
                # Проверка на то, чтобы данный файл не оказался битым или пустым
                Images.open(self.photo_file)
                # Запуск основного рабочего экрана - редактора
                self.close()
                self.main_window = EditorWindow(self.photo_file)
                self.main_window.show()
            except Exception as ex:
                print("Ошибка!")
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Произошла ошибка при загрузке фото!")
                error.setIcon(QMessageBox.Warning)
                error.setStandardButtons(QMessageBox.Ok)
                error.setInformativeText(str(ex))
                error.exec_()

    def take_photo(self):
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
    def __init__(self, photo_file):
        super().__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\editor.ui", self)
        self.setWindowTitle("Mega PhotoEditor")
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))
        self.move(120, 10)

        # Вывод выбранной картинки на экран
        self.img_pixmap = QPixmap(photo_file)
        self.image = Image(photo_file)
        self.screen = self.findChild(QGraphicsView, "screen")
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.img_pixmap)
        self.screen.setScene(self.scene)

        # Кнопка выхода в меню
        self.back_btn = self.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back_to_menu)

        # Кнопка сохранения фотографии
        self.save_btn = self.findChild(QPushButton, "save")
        self.save_btn.clicked.connect(self.save_photo)

        self.menu_window = None

    def back_to_menu(self):
        self.close()
        self.menu_window = StartWindow()
        self.menu_window.show()

    def save_photo(self):
        try:
            print("доход")
            file, _ = QFileDialog.getSaveFileName(self, 'Save File', f"{self.image.img_name}."
                                                                     f"{self.image.img_format}",
                                                  "Image Files (*.jpg *.png);;All Files (*)")
            self.image.save_image(file)
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
            error.setInformativeText(str(ex))
            error.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
