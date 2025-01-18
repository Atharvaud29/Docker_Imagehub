from flask import flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Word!"

if __name__=="__name__":
    app.run(host="0.0.0.0", port=5000)
