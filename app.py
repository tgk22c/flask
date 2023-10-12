from PIL import Image
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model 
import numpy as np

app=Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']  # 클라이언트에서 전송된 파일을 가져옵니다.
    image = Image.open(file).convert('L')  # 파일 객체를 이미지로 변환하고 흑백(그레이스케일)으로 변환합니다.
    
    resized_image = image.resize((28, 28))  # 이미지 크기를 조정합니다.
    normalized_image = np.array(resized_image) / 255.0  # 픽셀 값을 [0,1] 범위로 정규화(normalize)합니다.

    model = load_model('model.h5')  # 학습된 모델을 로드합니다.

    prediction = model.predict(normalized_image.reshape(1, -1))   # 모델을 사용하여 이미지의 숫자를 예측합니다. shape 변경
    
    return jsonify({'prediction': prediction.tolist()})   # 예측 결과를 JSON 형식으로 반환합니다.

