import pathlib

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QSlider
from image import Image
from copy import deepcopy


class DecBrightFrame(QWidget):
    def __init__(self, main):
        super().__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\brightness_box.ui", self)

        self.USER_DATA_PATH = main.USER_DATA_PATH

        self.frame = self.findChild(QFrame, "frame")
        self.accept_btn = self.findChild(QPushButton, "accept")
        self.accept_btn.clicked.connect(lambda: self.save_current_image(main))
        self.slider = self.findChild(QSlider, "verticalSlider")
        self.slider.valueChanged.connect(lambda: self.change_brightness(main))
        self.brightness_value = 0

    def change_brightness(self, main):
        self.brightness_value = -1 * self.slider.value()
        main.current_image = deepcopy(main.original_image)
        main.current_image.decrease_brightness(self.brightness_value)
        data_file_path = self.USER_DATA_PATH + "brightness." + main.current_image.img_format
        main.current_image.set_new_path(data_file_path)
        main.current_image.save_image(data_file_path)
        main.update_image()

    def save_current_image(self, main):
        try:
            self.frame.setParent(None)
            main.main_vbox.addWidget(main.main_frame)
            main.original_image = deepcopy(main.current_image)
        except Exception as ex:
            print(ex)

