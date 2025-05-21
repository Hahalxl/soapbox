from logging import exception

from flask import Flask, render_template, request, url_for, redirect, session
from library.person.person import Person, Admin
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
            return render_template("information.html", _person=_person_info)
    except KeyError:
        pass
    return render_template("index.html")

@app.route("/error")
def error():
    if(session['_error']):
        return render_template("error.html", error=session["_error"])
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
        print("Returned " + _person.name)
        return redirect(url_for("index"))

    print("Recorded: ")
    print(_person)
    saved = _person.save()
    if(saved):
        session['_person'] = json.dumps(_person.asjson())
        print("Clearing Console....")
        # CHANGE THIS TO CLEAR IF MAC MUST DO OR IT BREAKS
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
        return redirect(url_for("admin"))

@app.route("/admin-panel")
def admin():
    try:
        _info = session["admin"]
        perm = json.loads(_info)
    except Exception as e:
        session["_error"] = e
        return redirect(url_for("error"))

    if(perm["name"]):
        return render_template("admin.html")

    session["_error"] = "Unauthorize request"
    return redirect(url_for("error"))



if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True )