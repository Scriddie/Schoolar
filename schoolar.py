from flask import Flask
import sys
sys.path.append('/var/www/FlaskApps')
from SchoolarFlask.Schoolar.src.test import *

app = Flask(__name__)

@app.route("/")
def hello():
    christof = get_author('Christof Seiler')
    return christof['name']
    # return "Hello world! and stars"

if __name__ == "__main__":
    app.run()
