from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model 
import numpy as np

app=Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    data=request.form['data']
    
    # parse string of floats into a numpy array with shape (1,784)
    input_data=np.array([float(pixel_str) for pixel_str in data.split(',')]).reshape(1,-1)

   
    model=load_model('model.h5') 

   
    prediction=model.predict(input_data)

  
    final_prediction=np.argmax(prediction)

    return jsonify({'prediction': final_prediction.tolist()})
