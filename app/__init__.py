from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_toastr import Toastr

app = Flask(__name__, template_folder='../Template', static_folder='../static')
app.debug = True

app.config['SECRET_KEY']='ded0cbf553959a5be4b0e6755c6997f5'
app.secret_key="super secret key"

#Toast Messaging

toastr = Toastr(app)

#DB connection for model migrations

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/renumeration_bill'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#import Models form models.py

from Models.models import SubjectInformation,FacultyInformation,ExaminationBills

from app import views
from app.views import index

#Creating Blueprints

app.register_blueprint(index)

#Add your models to the migration context
migrate.init_app(app,db)