import cv2
import numpy as np

K_MIN = 3.0
K_MAX = 4.0
P_MIN = 200
P_MAX = 600
ANGLE_STEP = 0.1
LEFT_ANGLE_RANGE = -10
RIGHT_ANGLE_RANGE = 10
SPEED = 25

def getTranslationMatrix2d(dx, dy):
    return np.matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])


def rotateImage(image, angle):
    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(np.array(image_size) / 2)
    rot_mat = np.vstack([cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]])
    trans_mat = np.identity(3)
    w2 = image_size[0] * 0.5
    h2 = image_size[1] * 0.5
    rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])
    tl = (np.array([-w2, h2]) * rot_mat_notranslate).A[0]
    tr = (np.array([w2, h2]) * rot_mat_notranslate).A[0]
    bl = (np.array([-w2, -h2]) * rot_mat_notranslate).A[0]
    br = (np.array([w2, -h2]) * rot_mat_notranslate).A[0]
    x_coords = [pt[0] for pt in [tl, tr, bl, br]]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]
    y_coords = [pt[1] for pt in [tl, tr, bl, br]]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]
    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)
    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))
    new_image_size = (new_w, new_h)
    new_midx = new_w * 0.5
    new_midy = new_h * 0.5
    dx = int(new_midx - w2)
    dy = int(new_midy - h2)
    trans_mat = getTranslationMatrix2d(dx, dy)
    affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]
    result = cv2.warpAffine(image, affine_mat, new_image_size, flags=cv2.INTER_LINEAR)
    return result


image = cv2.imread("data/test1.jpg")
#vid = cv2.VideoCapture("data/2/2.mp4")
#sucsess, image = vid.read()

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
screen_res = 1920, 1080
scale_width = screen_res[0] / image.shape[1]
scale_height = screen_res[1] / image.shape[0]
scale = min(scale_width, scale_height)
window_width = int(image.shape[1] * scale)
window_height = int(image.shape[0] * scale)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)

while True:
    #sucsess, image = vid.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, board = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY)
    board = cv2.GaussianBlur(board, (5, 5), 0)
    _, founded_board, topology = cv2.findContours(board, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for countur in founded_board:
        peri = cv2.arcLength(countur, True)
        approx = cv2.approxPolyDP(countur, 0.02 * peri, True)
        if len(approx) == 4:
            retval = cv2.boundingRect(approx)
            k = retval[2] / retval[3]
            if (K_MIN <= k) and (k <= K_MAX) and (peri>P_MIN) and (peri<P_MAX):
                cv2.drawContours(image, [countur], -1, (150, 255, 100), 3)
                print(k)
    try:
        cv2.imshow('image', image)
    except:
        vid.release()
        raise
    ch = cv2.waitKey(5)
    if ch == 27:
        break
vid.release()
cv2.destroyAllWindows()
