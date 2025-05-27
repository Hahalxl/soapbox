from logging import exception

from flask import Flask, render_template, request, url_for, redirect, session
from library.person.person import *
from library.function import functions

import secrets
import logging
import json, os
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

#pip install -r requirement.txt

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

@app.route("/error")
def error():
    try:
        if(session['_error']):
            return render_template("error.html", error=session["_error"])
    except Exception as _:
        return redirect(url_for("index"))

@app.route("/record")
def record():
    _person = Person(
        request.args.get("first_name", "None") +" "+request.args.get("last_name", "None"),
        request.args.get("osis", "NULL"),
        request.args.get("email", "None"),
        request.args.get("organizations","Others") if not request.args.get("organization", "Others") else request.args.get("organization", "Others")
    )

    if(_person.check()):
        session['_person'] = json.dumps(_person.asjson())
        session['_recorded'] = True
        return redirect(url_for("index"))

    print("Recorded: ")
    print(_person)
    saved = _person.save()
    if(saved):
        session['_recorded'] = False
        session['_person'] = json.dumps(_person.asjson())
        print("Clearing Console....")
        os.system("cls")
    else:
        session["_error"] = "Person not record ERROR! Something is wrong with the file."
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




if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)