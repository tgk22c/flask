from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # 파일이 존재하면 아래 코드로 저장할 수 있습니다.
    # file.save(os.path.join('uploads', filename))
    
    return 'File uploaded successfully'
