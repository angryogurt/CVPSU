import cv2
import os
from matplotlib import pyplot as plt


def testPrepare(pathToVideo, pathToSave):
    vid = cv2.VideoCapture(pathToVideo)
    sucsess, image = vid.read()
    scale_percent = 20  # Процент от изначального размера
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    X1_CONTROL_ZONE = 150
    Y1_CONTROL_ZONE = 400
    X2_CONTROL_ZONE = 1300
    Y2_CONTROL_ZONE = 900
    for i in range(1):
        sucsess, image = vid.read()
        plt.imshow(image)
        plt.savefig(os.path.join(pathToSave, "standart.png"))
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        plt.imshow(resized)
        plt.savefig(os.path.join(pathToSave, "resized.png"))
        croped = image[Y1_CONTROL_ZONE:Y2_CONTROL_ZONE, X1_CONTROL_ZONE:X2_CONTROL_ZONE]
        plt.imshow(croped)
        plt.savefig(os.path.join(pathToSave, "croped.png"))
        resized_display_CZ = resized
        cv2.rectangle(resized_display_CZ,
                      (int(X1_CONTROL_ZONE * width / image.shape[1]), int(Y1_CONTROL_ZONE * height / image.shape[0])),
                      (int(X2_CONTROL_ZONE * width / image.shape[1]), int(Y2_CONTROL_ZONE * height / image.shape[0])),
                      (255, 0, 0), 2)
        plt.imshow(resized_display_CZ)
        plt.savefig(os.path.join(pathToSave, "resized_display_CZ.png"))


def convertVideo(pathToVideo, cadrNum, pathToSave, cadrPassNum=0):
    vid = cv2.VideoCapture(pathToVideo)
    sucsess, image = vid.read()
    height, width, layers = image.shape
    size = (width, height)
    out = cv2.VideoWriter(pathToSave, cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
    for i in range(cadrPassNum):
        sucsess, image = vid.read()
    # print('Pass '+str(cadrPassNum)+" cadr's")
    for i in range(cadrNum):
        # print('Convert cadr №'+ str(i))
        sucsess, image = vid.read()
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        out.write(image)


def makevideo(pathToCadrs, cadrStart, cadrStop, pathToSave):
    img = cv2.imread(pathToCadrs+"/cadr"+str(cadrStart)+".png")
    img = img[462:1154, 206:1435]
    height, width, layers = img.shape
    size = (width, height)
    out = cv2.VideoWriter(pathToSave, cv2.VideoWriter_fourcc(*'mp4v'), 24, size)
    for i in range(cadrStart, cadrStop):
        filename = pathToCadrs + "/cadr" + str(i) + ".png"
        print(filename)
        img = cv2.imread(filename)
        img = img[462:1154, 206:1435]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        out.write(img)


# for i in range(8):
#     # ROOT_DIR = os.path.abspath("../")
#     # VIDEO_DIR = os.path.join(ROOT_DIR, "data/input/2.mp4")
#     # SAVE_DIR = os.path.join(ROOT_DIR,"data/output/video/1_6.avi")
#     VIDEO_DIR = os.path.abspath("../data/input/"+str(i+1)+".mp4")
#     SAVE_DIR = os.path.abspath("../data/output/video/"+str(i+1)+".avi")
#     convertVideo(VIDEO_DIR, 50000, SAVE_DIR)
#     print("File №"+str(i+1)+" converted")

CADRS_DIR = os.path.abspath("../data/output/allscene/6/")
SAVE_DIR = os.path.abspath("../data/output/video/6_3.mp4")
makevideo(CADRS_DIR, 31368, 31799, SAVE_DIR)
