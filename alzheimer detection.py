# -*- coding: utf-8 -*-
"""ADPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1piEXoi3g_6-hZFVxizI9RlWrLcd7Dz8Z
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/ultralytics/yolov5  # clone
# %cd yolov5
# %pip install -qr requirements.txt  # install
import torch
import utils
display = utils.notebook_init()  # checks

import torchvision
import torch
import torchvision.models as models
from torchvision import datasets
import yaml
from yaml.loader import SafeLoader
import zipfile
from google.colab import drive
import os
import gc
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from shutil import copyfile
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from utils.general import labels_to_class_weights
#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Install W&B
!pip install -q --upgrade wandb
# Login
import wandb
wandb.login()

from google.colab import drive
drive.mount('/content/drive')

drive.mount('/content/drive/')
zip_ref = zipfile.ZipFile("/content/drive/My Drive/ML/YOLO5Dataset5.zip", 'r')
zip_ref.extractall("/content/tmp")
zip_ref.close()

TRAIN_PATH = '/content/tmp/YOLO5Dataset5/train/images'
IMG_SIZE = 800
BATCH_SIZE = 17
EPOCHS = 50

with open('/content/tmp//data.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)
    print(data)

!python train.py --img {IMG_SIZE} \
                 --batch {BATCH_SIZE} \
                 --epochs {EPOCHS} \
                 --data '/content/tmp/data.yaml' \
                 --weights yolov5s.pt \
                 --cache

#!wandb disabled
#!python train.py --img 416 --batch 16 --epochs 50 --data ../data.yaml --weights yolov5n.pt
#!python train.py --img 640 --batch 64 --epochs 3 --data /kaggle/working/traffic4_in_kaggle.yaml --weights yolov5s.pt

!python val.py --data '/content/tmp/data.yaml' --weights /content/drive/MyDrive/best.pt --batch 64 --task test

!python detect.py --weights /content/drive/MyDrive/best.pt --img 800 --conf 0.6 --source /content/ADNI_002_S_6103_MR_Axial_T2_STAR__br_raw_20171128103507245_22_S638319_I938770_jpg.rf.b6aba0a4f9c59ef515248ed04e17ff8c.jpg

# !pip install tensor

!python /content/yolov5/yolov5/export.py --weights /content/drive/MyDrive/best.pt --img 640 --batch 1

!yolov5.save('model.h5')

# import tensorflow as tf
# model = tf.keras.models.load_model('model.h5')
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()
# open("converted_model.tflite", "wb").write(tflite_model)

# !python export.py --weights /content/drive/MyDrive/best.pt --include tflite --img 640

# import tensorflow as tf

# # Load the TensorFlow model
# model = tf.keras.models.load_model('path/to/model.h5')

# # Convert the model to TensorFlow Lite format
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# tflite_model = converter.convert()

# # Save the TensorFlow Lite model to a file
# with open('model.tflite', 'wb') as f:
#     f.write(tflite_model)

# from PIL import Image
# image = Image.open('/content/drive/MyDrive/ML/images/MildDem--285-_jpg.rf.cdf1489a9f11192e4602575bbee6fde0.jpg')
# new_image = image.resize((640, 640))
# new_image.save('/content/drive/MyDrive/ML/images/000.jpg')

data = torchvision.io.read_image('/content/tmp/YOLO5Dataset2/train/images/26_jpg.rf.b9d70dfa41e9632336bf5ee52675c328.jpg')
data.shape
import matplotlib.pyplot as plt
plt.imshow(data.permute((1,2,0)))
#yolov5s.pt

# import numpy as np

# !reshaped_output = np.reshape(tflite_output, [1, 20, 20, 45])

# !pip install --upgrade tensorflow

# def classFilter(classdata):
#     classes = []  # create a list
#     for i in range(classdata.shape[0]):         # loop through all predictions
#         classes.append(classdata[i].argmax())   # get the best classification location
#     return classes  # return classes (int)

# def YOLOdetect(output_data):  # input = interpreter, output is boxes(xyxy), classes, scores
#     output_data = output_data[0]                # x(1, 25200, 7) to x(25200, 7)
#     boxes = np.squeeze(output_data[..., :4])    # boxes  [25200, 4]
#     scores = np.squeeze( output_data[..., 4:5]) # confidences  [25200, 1]
#     classes = classFilter(output_data[..., 5:]) # get classes
#     # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
#     x, y, w, h = boxes[..., 0], boxes[..., 1], boxes[..., 2], boxes[..., 3] #xywh
#     xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]  # xywh to xyxy   [4, 25200]

#     return xyxy, classes, scores  # output is boxes(x,y,x,y), classes(int), scores(float) [predictions length]

# import tensorflow as tf
# import numpy as np

# # assuming 'tensor' is a TensorFlowLite tensor with shape [1, 25200, 9]
# tensor = np.random.rand(1, 25200, 9)
# new_shape = [1, 20, 20, 45]

# reshaped_tensor = tf.reshape(tensor, new_shape)

# print(reshaped_tensor.shape)

# import numpy as np

# # Assume output_tensor is the output tensor from YOLOv5 model with shape [1, 25200, 9]
# output_tensor = np.zeros((1, 25200, 9))  # Example tensor with all zeros

# # Reshape tensor to [1, 20, 20, 45]
# reshaped_tensor = np.reshape(output_tensor, (1, 20, 20, 45))

# # Transpose tensor to [1, 20, 20, 45] format
# transposed_tensor = np.transpose(reshaped_tensor, (0, 2, 1, 3))

import tensorflow as tf

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="/content/drive/MyDrive/best-fp16.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Resize the output tensor
output_shape = [1, 20, 20, 45]
interpreter.resize_tensor_input(output_details[0]['index'], output_shape)
reshaped_output = np.reshape(output_details[0]['index'], [1, 20, 20, 45])
interpreter.allocate_tensors()

import tensorflow as tf
best_saved_model = "/content/drive/MyDrive/best.pt"
!best_saved_model.save("/content/my_model.h5",save_format="h5")

# # !python export.py --weights /content/drive/MyDrive/best.pt --img-size 640 --export onnx
# import onnx
# !python export.py --weights /content/drive/MyDrive/best.pt  --include torchscript onnx

# !pip install torch==1.9.0+cu102 torchvision==0.10.0+cu102 torchaudio==0.9.0 -f https://download.pytorch.org/whl/cu102/torch_stable.html
# !pip install tensorflow==2.6.0
# !pip install tensorflow-hub==0.12.0
# !pip install tensorflow-text==2.6.0
# !pip install tflite-support==0.2.0

# !pip install onnx==1.13.0

# !pip show onnx

# !pip install onnx_tf

# !python export.py --weights /content/drive/MyDrive/best.pt --include onnx --img-size 640 --batch-size 1

# !pip install onnx onnx_tf tensorflow==2.6.0 tensorflow-addons==0.14.0

# !pip install --upgrade tensorflow

# !pip uninstall tensorflow-probability
# !pip install tensorflow-probability

# !pip install --upgrade tensorflow-probability

# !pip install tensorflow==2.11

# import onnx
# import onnx_tf

# onnx_model = onnx.load('/content/drive/MyDrive/best.onnx')
# tf_graph = onnx_tf.backend.prepare(onnx_model).graph

# !pip install tensorflow==2.7.0
# !pip install tensorflow-addons==0.15.0
# !pip install tensorflow_hub==0.12.0
# !pip install tensorflow-text==2.7.0

# !git clone https://github.com/ultralytics/yolov5

!python yolov5/export.py --weights /content/drive/MyDrive/best.pt --img 640 --batch 1

# import tensorflow as tf

# saved_model_dir = '/content/drive/MyDrive/best_saved_model'
# converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]
# tflite_model = converter.convert()

# # Save the TFLite model to a file
# with open('/content/drive/MyDrive/yolov5.tflite', 'wb') as f:
#     f.write(tflite_model)

# import tensorflow as tf

# # Convert the model
# converter = tf.lite.TFLiteConverter.from_saved_model('/content/drive/MyDrive/best_saved_model') # path to the SavedModel directory
# tflite_model = converter.convert()

# # Save the model.
# with open('model.tflite', 'wb') as f:
#   f.write(tflite_model)

# !python export.py --weights /content/drive/MyDrive/best.pt --include tflite --img 640

!python detect.py --weights /content/drive/MyDrive/best-fp16.tflite --img 800 --conf 0.6 --source /content/drive/MyDrive/ML/test/images

# !python export.py --weights /content/drive/MyDrive/best.pt --include torchscript --img 640 --optimize

!zip -r /content/yolov5/exp29.zip /content/yolov5/runs/detect/exp/labels

import glob
from IPython.display import Image, display

for imageName in glob.glob('/content/yolov5/runs/detect/exp9*.jpg'): #assuming JPG
    display(Image(filename=imageName))
    print("\n")

import torch
import torchvision.models as models

# yolov5 = models.vgg16(pretrained=True)
torch.save(yolov5.state_dict(), 'content/drive/MyDrive/grauationProject.pth')

# import tensorflow
# from tensorflow import keras
# from tensorflow.keras.models import load_model
# model.save()

# !pip install tensorflow-addons==0.8.3
# !pip install tensorflow==2.2.0-rc3

!pip install onnx

!pip install tensorflow-addons

!pip install onnx-tf

import tensorflow as tf
import tensorflow_addons as tfa
import onnx
import onnx_tf
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
# Load the ONNX model
#model = onnx.load('/content/drive/MyDrive/best_saved_model/saved_model.pb')
#!model.save("/content/my_model.h5", save_format='h5')

New_Model = tf.keras.models.load_model('/content/drive/MyDrive/best_saved_model')

#my_model = load_model('/content/drive/MyDrive/savemodel/model.h5')
print(New_Model.summary())
# Convert the model to TensorFlow format
# tf_rep = onnx_tf.backend.prepare(model)
# tf_rep = prepare(onnx_model)



print(tf_rep)

!pip install tensorflow-addons

import tensorflow as tf
import tensorflow_addons as tfa
import onnx
import onnx_tf
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image

New_Model = tf.keras.models.load_model('/content/model.pb')
keras_model = models.convert_model(loaded_model)
#tf.keras.models.save_model(New_Model, 'best.h5', save_format='h5')

import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image

pb_model_dir = "/content/model.pb/saved_model.pb"
#h5_model = "/content/drive/MyDrive/savemodel"

# Loading the Tensorflow Saved Model (PB)
tf.keras.models.save_model(model, 'my_model.h5')

m = '/content/drive/MyDrive/best.onnx'
torch.save(m, '/content/model')

!pip install onnx
!pip install torch

!pip install onnx2pytorch

model = '/content/drive/MyDrive/best.onnx'

import onnx
!python export.py --weights /content/drive/MyDrive/best.pt  --include torchscript h5

import tensorflow as tf
from tensorflow.keras.models import save_model, Sequential

model_path = r"/content/model.pb/saved_model.pb"

model = tf.keras.models.load_model(model_path)