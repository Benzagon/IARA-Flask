import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import requests
from useful_functions import model_predict_cnn, model_cnn
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return jsonify("Hola")


@app.route('/predict', methods=['POST'])
def upload():
    print(request.json)
    imagefile = request.json
    req = requests.post('http://localhost:4000/images/sendFile', json=imagefile)
    print(req)
    print(req.content)

    base64_data = req.content

    image = Image.open(io.BytesIO(base64_data))
    print(image)

    '''imagefile = request.files['file']
    print(imagefile)
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)
    '''

    preds = model_predict_cnn(image, model_cnn)

    accuracy = float(np.max(preds, axis=1)[0])
    accuracy = str(round(accuracy * 100 , 2))
    accuracy = accuracy + ' %'

    response = {'prediction: ' : accuracy}


    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8000,debug=True)
