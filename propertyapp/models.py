from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from itsdangerous import URLSafeTimedSerializer as Serializer
from propertyapp import *


db=SQLAlchemy()
class State(db.Model):
    state_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name=db.Column(db.String(20),nullable=False)
    #set relationship: using backref means that you dont have to set relationship on the second table (lga)
    lgas = db.relationship("Lga",backref='state_deets')
class Lga(db.Model):
    lga_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_id= db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)  
    lga_name=db.Column(db.String(20),nullable=False)

class Property(db.Model):
    property_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    property_title = db.Column(db.Text(),nullable=False)
    property_desc = db.Column(db.Text())
    property_cover = db.Column(db.String(100))
    property_publication =db.Column(db.Date()) 
    property_catid = db.Column(db.Integer, db.ForeignKey('category.cat_id'),nullable=False)  
    property_status =db.Column(db.Enum('1','0'),nullable=False, server_default=("0"))  
    property_type=db.Column(db.Text(),nullable=False)
    property_beds=db.Column(db.String(10),nullable=True)
    property_baths=db.Column(db.String(10),nullable=True)
    property_garage=db.Column(db.String(10),nullable=True)
    property_location=db.Column(db.Text()) 
    property_price=db.Column(db.String(120),nullable=True)
   # property_agentid = db.Column(db.Integer, db.ForeignKey('property_agentid'), nullable=False)
    
    property_agentid = db.Column(db.Integer, db.ForeignKey('agent.agent_id'))

    #set relationships
    catdeets = db.relationship("Category", back_populates="propertydeets")
    

class Category(db.Model):
    cat_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    cat_name=db.Column(db.String(20),nullable=False) 
    #set relationship
    propertydeets = db.relationship("Property", back_populates="catdeets")

class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(20),nullable=True)

class User(db.Model):  
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fullname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120),unique=True) 
    user_pwd=db.Column(db.String(120),nullable=True)
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)#default 
    
    #set relationship    
    user_reviews=db.relationship("Reviews",back_populates='reviewby') 
    def get_token(self,expires_sec=3600):
        serial = Serializer(app.config['SECRET_KEY'],expires_sec)
        return serial.dumps({'user_id:user.user_id'}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        serial =Serializer(app.config['SECRET_KEY'])
        try:
            user_id=serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Reviews(db.Model):
    rev_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    rev_title = db.Column(db.String(255),nullable=False)
    rev_text = db.Column(db.String(255),nullable=False)
    rev_date =db.Column(db.DateTime(), default=datetime.utcnow)
    rev_userid = db.Column(db.Integer, db.ForeignKey('user.user_id'))  
    rev_agentid =db.Column(db.Integer, db.ForeignKey('agent.agent_id'))  
    
    #set relationships
    reviewby = db.relationship("User", back_populates="user_reviews")
    thepro = db.relationship("Agent", back_populates="agentreviews")   

class Agent(db.Model):
    agent_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    agent_fullname = db.Column(db.String(100),nullable=False)
    agent_email = db.Column(db.String(120)) 
    agent_pwd=db.Column(db.String(120),nullable=True)
    agent_pix=db.Column(db.String(120),nullable=True) 
    agent_datereg=db.Column(db.DateTime(), default=datetime.utcnow)#default 
    agent_phoneno=db.Column(db.String(120),nullable=True)
    agent_no=db.Column(db.String(120),nullable=True)
    agent_location=db.Column(db.String(120),nullable=True)
    #set relationhips
    properties = db.relationship('Property', backref='agent', lazy=True)
    agentreviews = db.relationship("Reviews", back_populates="thepro",cascade="all, delete-orphan")
   # props = db.relationship('Property', backref='agent')
