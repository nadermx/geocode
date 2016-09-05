import os
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import geocoder
import config
import uuid
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # google = request.form.getlist('google')[0]
        # baidu =
        # bing =
        # canadapost =
        # mapquest =
        #
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = '%s___%s' % (filename, uuid.uuid4())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    saved_column = df.ADDRESS
    addresses = []
    for i in saved_column:
        g = geocoder.yahoo(i)
        print(g)
        addresses.append([i, g])
    return jsonify(addresses)


if __name__ == "__main__":
    app.run(debug=True)
