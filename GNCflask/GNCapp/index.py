import os
# from
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    app, send_from_directory, Flask, abort, session)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from GNCapp.python_scripts.parseScripts import *
from GNCapp.db import get_db
from flask import current_app, g
from GNCapp.auth import login_required
from GNCapp.db import get_db

bp = Blueprint('hello', __name__)
app = Flask(__name__)
# change it to reusable relative path
app.config['UPLOAD_FOLDER'] = "GNCapp/static/uploads/"  #


# just redirect to index
@bp.route('/')
def redirect_to_index():
    if 'user_id' not in session:
        return redirect('/auth/login')
    else:
        return redirect('/index')


@bp.route('/index', methods=["GET", "POST"])
def index():
    if 'user_id' not in session:
        return redirect('/auth/login')
    else:
        if request.method == "POST":
            if request.files:
                file = request.files["file"]
                print(file)
                db = get_db()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                db.execute(
                    'INSERT INTO user_files (owner_id, file_full_name) VALUES (?, ?)',
                    (str(session['user_id']), file.filename)
                )
                db.commit()
                print('file saved')
                return redirect(request.url)
            # add usage of db
        if request.method == "GET":
            print("GETT")
            req = request.args
            print(req)
            file_name = request.args.get('filename')
            if request.args.get('filename'):
                outputFilename = ""
                error = None
                if request.args.get('input') == 'inputCisco':
                    if request.args.get('output') == 'outputJSON':
                        ciscoToJSON(file_name)
                        outputFilename = file_name + ".json"
                    elif request.args.get('output') == 'outputJuniper':
                        ciscoToJuniper(file_name)
                        outputFilename = file_name + ".txt"
                    else:
                        error = 'There is no point in translating Cisco to Cisco'
                        print('cisco to cisco translating')
                elif request.args.get('input') == 'inputJuniper':
                    if request.args.get('output') == 'outputCisco':
                        juniperToCisco(file_name)
                        outputFilename = file_name + ".txt"
                    elif request.args.get('output') == 'outputJSON':
                        juniperToJSON(file_name)
                        outputFilename = file_name + ".json"
                    else:
                        error = 'There is no point in translating Juniper to Juniper'
                        print('juniper to juniper translating')
                elif request.args.get('input') == 'inputJSON':
                    if request.args.get('output') == 'outputCisco':
                        JSONToCisco(file_name)
                        outputFilename = file_name + ".txt"
                    elif request.args.get('output') == 'outputJuniper':
                        JSONToJuniper(file_name)
                        outputFilename = file_name + ".txt"
                    else:
                        error = 'There is no point in translating JSON to JSON'
                        print('json to json translating')
                if error is None:
                    try:
                        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=outputFilename, as_attachment=True)
                    except FileNotFoundError:
                        print("File not found")
                        abort(404)
                else:
                    flash(error)

            else:
                print("empty")
        return render_template('index.html')


# download with direct link
@bp.route("/get-file/<file_name>")
def get_file(file_name):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)
