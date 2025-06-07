from flask import Flask, render_template, request, jsonify
import base64
import re
from PIL import Image
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt
import utils
import pickle

app = Flask(__name__)
model = pickle.load(open("model_LogReg.pkl", "rb"))
# TODO: train CNN on MNIST dataset for better accuracy

@app.route("/")
def index():
    return render_template("index.html")

#TODO: assert image has correct dimension/size/shape
# TODO: assert image is not empty/something has been drawn at all
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()
    image_data = data["image"]

    # Remove header: "data:image/png;base64,..."
    image_data = re.sub("^data:image/.+;base64,", "", image_data)

    # Decode from base64 to raw bytes
    image_bytes = base64.b64decode(image_data)

    # Convert to a PIL image
    image = Image.open(BytesIO(image_bytes))
    
    preprocessed_image = utils.preprocess(image)

    # model expects batch dimension and flattened images
    input = np.expand_dims(preprocessed_image.flatten(), axis=0)

    prediction = model.predict(input).item()
    print(prediction)


    return jsonify({"message": "Image received"})



if __name__ == "__main__":
    app.run()