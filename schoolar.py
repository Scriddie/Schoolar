from flask import Flask, request, render_template
import sys
sys.path.append('/var/www/FlaskApps')
from SchoolarFlask.query import *

app = Flask(__name__)


@app.route("/")
def run():
    df = load_authors()
    graphJSON = plot_citations(df)
    return render_template('simple.html', graphJSON=graphJSON)
    # return christof['name']
    # return "Hello world! and stars"


@app.route('/', methods=['POST'])
def my_post():
    text = request.form['add_researcher']
    author = get_author(text)
    add_author(author)
    df = load_authors()
    graphJSON = plot_citations(df)
    return render_template('simple.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()
