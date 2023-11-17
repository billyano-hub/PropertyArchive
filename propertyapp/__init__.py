from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail

mail=Mail()
csrf=CSRFProtect()

#instantiate an object of flask
def create_app():
    """keep all imports that may cause conflict within 
    this function so that anythime we write "
    from pkg.. import... none of these statements will be eexecuted"""
    from propertyapp.models import db
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile("config.py",silent=True)
    db.init_app(app)
    migrate=Migrate(app,db)
    csrf.init_app(app)
    return app

app=create_app()


#load the route here

from propertyapp import admin_routes,user_routes,agent_routes
from propertyapp.forms import *