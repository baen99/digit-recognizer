"""
Contains utility functions for image preprocessing for the classification model
"""

import numpy as np
import base64
import re
from PIL import Image
from io import BytesIO
import torch as tc
from torch import nn

def preprocess(image_data, target_size):
    """
    Transform raw image data into numpy array
    """
    # Remove header: "data:image/png;base64,..."
    image_data = re.sub("^data:image/.+;base64,", "", image_data)

    # Decode from base64 to raw bytes
    image_bytes = base64.b64decode(image_data)

    # Convert to a PIL image
    image = Image.open(BytesIO(image_bytes)) 

    # Convert RGBA image to grayscale and match size with training data
    image_array = np.array(image.convert("L").resize((target_size,target_size)))

    # Scale the drawn image from 0-255 to 16-0 in analogy to the training data
    rescaled_arr = 16*(1 - image_array.astype('float64')/255)

    # check if anything has been drawn at all
    if not rescaled_arr.any():
        raise BlankCanvasError()

    return rescaled_arr


class BlankCanvasError(Exception):
    """
    Raised when client sends an empty canvas
    """
    def __init__(self):
        self.error_message = "Bitte zeichne etwas."
        super().__init__(self.error_message)



"""
Declare CNN as global variable so it can be imported into api.py
"""
conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=2, padding=1, dtype=tc.float64)
conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=2, padding=1, dtype=tc.float64)
pool = nn.MaxPool2d(2,2)
flat = nn.Flatten(start_dim=-3, end_dim=-1)
linear1 = nn.Linear(in_features=32*7*7, out_features=128, dtype=tc.float64)
linear2 = nn.Linear(in_features=128, out_features=10, dtype=tc.float64)

model_cnn = nn.Sequential(
    conv1,
    nn.ReLU(),
    pool,
    conv2,
    nn.ReLU(),
    pool,
    flat,
    linear1,
    nn.ReLU(),
    linear2
)
# no softmax at the end because probabilites are implicitly generated during training in Cross Entropy loss
# add softmax in code when manually predicting on unlabeled input
