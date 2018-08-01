from flask import Flask, render_template,redirect,url_for,send_from_directory, flash, request,send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
import os
import pyttsx3

UPLOAD_FILE_PATH = '/home/swayam/Desktop/mike/storage'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FILE_PATH'] = UPLOAD_FILE_PATH


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def launch():
    return render_template("home2.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/img_to_text", methods=['POST'])
def product_create():
    file_name = request.form['file_name']
    #print(str(file_name))
    from PIL import Image
    import pytesseract
    im = Image.open(file_name)
    text = pytesseract.image_to_string(im, lang = 'eng')
    print(text)
    return render_template("asd.html", msg=text)


@app.route("/text_to_voice", methods=['POST','GET'])
def product(file_name):
    # file_name = request.form['file_name']
    # print(str(file_name))
    from PIL import Image
    import pytesseract
    from gtts import gTTS
    import os

    im = Image.open(file_name)

    gg = pytesseract.image_to_string(im, lang='eng')

    print(gg)

    engine = pyttsx3.init()
    engine.setProperty('voice','english+f3')
    engine.setProperty('rate',150)
    engine.say(gg)
    engine.runAndWait()

    #tts = gTTS(text=gg)
    #tts.save("img_text.mp3")
    #os.system("cvlc img_text.mp3")
    # return render_template("zxc.html", message=text)


@app.route('/file_upload', methods=['GET', 'POST'])
def store():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_name' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file_name']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FILE_PATH'], filename))
            return redirect(url_for('storing_file', filename=filename))
    return 'successful'


@app.route('/abc/<filename>')
def storing_file(filename):
    product(filename)
    return send_from_directory(app.config['UPLOAD_FILE_PATH'],
                               filename)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
