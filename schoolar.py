from flask import Flask, request, render_template
import sys
sys.path.append('/var/www/FlaskApps')
from SchoolarFlask.query import *

app = Flask(__name__)


@app.route("/")
def run():
    christof = get_author('Christof Seiler')
    sebastian = get_author('Sebastian Weichwald')
    graphJSON = plot_citations(christof, sebastian)
    return render_template('simple.html', graphJSON=graphJSON)
    # return christof['name']
    # return "Hello world! and stars"


@app.route('/', methods=['POST'])
def my_post():
    text = request.form['add_researcher']
    researcher = get_author(text)
    graphJSON = plot_citations(researcher)
    return render_template('simple.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()
