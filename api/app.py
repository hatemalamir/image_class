import io
import base64
from io import BytesIO
from flask import Flask, jsonify, make_response, send_file, request
from flask_cors import CORS, cross_origin
from grad_cam import grad_cam
from tensorflow.keras.models import load_model

IMG_SIZE = (299, 299)
MODEL_PATH='xception_model_ft.h5'
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
#app.config['CORS_HEADERS'] = 'Content-Type'

model = load_model(MODEL_PATH)
last_conv_layer_name = 'block14_sepconv2_act'
classifier_layer_names = ["global_average_pooling2d_1", "dense_1", "dense_2"]

monkey_labels = {
    0: "Mantled Howler",
    1: "Patas Monkey",
    2: "Bald Uakari",
    3: "Japanese Macaque",
    4: "Pygmy Marmoset",
    5: "White-headed Capuchin",
    6: "Silvery Marmoset",
    7: "Common Squirrel Monkey",
    8: "Black-headed Night Monkey",
    9: "Nilgiri Langur",
}

@app.route('/api/class', methods=['POST'])
@cross_origin(origin='*')
def classifier():
    print("====================reading img=======================")
    req = request.json
    # print(req)
    img_str = req["url"]
    img_name = req['name']
    img_data = base64.b64decode(img_str.split(',')[-1])
    TEMP_IMG_NAME = "/backend/" + img_name
    with open(TEMP_IMG_NAME, 'wb') as f:
        f.write(img_data)
    img, top_pred_index = grad_cam(TEMP_IMG_NAME, IMG_SIZE, model, last_conv_layer_name, classifier_layer_names)
    monkey_name = monkey_labels[top_pred_index]
    print("++++++++++++++++++++Name api "+monkey_name)
    classifiedImg = img_name + '_classified.jpeg'
    img.save(classifiedImg)
    print("====================reading classified img=======================")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    classImg_str = base64.b64encode(buffered.getvalue())
    response = make_response()
    response.data = classImg_str
    response.headers['Access-Control-Expose-Headers']= "name"
    response.headers['name'] = monkey_name
    return response

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
            {"id": 1, "name": "Apples",  "price": "$2"},
            {"id": 2, "name": "Peaches", "price": "$5"}
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
