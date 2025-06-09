"""
Contains utility functions for image preprocessing for the classification model
"""

import numpy as np
import base64
import re
from PIL import Image
from io import BytesIO

def preprocess(image_data):
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
    image_array = np.array(image.convert("L").resize((8,8)))

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
