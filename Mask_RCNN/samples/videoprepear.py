import cv2
import os
from matplotlib import pyplot as plt

ROOT_DIR = os.path.abspath("../")
VIDEO_DIR = os.path.join(ROOT_DIR, "data/1.mp4")
vid = cv2.VideoCapture(VIDEO_DIR)

sucsess, image = vid.read()

scale_percent = 20 # Процент от изначального размера
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

for i in range(1):
    sucsess, image = vid.read()
    plt.imshow(image)
    plt.savefig("standart")
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    plt.imshow(resized)
    plt.savefig("resized")
    croped = image[400:1500, 50:1200]
    plt.imshow(croped)
    plt.savefig("croped")
