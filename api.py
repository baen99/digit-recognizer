from flask import Flask, render_template, request, jsonify
import numpy as np
import utils
import pickle
import torch as tc
import torch.nn.functional as F

#modelname = "Logistic Regression"
modelname = "CNN"

app = Flask(__name__)
mobile = False

if modelname == "Logistic Regression":
    model = pickle.load(open("model_LogReg.pkl", "rb"))
elif modelname == "CNN":
    model = utils.model_cnn
    model.load_state_dict(tc.load("CNN_Digit.ptc", map_location="cpu"))
    model.eval()

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
    
    
    if modelname == "Logistic Regression":
        try:
            preprocessed_image = utils.preprocess(image_data, target_size=8)
        except utils.BlankCanvasError as e:
            # raised if client sends empty canvas
            return jsonify({"error_message": e.error_message}), 400
        
        # model expects batch dimension and flattened images
        input = np.expand_dims(preprocessed_image.flatten(), axis=0)
        probabilities = model.predict_proba(input) # probabilites for all 10 classes
        prediction = probabilities.flatten().argmax().item()
        confidence = round(probabilities.max().item()*100)



    elif modelname == "CNN":
        try:
            preprocessed_image = utils.preprocess(image_data, target_size=28)
        except utils.BlankCanvasError as e:
            # raised if client sends empty canvas
            return jsonify({"error_message": e.error_message}), 400
        
        input_tensor = tc.tensor(preprocessed_image, requires_grad=False)
        input_tensor = input_tensor.unsqueeze(dim=0)
        output = F.softmax(model(input_tensor), dim=-1)
        confidence, prediction = tc.max(output, axis=0)
        confidence, prediction = round(confidence.item()*100), prediction.item()



    return jsonify({"prediction": prediction, "confidence": confidence}), 200



if __name__ == "__main__":
    if mobile:
        host = "0.0.0.0"
    else:
        host = "127.0.0.1" # localhost
    app.run(host=host, port=5000)