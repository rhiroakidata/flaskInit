from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
db = MySQL(app)
app.config.from_pyfile('config.py')

from endpoints import *

if __name__ == '__main__':
    app.run(debug=True)

