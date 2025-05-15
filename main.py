from flask import Flask, render_template, request, url_for, redirect, session
from library.person.person import Person
import library.function

import secrets
import logging
import json
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

@app.route("/")
def index():
    try:
        _person = session["_person"]
        if(_person is not None):
            _person_info = json.loads(_person)
            return render_template("index.html", json_info=_person_info)
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
        request.args.get("name", "None"),
        request.args.get("osis", "NULL"),
        request.args.get("email", "None"),
        request.args.get("organization", "Others")
    )
    _person.save()
    if(_person.check()):
        print("Returned " + _person.name)
        return redirect(url_for("index"))
    session['_person'] = json.dumps(_person.asjson())
    print("Recorded: ")
    print(_person)
    return redirect(url_for("index"))

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True )