import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    app, send_from_directory, Flask)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from GNCapp.auth import login_required
from GNCapp.db import get_db

bp = Blueprint('hello', __name__)
app = Flask(__name__)
#change it to reuseable relative path
app.config['UPLOAD_FOLDER'] ="D:\\STUDIA\\INFORMATYKA\\SEMESTR 6\\Projekt " \
                             "kompetencyjny\\generic-network-configuration\\GNCflask\\GNCapp\\static\\uploads" #
# app.config["ALLOWED_FILE_EXTENSIONS"] = ["JSON","TXT"]
##check filename
##secure file name
##flash when succes and fail
##filesize
@bp.route('/upload-file', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":

        if request.files:
            file = request.files["file"]
            # if file.filename == "":
            #     flash('No file part')
            # return redirect(request.url)
                  # if 'file' not in request.files:
            #     flash('No file part')
            #     return redirect(request.url)
            print(file)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print ('file saved')
            return redirect(request.url)

    return render_template('upload-file.html')

@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

# @app.route('/bye')
# def good_bye():
#     return 'Good Bye!'
# #
# #
# if __name__ == '__main__':
#     app.run()
