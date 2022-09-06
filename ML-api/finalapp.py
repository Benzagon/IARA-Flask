from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import base64
from PIL import Image
import io
import re

img_size = 100

app = Flask(__name__)

model = load_model('model-015.model')

label_dict = {0: 'Covid19 Negative', 1: 'Covid19 Positive'}


def preprocess(img):

    img = np.array(img)

    if (img.ndim == 3):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    gray = gray/255
    resized = cv2.resize(gray, (img_size, img_size))
    reshaped = resized.reshape(1, img_size, img_size)
    return reshaped


@app.route("/")
def index():
    return "Hola"


@app.route("/predict", methods=["POST"])
def predict():
    print('HERE')

    imagefile = request.files['imagefile']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    decoded = base64.b64decode(imagefile)
    dataBytesIO = io.BytesIO(decoded)
    dataBytesIO.seek(0)
    image = Image.open(dataBytesIO)

    test_image = preprocess(image)

    prediction = model.predict(test_image)
    result = np.argmax(prediction, axis=1)[0]
    accuracy = float(np.max(prediction, axis=1)[0])

    label = label_dict[result]

    print(prediction, result, accuracy)

    response = {'prediction': {'result': label, 'accuracy': accuracy}}

    return jsonify(response)


app.run(debug=True)

# <img src="" id="img" crossorigin="anonymous" width="400" alt="Image preview...">
