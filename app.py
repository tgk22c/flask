from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

app = Flask(__name__)
model = load_model('model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img_raw = Image.open(file.stream).convert('L') # Convert to grayscale

    # Resize image to 28x28 pixels 
    img_resized = img_raw.resize((28, 28), Image.ANTIALIAS)

    # Convert image data to numpy array and normalize
    img_arr = np.array(img_resized) / 255.0
    
    # Reshape for model input and make prediction
    img_arr = img_arr.reshape((1,) + (img_arr.shape[0], img_arr.shape[1], 1))
    
    prediction = model.predict(img_arr)
    
    predicted_class = np.argmax(prediction) # Get class with highest probability
    
    return jsonify({'prediction': int(predicted_class)}) # Return as JSON

if __name__ == '__main__':
   app.run()
