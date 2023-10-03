import os
import io
from flask import Flask, request, send_file
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Ensure the upload directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Flip the image upside down
            img = Image.open(filepath)
            img_rotated = img.rotate(180)
            
            # Save the rotated image to a BytesIO object
            byte_io = io.BytesIO()
            img_rotated.save(byte_io, 'JPEG')
            byte_io.seek(0)

           return send_file(
                byte_io,
                mimetype='image/jpeg',
                as_attachment=True,
                attachment_filename=filename)
    else:
        return '''
        <!doctype html>
        <title>Upload a .jpg File</title>
        <h1>Upload a .jpg File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
       '''

if __name__ == "__main__":
   app.run(debug=True)
``
