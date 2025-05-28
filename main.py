from logging import exception
from flask import send_from_directory
from flask import Flask, render_template, request, url_for, redirect, session
from library.person.person import *
from library.function import functions

import secrets
import logging
import json
import os

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

# Helper function to load config
def _config():
    """
    Reads config.json and returns the 'filing' dictionary
    You must have a config.json file in your project root with this format:

    {
      "filing": {
        "name": "5312025.csv",
        "dir": "data"
      }
    }
    """
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config["filing"]

@app.route("/")
def index():
    try:
        _person = session["_person"]
        if(_person is not None):
            _person_info = json.loads(_person)
            _person_info["color"] = functions.randcol()
            _person_info["recorded"] = session['_recorded']
            session.clear()
            return render_template("information.html", _person=_person_info)
    except KeyError:
        pass
    return render_template("index.html")

@app.route("/record")
def record():
    # Get and clean OSIS (default to "None" if empty)
    osis = request.args.get("osis", "").strip()
    osis = "None" if not osis else osis

    # Get and clean organization (default to "None" if empty)
    org = request.args.get("organization", "").strip() or "None"
    orgs = request.args.get("organizations", "").strip() or org  # Fallback to org if empty

    _person = Person(
        request.args.get("first_name", "None") + " " + request.args.get("last_name", "None"),
        osis,  # Now "None" if empty
        request.args.get("email", "None"),
        orgs   # Now "None" if empty
    )

    if _person.check():
        session['_person'] = json.dumps(_person.asjson())
        session['_recorded'] = True
        return redirect(url_for("index"))

    print(f"Recording: {_person}")
    
    try:
        saved = _person.save()
        if saved:
            session['_recorded'] = False
            session['_person'] = json.dumps(_person.asjson())
            print("Clearing Console...")
            os.system("cls" if os.name == 'nt' else "clear")
        else:
            session["_error"] = "Failed to save record. Check file permissions."
            return redirect(url_for("error"))
    except Exception as e:
        session["_error"] = f"Error saving record: {str(e)}"
        return redirect(url_for("error"))

    return redirect(url_for("index"))

@app.route("/admin")
def admin_login():
    _admin = Admin(
        name = request.args.get("username"),
        password = request.args.get("password")
    )

    if(_admin.ifadmin()):
        _json = json.dumps({"name":_admin.name, "password":_admin.password})
        session["admin"] = _json
        session["output"] = " "
        return redirect(url_for("control"))
    else:
        session["_error"] = "Person not authorized"
        return redirect(url_for("error"))

@app.route("/controls")
def control():
    try:
        _output = session["output"]
        _info = session["admin"]
        thisinfo = functions.information()
        if(_output != " "):
            _output = json.loads(_output)
    except Exception as e:
        session["_error"] = f"Unfound error: {e}"
        return redirect(url_for("error"))

    if(_info):
        return render_template("admin.html", output=_output, info=thisinfo)
    session["_error"] = "Person not authorized"
    return redirect(url_for("error"))

@app.route("/delete")
def delete():
    _person = Person(
        request.args.get("first_name", "None") + " " + request.args.get("last_name", "None"),
        request.args.get("osis", "NULL"),
        request.args.get("email", "None"),
        request.args.get("organizations", "Others") if not request.args.get("organization", "Others") else request.args.get("organization", "Others")
    )
    print(_person)
    if (_person.check()):
        remove(_person)
        session["output"] = json.dumps({"command":f"sudo remove {_person.name}", "output":"Successfully removed!"})
        session["admin"] = True
    else:
        session["output"] = json.dumps({"command": f"sudo remove {_person.name}", "output":"Failed to find person, please ensure that you have inputted the correct information"})
        session["admin"] = True
    return redirect(url_for("control"))

@app.route("/edit")
def edit():
    _person = Person(
        request.args.get("first_name", "None") + " " + request.args.get("last_name", "None"),
        request.args.get("osis", "NULL"),
        request.args.get("email", "None"),
        request.args.get("organizations", "Others") if not request.args.get("organization", "Others") else request.args.get("organization", "Others")
    )
    print(_person)
    if (_person.check()):
        replaces(_person)
        session["output"] = json.dumps({"command":f"sudo edit {_person.name}", "output":"Successfully editted!"})
        session["admin"] = True
    else:
        session["output"] = json.dumps({"command": f"sudo edit {_person.name}", "output":"Failed to find person, please ensure that you have inputted the correct information"})
        session["admin"] = True
    return redirect(url_for("control"))
#added
@app.route("/download")
def download_csv():
    if "admin" not in session:
        session["_error"] = "Unauthorized access to download."
        return redirect(url_for("error"))
    
    config = _config()
    filename = config["name"]     # "5312025.csv"
    directory = config["dir"]     # "data"
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    session.pop("output", None)
    return redirect(url_for("index"))

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)
