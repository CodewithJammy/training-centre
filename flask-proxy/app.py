from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Replace with your Google Apps Script Web App URL
GAS_URL = "https://training-centre-proxy-hqhxcyfearcqayhw.centralindia-01.azurewebsites.net"

@app.route("/proxy", methods=["GET", "POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        resp = Response()
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
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

if __name__ == "__main__":
    app.run(debug=True)

