import os
from pathlib import Path
from hashlib import md5
from functools import partial

import peewee
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
from sanic import Sanic
from sanic.response import json, html, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape

from memegram.db.models import Image

UPLOAD_DIRECTORY = "./static/pictures"
VIEWS_PATH = Path(__file__).parent.joinpath("views")

app = Sanic()

jinja = SanicJinja2(app, loader=FileSystemLoader(str(VIEWS_PATH)))
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

jinja.add_env(
    "image_static_url", partial(app.url_for, "static", name="images")
)
# Serve CSS files
app.static("/css", "./static/css")
# Serve JS files
app.static("/js", "./static/js")
# Serve Image files
app.static("/images", "./static/pictures", name="images")


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


def render_template(filename, request, **template_variables):
    return jinja.render(
        filename,
        errors=request.get("flash", {}).get("errors", []),
        info=request.get("flash", {}).get("info", []),
        **template_variables,
    )


@app.route("/")
async def test(request):
    return json({"hello": "world"})


@app.route("/upload", methods=["POST"])
async def upload(request):
    picture_file = request.files["picture"][0]
    if len(picture_file.name) > 0:
        filepath = os.path.join(UPLOAD_DIRECTORY, picture_file.name)

        if save_image_details(picture_file, filepath):
            with open(filepath, "wb") as f:
                f.write(picture_file.body)
            request["flash"] = {"info": ["successfully saved image"]}
        else:
            request["flash"] = {"errors": ["Image file already exists"]}
    else:
        request["flash"] = {"errors": ["Please upload a file"]}

    return await index(request)


@app.route("/index")
async def index(request):
    image_files = Image.select()
    return jinja.render("layout.html.jinja2", request, image_files=image_files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
