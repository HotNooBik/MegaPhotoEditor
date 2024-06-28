import cv2


class Image():
    def __init__(self, file: str):
        self.img = cv2.imread(file)

        self.img_name = file.split("\\")[-1][0:file.split("\\")[-1].rfind('.')]
        self.img_format = file.split("\\")[-1][file.split("\\")[-1].rfind('.')+1:]

    def save_image(self, file: str):
        cv2.imwrite(file, self.img)


if __name__ == "__main__":
    image = Image(f'C:\\Users\\maksi\\Desktop\\MegaPhotoEditor\\images\\data\\cam.png')
    print(image.img_name, image.img_format)