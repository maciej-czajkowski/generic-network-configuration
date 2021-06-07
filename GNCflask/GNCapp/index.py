import os
import subprocess
import pathlib
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
app.config['UPLOAD_FOLDER'] = "GNCapp/static/uploads/"
app.config['DOWNLOAD_FOLDER'] = "static/uploads/"




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
                # file = request.files["file"]
                # print(file)
                # db = get_db()
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                # db.execute(
                #     'INSERT INTO user_files (owner_id, file_full_name) VALUES (?, ?)',
                #     (str(session['user_id']), file.filename)
                # )
                # db.commit()
                # print('file saved')
                tmp = pathlib.Path("tmp")
                input_config = request.files["input_config"]
                input_config_filename = input_config.filename #for latter use
                input_config.save(os.path.join("../tmp", "input_config"))

                input_config = request.files["config_py"]
                input_config_filename = input_config.filename #for latter use
                input_config.save(os.path.join("../tmp", "config.py"))


                docker_cmd = ["python3", "GNCapp/docker/docker_runner.py", 
                        "-c", "../../../tmp/config.py", 
                        "-i", "../../../tmp/input_config", 
                        "-if", request.form.to_dict()['input'],
                        "-of", request.form.to_dict()['output']]
                print(docker_cmd)

                docker_proc = subprocess.run(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if docker_proc.returncode:
                    print("Something went wrong with docker ", docker_proc.returncode)
                else:
                    f = open("GNCapp/docker/out/output.txt", "r").readlines() # <-- parsed config
                    print(f)
                #  move to new page with link to download

                # clean up
                os.remove("../tmp/config.py")
                os.remove("../tmp/input_config")
                # os.remove("GNCapp/docker/out/output.txt")


                return redirect(request.url)
            # add usage of db
        if request.method == "GET":
            print("GET")
            req = request.args
            print(req)
            file_name = request.args.get('filename')
            if request.args.get('filename'):
                outputFilename = ""
                error = None
                db = get_db()
                if db.execute('SELECT file_id FROM user_files WHERE owner_id = ? and file_full_name = ?', (str(session['user_id']), file_name)).fetchone() is None:
                    error = "You don't have file with name " + file_name
                # else:
                    # ToDo: add proper validation on java_script level or sth


                    # docker_cmd = ["python3", "docker/docker_runner.py", 
                    #     "-c", "config.py", 
                    #     "-i", "input_file", 
                    #     "-if", request.args.get('input'),
                    #     "-of", request.args.get('output')]
                    # docker_proc = subprocess.run(docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # if docker_proc.returncode:
                    #     print("Something went wrong with docker ", docker_proc.returncode)
                    # else:
                    #     f = open("/docker/output.txt", "r").readlines()
                    #     print(f)


                    # if request.args.get('input') == 'inputCisco':
                    #     if request.args.get('output') == 'outputJSON':
                    #         ciscoToJSON(file_name)
                    #         outputFilename = file_name + ".json"
                    #     elif request.args.get('output') == 'outputJuniper':
                    #         ciscoToJuniper(file_name)
                    #         outputFilename = file_name + ".txt"
                    #     else:
                    #         error = 'There is no point in translating Cisco to Cisco'
                    #         print('cisco to cisco translating')
                    # elif request.args.get('input') == 'inputJuniper':
                    #     if request.args.get('output') == 'outputCisco':
                    #         juniperToCisco(file_name)
                    #         outputFilename = file_name + ".txt"
                    #     elif request.args.get('output') == 'outputJSON':
                    #         juniperToJSON(file_name)
                    #         outputFilename = file_name + ".json"
                    #     else:
                    #         error = 'There is no point in translating Juniper to Juniper'
                    #         print('juniper to juniper translating')
                    # elif request.args.get('input') == 'inputJSON':
                    #     if request.args.get('output') == 'outputCisco':
                    #         JSONToCisco(file_name)
                    #         outputFilename = file_name + ".txt"
                    #     elif request.args.get('output') == 'outputJuniper':
                    #         JSONToJuniper(file_name)
                    #         outputFilename = file_name + ".txt"
                    #     else:
                    #         error = 'There is no point in translating JSON to JSON'
                    #         print('json to json translating')
                if error is None:
                    try:
                        return send_from_directory(app.config["DOWNLOAD_FOLDER"], path=outputFilename, as_attachment=True)
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
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename=file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)
