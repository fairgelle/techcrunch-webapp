from flask import Flask

app = Flask(__name__)

from techcrunchapp import routes
