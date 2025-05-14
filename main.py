from flask import Flask, render_template
import library.person
import library.function

import logging
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True )