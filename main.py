import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QLabel, QGraphicsView, \
    QGraphicsScene, QWidget, QSizePolicy

import pathlib
import sys
import cv2


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\EditorMenu.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))

        self.load_photo_button = self.findChild(QPushButton, "load_photo_btn")
        self.take_photo_button = self.findChild(QPushButton, "take_photo_btn")
        self.info_label = self.findChild(QLabel, "info_label")
        self.movie = QMovie(f"{pathlib.Path(__file__).parent.absolute()}\\images\\loading.gif")
        self.load_photo_button.clicked.connect(self.load_photo)
        self.take_photo_button.clicked.connect(self.take_photo)
        self.file, self.main_window = None, None

    def load_photo(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png);;All Files (*)")
        if files:
            self.file = files[0]
            self.close()
            self.main_window = Main(self.file)
            self.main_window.show()

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
        self.main_window = Main(f'{pathlib.Path(__file__).parent.absolute()}\\images\\data\\cam.png')
        self.main_window.show()
        # Отключаем камеру
        cap.release()


class Main(QWidget):
    def __init__(self, file):
        super().__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\editor.ui", self)
        self.setWindowTitle("Mega PhotoEditor")
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\images\\icon.ico"))
        self.move(120, 10)

        # Вывод выбранной картинки на экран
        self.img = QPixmap(file)
        self.screen = self.findChild(QGraphicsView, "screen")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img)
        self.screen.setScene(self.scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
