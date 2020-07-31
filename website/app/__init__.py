from flask import Flask

app = Flask(__name__)
app.secret_key = 'Not meant to run on public internet'

from app import views
#from app import admin_views
