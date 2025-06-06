from flask import Flask, render_template, request, jsonify
import base64
import re
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


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

    # Do something with it
    print("Image mode:", image.mode)
    print("Image size:", image.size)
    image.show()  # Opens the image using default viewer 
    return jsonify({"message": "Image received"})



if __name__ == "__main__":
    app.run()