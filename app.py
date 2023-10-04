from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'picture' in request.files:
        file = request.files['picture']
        image = Image.open(file.stream).convert("RGB")
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        
        byte_arr = io.BytesIO()
        flipped_image.save(byte_arr, format='JPEG')
        
        byte_arr.seek(0)
        
        return send_file(
            byte_arr,
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename='flipped_image.jpg'
       )
    else:
       return "No file uploaded", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
