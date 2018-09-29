import cv2
import video
cap = video.create_capture(0)
while True:
    K_MIN = 2.0
    K_MAX = 5.0
    P_MIN = 500
    P_MAX = 1200
    flag, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    board = cv2.Canny(gray, 10, 250)
    board = gray
    ret, result = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    _, board, topology = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for countur in board:
        peri = cv2.arcLength(countur, True)
        approx = cv2.approxPolyDP(countur, 0.02 * peri, True)
        if len(approx) == 4:
            retval = cv2.boundingRect(approx)
            k = retval[2] / retval[3]
            if (K_MIN <= k) and (k <= K_MAX) and (peri>P_MIN) and (peri<P_MAX):
                cv2.drawContours(image, [countur], -1, (0, 255, 0), 3)
                resource = image
                output = open("file01.jpg", "wb")
                output.write(resource)
                output.close()
                exit(0)
    try:
        cv2.imshow('image', image)
    except:
        cap.release()
        raise
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cap.release()
cv2.destroyAllWindows()
