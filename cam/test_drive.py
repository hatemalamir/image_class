from IPython.display import Image
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import Xception

from cam.grad_cam import grad_cam
%matplotlib inline

MODEL_PATH = '../xception_model_ft.h5'
IMG_PATH = 'n9065.jpg'
SAVE_PATH = IMG_PATH.split('.')[0] + '_cam.jpg'
IMG_SIZE = (299, 299)

#model = Xception(weights='imagenet')
model = load_model(MODEL_PATH)
model.summary()
last_conv_layer_name = 'block14_sepconv2_act'
classifier_layer_names = ['global_average_pooling2d_1', 'dense_1', 'dense_2']

superimposed_img = grad_cam(IMG_PATH, IMG_SIZE, model, last_conv_layer_name, classifier_layer_names)

superimposed_img.save(SAVE_PATH)
display(Image(SAVE_PATH))
#
