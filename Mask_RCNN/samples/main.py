import os
import sys
import matplotlib.pyplot as plt
import warnings
import tensorflow as tf
import cv2
from detector.detector import MotionDetector

physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

ROOT_DIR = os.path.abspath("../")

warnings.filterwarnings("ignore")

sys.path.append(ROOT_DIR)
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize

sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
from samples.coco import coco

'exec(%matplotlib inline)'
# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join('', "mask_rcnn_coco.h5")

# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
# config.display()


# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir='mask_rcnn_coco.hy', config=config)

# Load weights trained on MS-COCO
model.load_weights('mask_rcnn_coco.h5', by_name=True)

# COCO Class names
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


VIDEO_DIR = os.path.join(ROOT_DIR, "data/1.mp4")
vid = cv2.VideoCapture(VIDEO_DIR)
sucsess, image = vid.read()
scale_percent = 50 # Процент от изначального размера
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

detector = MotionDetector(bg_history=20, brightness_discard_level=125, group_boxes=False, expansion_step=5)

res = []

for i in range(0):
    sucsess, image = vid.read()

for i in range(600):
    sucsess, image = vid.read()
    print("Read img №" + str(i))
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    croped = image[400:1500, 50:1200]
    boxes = detector.detect(croped)
    if boxes:
        print("Compute img №" + str(i))
        results = model.detect([resized], verbose=0)
        r = results[0]
        img = visualize.get_instances(resized, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
        #plt.savefig("../../results2/cadr" + str(i))
        cv2.imwrite("../../results2/zone" + str(i)+".png", croped)
        plt.clf()
    #else:
        #cv2.imwrite("../../results2/cadr" + str(i)+".png", image)







