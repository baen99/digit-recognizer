"""
Contains utility functions for image preprocessing for the classification model
"""

import numpy as np

def preprocess(image):
    """
    1) Convert RGBA image to grayscale and match size with training data
    2) Scale the drawn image from 0-255 to 16-0 in analogy to the training data
    """ 
    image_array = np.array(image.convert("L").resize((8,8)))
    rescaled_arr = 16*(1 - image_array.astype('float64')/255)
    return rescaled_arr
