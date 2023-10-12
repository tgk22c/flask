from flask import Flask, request
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# 모델 불러오기
model = tf.keras.models.load_model('your_model_path')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    image = preprocess_image(file)
    prediction = make_prediction(image)
    return prediction

def preprocess_image(file):
    img = tf.keras.preprocessing.image.load_img(file, target_size=(28, 28), color_mode='grayscale')
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array /= 255.0  # 이미지 정규화
    return np.expand_dims(img_array, axis=0)

def make_prediction(image):
    predictions = model.predict(image)
    class_index = np.argmax(predictions[0])
    
    # 클래스 인덱스에 따라 예측 결과 반환 (여기서는 단순히 클래스 인덱스를 문자열로 변환하여 반환)
    return str(class_index)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
