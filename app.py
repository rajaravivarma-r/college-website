import os

from sanic import Sanic
from sanic.response import json, html, redirect

UPLOAD_DIRECTORY = "./static/pictures"

app = Sanic()

# Serve CSS files
app.static("/css", "./static/css")
# Serve JS files
app.static("/js", "./static/js")


def readhtml_file(filename):
    with open(filename, "r") as f:
        return f.read()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/upload", methods=["POST"])
async def upload(request):
    if len(request.files["picture"]) > 0:
        picture_file = request.files["picture"][0]
        filename = os.path.join(UPLOAD_DIRECTORY, picture_file.name)
        with open(filename, "wb") as f:
            f.write(picture_file.body)

    return redirect(app.url_for("index"))


@app.route("/index")
async def index(request):
    return html(readhtml_file("./views/layout.html"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
