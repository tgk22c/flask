from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        
        # 임시로 저장할 경로 지정. 실제 서버에서는 보안상의 이유로 안전한 위치를 선택해야 합니다.
        temp_path = os.path.join('temp', file.filename)
        
        # 파일을 임시 경로에 저장
        file.save(temp_path)

        # 이미지 상하 반전 처리
        flipped_img = flip_image(temp_path)

        # 결과 이미지를 저장할 경로 지정. 여기서는 원본 파일명에 '_flipped'를 추가합니다.
        result_path = os.path.join('results', os.path.splitext(file.filename)[0] + '_flipped.jpg')

        # 결과 이미지 저장
        flipped_img.save(result_path)

    return render_template('index.html')

def flip_image(image_path):
    img = Image.open(image_path)
    flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    return flipped_img

if __name__ == '__main__':
    app.run(debug=True)
