from flask import Flask, request

app = Flask(__name__)


@app.route("/get_text", methods=["GET", "POST"])
def get_text():
    print(f"request.method: {request.method}")

    if request.method == "POST":
        if "file" not in request.files:
            return "You must send file"

        file = request.files["file"]
        if not file or file.filename == "":
            return "You must send not empty file"

        if file.mimetype not in {"image/jpeg"}:
            return "You must send file with mime type: image/jpeg"

    return {"name": "Arsenii", "surname": "Kuznetsov"}
