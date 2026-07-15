from flask import Flask, request, Response
import requests
from flask_cors import CORS
from flask import Flask
from db_config import init_db, db
from routes.admin_routes import admin_bp

app = Flask(__name__)
init_db(app)

# Register the admin blueprint
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensures ExamQuestions table exists
    app.run(debug=True)

app = Flask(__name__)
CORS(app)  # adds CORS headers automatically

# Google Apps Script Web App URL
GAS_URL = "https://script.google.com/macros/s/AKfycbwbJedA3rIluoThDP3r17JbrotsKpEWqBCppgGhikuSQn1PCydVO_rMj3G0tI65I6NJLw/exec"

@app.route("/proxy", methods=["GET", "POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        # Explicit preflight response
        resp = Response()
        resp.status_code = 200
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    if request.method == "GET":
        r = requests.get(GAS_URL, params=request.args)
    else:
        r = requests.post(GAS_URL, json=request.json)

    resp = Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type"))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

if __name__ == "__main__":
    app.run(debug=True)
