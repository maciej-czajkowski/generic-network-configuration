from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'json'}

from GNCapp.auth import login_required
from GNCapp.db import get_db

bp = Blueprint('hello', __name__)

@bp.route('/index')
def hello():
    return render_template('hello.html')

@bp.route('/upload-image', methods=["GET", "POST"])
def upload_image():
    return render_template('upload-image.html')




# @app.route('/bye')
# def good_bye():
#     return 'Good Bye!'
# #
# #
# if __name__ == '__main__':
#     app.run()
