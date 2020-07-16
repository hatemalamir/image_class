import numpy as np
from matplotlib import cm
from io import BytesIO
from urllib.request import urlopen
from tensorflow import GradientTape, argmax, reduce_mean
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from tensorflow.keras import Model, Input
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
from tensorflow.keras.applications.xception import preprocess_input, decode_predictions

# configure tensorflow gpu session
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


def grad_cam(img_path, size, model, last_conv_layer_name, classifier_layer_names):
    img_arr = get_img_array(img_path, size)
    heatmap = make_gradcam_heatmap(img_arr, model, last_conv_layer_name, classifier_layer_names)
    orig_img_arr = img_to_array(load_img(img_path, target_size=size))
    superimposed_image = create_superimposed_image(orig_img_arr, heatmap)
    return superimposed_image


def get_img_array(img_path, size):
    # `img` is a PIL image of the specified size
    img = load_img(img_path, target_size=size)
    # `img_arr` is a float32 Numpy array of shape (size_w, size_h, 3)
    img_arr = img_to_array(img)
    # add a dimension to transform our array into a "batch" of size (1, size_w, size_h, 3)
    img_arr = np.expand_dims(img_arr, axis=0)
    # scale input pixels between -1 and 1
    img_arr = preprocess_input(img_arr)
    return img_arr


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, classifier_layer_names):
    # First, we create a model that maps the input image to the activations of the last conv layer
    last_conv_layer = model.get_layer(last_conv_layer_name)
    last_conv_layer_model = Model(model.inputs, last_conv_layer.output)
    # Second, we create a model that maps the activations of the last conv layer to the final class predictions
    classifier_input = Input(shape=last_conv_layer.output.shape[1:])
    x = classifier_input
    for layer_name in classifier_layer_names:
        x = model.get_layer(layer_name)(x)
    classifier_model = Model(classifier_input, x)
    # Then, we compute the gradient of the top predicted class for our input image with respect to the activations of the last conv layer
    with GradientTape() as tape:
        # Compute activations of the last conv layer and make the tape watch it
        last_conv_layer_output = last_conv_layer_model(img_array)
        tape.watch(last_conv_layer_output)
        # Compute class predictions
        preds = classifier_model(last_conv_layer_output)
        top_pred_index = argmax(preds[0])
        top_class_channel = preds[:, top_pred_index]
    # This is the gradient of the top predicted class with regard to the output feature map of the last conv layer
    grads = tape.gradient(top_class_channel, last_conv_layer_output)
    # This is a vector where each entry is the mean intensity of the gradient over a specific feature map channel
    pooled_grads = reduce_mean(grads, axis=(0, 1, 2))
    # We multiply each channel in the feature map array by "how important this channel is" with regard to the top predicted class
    last_conv_layer_output = last_conv_layer_output.numpy()[0]
    pooled_grads = pooled_grads.numpy()
    for i in range(pooled_grads.shape[-1]):
        last_conv_layer_output[:, :, i] *= pooled_grads[i]
    # The channel-wise mean of the resulting feature map is our heatmap of class activation
    heatmap = np.mean(last_conv_layer_output, axis=-1)
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
    return heatmap


def create_superimposed_image(img_arr, heatmap):
    # rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)
    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap('jet')
    # create an image with RGB colorized heatmap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]
    # create an image with RGB colorized heatmap
    jet_heatmap = array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img_arr.shape[1], img_arr.shape[0]))
    jet_heatmap = img_to_array(jet_heatmap)
    # Superimpose the heatmap on original image
    superimposed_image = jet_heatmap * 0.4 + img_arr
    superimposed_image = array_to_img(superimposed_image)
    return superimposed_image
