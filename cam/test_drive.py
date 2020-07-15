from IPython.display import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import Xception


from cam.grad_cam import grad_cam
%matplotlib inline

#IMG_PATH = "images/african_elephant.jpg"
IMG_PATH = "https://i.imgur.com/Bvro0YD.png"
SAVE_PATH = 'african_elephant_superimposed.jpg'
IMG_SIZE = (299, 299)

model = Xception(weights='imagenet')
last_conv_layer_name = 'block14_sepconv2_act'
classifier_layer_names = ["avg_pool", "predictions", ]

superimposed_img = grad_cam(IMG_PATH, IMG_SIZE, model, last_conv_layer_name, classifier_layer_names)

img = image.load_img(, target_size=(125, 125))

superimposed_img.save(SAVE_PATH)
display(Image(SAVE_PATH))
#
