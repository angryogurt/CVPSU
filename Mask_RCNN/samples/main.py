import os
import sys
import tracemalloc
import logging
import matplotlib.pyplot as plt
import warnings
import tensorflow as tf
import cv2
import gc
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


VIDEO_DIR = os.path.join(ROOT_DIR, "data/input/6.avi")
vid = cv2.VideoCapture(VIDEO_DIR)
sucsess, image = vid.read()
scale_percent = 50 # Процент от изначального размера
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

detector = MotionDetector(bg_history=20, brightness_discard_level=100, group_boxes=False, expansion_step=5)

X1_CONTROL_ZONE = 150
Y1_CONTROL_ZONE = 400
X2_CONTROL_ZONE = 1300
Y2_CONTROL_ZONE = 900
cz = [Y1_CONTROL_ZONE,X1_CONTROL_ZONE,Y2_CONTROL_ZONE,X2_CONTROL_ZONE]

res = []

start_frame_number = 10801
vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)

counter = 0

HEX_TO_MASK_UNDEFINED = "f5e105"
RGB_TO_MASK_UNDEFINED = tuple(int(HEX_TO_MASK_UNDEFINED[i:i+2], 16) for i in (0, 2, 4))
BGR_TO_MASK_UNDEFINED = [round(RGB_TO_MASK_UNDEFINED[2]/255, 2), round(RGB_TO_MASK_UNDEFINED[1]/255, 2), round(RGB_TO_MASK_UNDEFINED[0]/255, 2)]

HEX_TO_MASK_OUR = "57fa48"
RGB_TO_MASK_OUR = tuple(int(HEX_TO_MASK_OUR [i:i+2], 16) for i in (0, 2, 4))
BGR_TO_MASK_OUR = [round(RGB_TO_MASK_OUR [2]/255, 2), round(RGB_TO_MASK_OUR [1]/255, 2), round(RGB_TO_MASK_OUR [0]/255, 2)]

HEX_TO_MASK_ALIEN = "c90808"
RGB_TO_MASK_ALIEN = tuple(int(HEX_TO_MASK_ALIEN[i:i+2], 16) for i in (0, 2, 4))
BGR_TO_MASK_ALIEN = [round(RGB_TO_MASK_ALIEN[2]/255, 2), round(RGB_TO_MASK_ALIEN[1]/255, 2), round(RGB_TO_MASK_ALIEN[0]/255, 2)]

HEX_TO_CZ_CLEAR = "858585"
RGB_TO_CZ_CLEAR = tuple(int(HEX_TO_CZ_CLEAR[i:i+2], 16) for i in (0, 2, 4))
BGR_TO_CZ_CLEAR = [RGB_TO_CZ_CLEAR[2], RGB_TO_CZ_CLEAR[1], RGB_TO_CZ_CLEAR[0]]

HEX_TO_CZ_DETECT = "57fa48"
RGB_TO_CZ_DETECT = tuple(int(HEX_TO_CZ_DETECT[i:i+2], 16) for i in (0, 2, 4))
BGR_TO_CZ_DETECT = [RGB_TO_CZ_DETECT[2], RGB_TO_CZ_DETECT[1], RGB_TO_CZ_DETECT[0]]

# for i in range(10440, 10704):
#     sucsess, image = vid.read()
#     print("Read img №" + str(i))
#     if sucsess:
#         if counter == 0:
#             croped = image[Y1_CONTROL_ZONE:Y2_CONTROL_ZONE, X1_CONTROL_ZONE:X2_CONTROL_ZONE]
#             boxes = detector.detect(croped)
#             if boxes:
#                 counter = 48
#                 print("Compute img №" + str(i))
#                 results = model.detect([image], verbose=0)
#                 r = results[0]
#                 cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_DETECT, 5)
#                 visualize.display_instances_lite(image, r['rois'], r['masks'], r['class_ids'], class_names, BGR_TO_MASK_UNDEFINED, cz)
#             else:
#                 cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_CLEAR, 5)
#                 visualize.display_image(image)
#         else:
#             counter -= 1
#             print("Compute img №" + str(i))
#             results = model.detect([image], verbose=0)
#             r = results[0]
#             cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_DETECT, 5)
#             visualize.display_instances_lite(image, r['rois'], r['masks'], r['class_ids'], class_names, BGR_TO_MASK_UNDEFINED, cz)
#         plt.savefig("../data/output/allscene/6/cadr" + str(i))
#         plt.clf()

tracemalloc.start()

counter = 1

for i in range(10801, 11280):
    sucsess, image = vid.read()
    print("Read img №" + str(i))
    if sucsess:
        if counter == 0:
            croped = image[Y1_CONTROL_ZONE:Y2_CONTROL_ZONE, X1_CONTROL_ZONE:X2_CONTROL_ZONE]
            boxes = detector.detect(croped)
            if boxes:
                counter = 48
                print("Compute img №" + str(i))
                results = model.detect([image], verbose=0)
                r = results[0]
                cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_DETECT, 5)
                visualize.display_instances_lite(image, r['rois'], r['masks'], r['class_ids'], class_names, BGR_TO_MASK_ALIEN, cz)
            else:
                cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_CLEAR, 5)
                visualize.display_image(image)
        else:
            counter -= 1
            print("Compute img №" + str(i))
            results = model.detect([image], verbose=0)
            r = results[0]
            cv2.rectangle(image, (X1_CONTROL_ZONE, Y1_CONTROL_ZONE), (X2_CONTROL_ZONE, Y2_CONTROL_ZONE), BGR_TO_CZ_DETECT, 5)
            visualize.display_instances_lite(image, r['rois'], r['masks'], r['class_ids'], class_names, BGR_TO_MASK_ALIEN, cz)
        plt.savefig("../data/output/allscene/6/cadr" + str(i))
        plt.clf()

snapshot = tracemalloc.take_snapshot()
for i, stat in enumerate(snapshot.statistics('filename')[:10], 1):
    logging.info("top_current", i=i, stat=str(stat))






