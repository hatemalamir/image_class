import io
from flask import Flask, jsonify, make_response,send_file,request
from flask_cors import CORS,cross_origin
from grad_cam import grad_cam
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import Xception

IMG_SIZE = (299, 299)
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/class', methods=['POST'])
@cross_origin(origin='*')
def classifier():
    print("====================testing=======================")
    req = request.json
    # print(req)
    img_path =req["url"]
    img_name = req['name']
    # print(img_path)
    model = Xception(weights='imagenet')
    last_conv_layer_name = 'block14_sepconv2_act'
    classifier_layer_names = ["avg_pool", "predictions", ]
    img = grad_cam(img_path, IMG_SIZE, model, last_conv_layer_name, classifier_layer_names)
    return img.save("testing.jpeg")
    # img2 = img
    # img2.save("testing.jpeg")
    # bytImg = io.BytesIO()
    # img.save(bytImg,"jpeg")
    # bytImg.seek(0)
    # #returnV.append({"original":,"cam":,"label"})
    # return send_file(bytImg, mimetype='image/jpg')



@app.route('/api/v1.0/test', methods=['GET'])
def test_response():
    """Return a sample JSON response."""
    sample_response = {
        "items": [
            { "id": 1, "name": "Apples",  "price": "$2" },
            { "id": 2, "name": "Peaches", "price": "$5" }
        ]
    }
    # JSONify response
    response = make_response(jsonify(sample_response))

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    # Mozilla provides good references for Access Control at:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Server-Side_Access_Control

    return response
