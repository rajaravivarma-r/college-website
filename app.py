import os
from hashlib import md5

import peewee
from sanic import Sanic
from sanic.response import json, html, redirect

from memegram.db.models import Image

UPLOAD_DIRECTORY = "./static/pictures"

app = Sanic()

# Serve CSS files
app.static("/css", "./static/css")
# Serve JS files
app.static("/js", "./static/js")


def save_image_details(image_file, image_filepath):
    image_digest = md5(image_file.body).hexdigest()
    try:
        Image.create(
            filename=image_file.name,
            filepath=image_filepath,
            digest=image_digest,
        )
        return True
    except peewee.IntegrityError as e:
        print("Duplicate file detected")
        return False


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
        filepath = os.path.join(UPLOAD_DIRECTORY, picture_file.name)
        save_image_details(picture_file, filepath)

        with open(filepath, "wb") as f:
            f.write(picture_file.body)

    return redirect(app.url_for("index"))


@app.route("/index")
async def index(request):
    return html(readhtml_file("./views/layout.html"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
