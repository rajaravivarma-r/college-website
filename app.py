from sanic import Sanic
from sanic.response import json, html

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


@app.route("/index")
async def index(request):
    return html(readhtml_file("./views/layout.html"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
