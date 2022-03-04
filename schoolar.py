from flask import Flask, request, render_template
import sys
sys.path.append('/var/www/FlaskApps')
from SchoolarFlask.query import *

app = Flask(__name__)


@app.route("/")
def run():
    a = get_author('Christof Seiler')
    df = add_author(df=None, a)
    b = get_author('Sebastian Weichwald')
    df = add_author(df, b)
    graphJSON = plot_citations(df)
    return render_template('simple.html', graphJSON=graphJSON)
    # return christof['name']
    # return "Hello world! and stars"


@app.route('/', methods=['POST'])
def my_post():
    df = pd.read_csv('temp/authors.csv')
    text = request.form['add_researcher']
    author = get_author(text)
    df = add_author(df, author)
    graphJSON = plot_citations(df)
    return render_template('simple.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()
