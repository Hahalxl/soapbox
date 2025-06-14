from logging import exception
from flask import send_from_directory
from flask import Flask, render_template, request, url_for, redirect, session, send_file
from library.person.person import *
from library.function import functions
from datetime import datetime

import secrets
import logging
import json
import os

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


@app.route("/error")
def error():
    try:
        if(session['_error']):
            session.pop("_error")
            return render_template("error.html", error=session["_error"])
    except KeyError:
        return redirect(url_for("index"))

@app.route("/")
def index():
    try:
        _person = session["_person"]
        if(_person):
            _person_info = json.loads(_person)
            return render_template("confirm.html", this=_person_info)
        
    except Exception as e:
        pass
    return render_template("index.html")

@app.route("/record")
def record():
    _person = Person(
        request.args.get("last", "None"),
        request.args.get("first", "None"),
        request.args.get("email", "None"),
        request.args.get("phone", "None"),
        request.args.get("school", "John Dewey High School"),
        request.args.get("osis", "None"),
        request.args.get("dobs", "None"),
        request.args.get("role", "None")
    )
    try:
        _person.save()
        session['_recorded'] = False
        session['_person'] = json.dumps(_person.asjson())
        return redirect(url_for("index"))
    except Exception as e:
        session["_error"] = f"Error saving record: {str(e)}"
        return redirect(url_for("error"))

    return redirect(url_for("index"))

@app.route("/return")
def returnindex():
    session.clear()
    return redirect(url_for("index"))



if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=500, debug=True)
