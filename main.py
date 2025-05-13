from flask import Flask
import library.person

app = Flask(__name__)

@app.route("/")
def index():
    return "<html style='background-color:#ff0000;'><h1 style='color: #00ff00;'>Holy skibidi toliet</h1></html>"

if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=5000, debug=True)