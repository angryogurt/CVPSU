import cv2

img_array = []

for i in range(600):
    filename = "../../results/cadr"+str(i)+".png"
    print(filename)
    img = cv2.imread(filename)
    img = img[462:1154, 206:1435]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

out = cv2.VideoWriter('../../results/project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, size)

for i in range(len(img_array)):
    out.write(img_array[i])