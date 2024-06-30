import cv2
import numpy


class Image:
    def __init__(self, file: str):
        self.img = cv2.imdecode(numpy.fromfile(file, dtype=numpy.uint8), -1)

        self.img_name = file.split("\\")[-1][0:file.split("\\")[-1].rfind('.')]
        self.img_format = file.split("\\")[-1][file.split("\\")[-1].rfind('.')+1:]
        self.img_path = file

    def set_new_path(self, file: str):
        self.img_name = file.split("\\")[-1][0:file.split("\\")[-1].rfind('.')]
        self.img_format = file.split("\\")[-1][file.split("\\")[-1].rfind('.') + 1:]
        self.img_path = file

    def save_image(self, file: str):
        img_format = "." + file.split("\\")[-1][file.split("\\")[-1].rfind('.') + 1:]
        cv2.imencode(img_format, self.img)[1].tofile(file)

    def make_negative(self):
        self.img = cv2.bitwise_not(self.img)

    def decrease_brightness(self, value: int):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        self.img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)


if __name__ == "__main__":
    image = Image(f'C:\\Users\\maksi\\Desktop\\MegaPhotoEditor\\images\\data\\cam.png')
    print(image.img_name, image.img_format)
    while True:
        value = int(input("Введите значение: "))
        image.decrease_brightness(value)