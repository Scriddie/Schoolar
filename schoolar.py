from flask import Flask, request, render_template, make_response
from flask_session import Session
import numpy as np
import sys

sys.path.append('/var/www/FlaskApps')
from SchoolarFlask.query import *


# generate app and start session
app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)


@app.route("/")
def run():
    user_id = str(np.random.randint(0, 999999))
    create_user_storage(user_id)
    df = load_authors(user_id)
    graphJSON = plot_citations(df)
    resp = make_response(render_template('simple.html', graphJSON=graphJSON))
    resp.set_cookie('userID', user_id)
    return resp


@app.route('/', methods=['POST'])
def my_post():
    user_id = request.cookies.get('userID')
    if 'reset_button' in request.form:
        create_user_storage(user_id)
    elif 'first_author' in request.form:
        pass
    elif 'add_researcher' in request.form:
        text = request.form['add_researcher']
        author = get_author(text)
        if author is None:
            # TODO author does not exist
            pass
        else:
            add_author(author, user_id)
    else:
        pass
    df = load_authors(user_id)
    graphJSON = plot_citations(df)
    return render_template('simple.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()
