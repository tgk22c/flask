from flask import Flask, request, jsonify  # 필요한 라이브러리들을 임포트합니다.
from keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)  # Flask 앱 객체를 생성합니다.

# Load your trained model
model = load_model('model.h5')  # 학습된 모델을 불러옵니다. 'model.h5' 파일이 서버와 같은 위치에 있어야 합니다.

@app.route('/predict', methods=['POST'])  # '/predict' 경로에 POST 요청이 오면 아래 함수를 실행합니다.
def predict():
    if 'file' not in request.files:  # 요청에서 파일을 받지 못하면 에러 메시지와 함께 HTTP 상태 코드 400을 반환합니다.
        return jsonify({'error': 'no file'}), 400
    
    file = request.files['file']  # 요청에서 파일 객체를 가져옵니다.
    image = Image.open(file).convert('L')  # 파일 객체를 이미지로 변환하고 흑백(그레이스케일)으로 변환합니다.

    # Preprocess the image - Invert colors, resize and normalize pixels values 
    image = np.invert(image)   # 이미지의 색상을 반전시킵니다 (MNIST 데이터셋과 동일하게 처리).
    image = np.array(image.resize((28, 28))) / 255.0   # 이미지 크기를 조정하고 픽셀 값을 [0,1] 범위로 정규화(normalize)합니다.

    prediction = model.predict(image[np.newaxis,:,:,np.newaxis])   # 전처리된 이미지에 대해 모델 예측을 수행합니다.
    
    return jsonify({'prediction': int(np.argmax(prediction))})   # 예측 결과 중 가장 확률이 높은 클래스의 인덱스(여기서는 숫자)를 JSON 형태로 반환합니다.

