from flask import Flask, request, render_template, make_response
import os
import sys
parent_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent_dir)
import query
import json


# # view counter configuration
# app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
# app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'
# from flask.ext.track_usage import TrackUsage
# from flask_track_usage.storage.printer import PrintWriter
# from flask_track_usage.storage.output import OutputWriter

# # Make an instance of the extension and put two writers
# t = TrackUsage(app, [
#     PrintWriter(),
#     OutputWriter(transform=lambda s: "OUTPUT: " + str(s))
# ])


app = Flask(__name__)


@app.route("/")
def run():
    user_id = query.new_user_id()
    query.create_user_storage(user_id)
    author_data = query.load_authors(user_id)
    graphJSON = query.plot_citations(author_data)
    resp = make_response(render_template('simple.html', graphJSON=graphJSON))
    resp.set_cookie('userID', user_id)
    return resp


@app.route('/', methods=['POST'])
def my_post():
    user_id = request.cookies.get('userID')
    profile_names = ""
    if 'reset_button' in request.form:
        query.create_user_storage(user_id)
    elif 'first_author' in request.form:
        # TODO
        pass
    elif 'add_researcher' in request.form:
        text = request.form['add_researcher']
        author, profile_names = query.get_author(text)
        if author is None:
            # TODO author does not exist
            pass
        else:
            query.add_author(author, user_id)
    else:
        pass
    author_data = query.load_authors(user_id)
    bar, timeline = query.plot_citations(author_data)
    profile_list = json.dumps(list(profile_names.split('---')))
    return render_template('simple.html', 
                           profiles=profile_names,
                           list=profile_list, # json.dumps(profile_list)
                           bar=bar,
                           timeline=timeline)


if __name__ == "__main__":
    app.run()
