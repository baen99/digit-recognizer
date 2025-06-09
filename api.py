from flask import Flask, render_template, request, jsonify
import numpy as np
import utils
import pickle

app = Flask(__name__)
model = pickle.load(open("model_LogReg.pkl", "rb"))
# TODO: train CNN on MNIST dataset for better accuracy

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error_message": "Ungültiges oder fehlendes JSON."}), 400
    # 2 different ways of error handling just for practice's sake
    try:
        assert "image" in data, "Dict enthält keinen key 'image'."
    except AssertionError as e:
        return jsonify({"error_message": e.args[0]}), 400
    

    image_data = data["image"]
    
    try:
        preprocessed_image = utils.preprocess(image_data)
    except utils.BlankCanvasError as e:
        # rasied if client sends empty canvas
        return jsonify({"error_message": e.error_message}), 400
    

    # model expects batch dimension and flattened images
    input = np.expand_dims(preprocessed_image.flatten(), axis=0)

    probabilities = model.predict_proba(input) # probabilites for all 10 classes
    prediction = probabilities.flatten().argmax().item()
    confidence = round(probabilities.max().item()*100)


    return jsonify({"prediction": prediction, "confidence": confidence}), 200



if __name__ == "__main__":
    app.run()