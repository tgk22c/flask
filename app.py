from flask import Flask, request
import numpy as np
from PIL import Image
import io

def create_app():
    app = Flask(__name__)
    model = None

    @app.before_first_request
    def load_model_to_app():
        from tensorflow.python.keras.models import load_model
        app.model = load_model('model.h5')

    @app.route('/predict', methods=['POST'])
    def predict():
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        try:
            img = Image.open(io.BytesIO(file.read())).convert("L") # Open the image file and convert it to grayscale
            img = img.resize((28, 28)) # Resize the image to 28x28 pixels as required by the model
            img_arr = np.array(img) / 255.0 # Convert the image to a numpy array and normalize pixel values
            
            prediction = app.model.predict(img_arr.reshape(1,784)) # Reshape the array for model input and make prediction
            predicted_class = np.argmax(prediction) # Get index of highest probability class from softmax output
            
            return str(predicted_class), 200

        except Exception as e:
             return str(e), 500 

    return app

