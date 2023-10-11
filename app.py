from flask import Flask, request, jsonify
from keras.models import load_model
from PIL import Image
import numpy as np

app = Flask(__name__)
model = load_model('model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img_raw = Image.open(file.stream)
    
    # Preprocess image here (resize to model input size etc.)
    
    img_arr = np.array(img_raw).reshape((1,) + img_raw.size + (1,))
    
    prediction = model.predict(img_arr)
    
    return jsonify({'prediction': prediction.tolist()})

