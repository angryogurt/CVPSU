try:
    import Image
except ImportError:
    from PIL import Image
import cv2

K_MIN = 2.0
K_MAX = 5.0

image = cv2.imread("data/test.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
board = cv2.Canny(image, 10, 250)
board = image
_, founded_board_image, topology = cv2.findContours(board, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for countur in founded_board_image:
    peri = cv2.arcLength(countur, True)
    approx = cv2.approxPolyDP(countur, 0.02*peri, True)
    if len(approx) == 4:
        retval = cv2.boundingRect(approx)
        k = retval[2]/retval[3]
        if (K_MIN <= k) and (k <= K_MAX):
            cv2.drawContours(image, [countur], -1, (150, 255, 100), 3)
            print(k)
cv2.imshow('image', image)
cv2.waitKey(200000)
