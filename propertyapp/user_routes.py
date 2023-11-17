import json
from functools import wraps
from flask import render_template,request,abort,redirect,flash, make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
#local imports
from propertyapp import app,csrf,mail
from propertyapp.models import db,User,Category,State,Lga,Reviews,Property,Agent
from propertyapp.forms import *
@app.route('/user/details/<id>')
def pro_details(id):
    pro=Property.query.get_or_404(id)
    
    return render_template("user/prodetails.html",pro=pro)


@app.route("/user/proall/")
def proall():
   pros=db.session.query(Property.property_status=="1").all()
   return render_template("user/propertylist.html",pros=pros)
@app.route("/user/dashboard/")
def dashboard():
    return render_template("user/dashboard.html")
@app.route("/user/chgpwd/")
def changepassword():
    return render_template("user/changepassword.html")
@app.route("/user/contactus/")
def contactus(): 
    return render_template("user/contact.html")

@app.route("/")
def home():
    pros=db.session.query(Property).filter(Property.property_status=="1").limit(4).all()

    return render_template("user/homepage.html",pros=pros)
@app.route("/logout")
def logout():
    if session.get('userloggedin')!=None:
        session.pop('userloggedin',None)
    return redirect("/")
@app.route("/user/profile", methods=["GET","POST"])
def myprofile():
    id= session.get("userloggedin")
    userdeets=db.session.query(User).get(id)
    pform =ProfileForm()
    if request.method=="GET":
        return render_template('user/myprofile.html',pform=pform,userdeets=userdeets)
    else:
        if pform.validate_on_submit():
             fullname=request.form.get('fullname')
             email=request.form.get('email')
             userdeets.user_fullname=fullname
             userdeets.user_email=email
             db.session.commit()
             flash("Profile Updated Successfully!", category="success")
             return redirect(url_for("dashboard"))
        else:
            return render_template("user/myprofile.html",pform=pform,userdeets=userdeets)

@app.route("/user/login/", methods=['POST','GET'])
def login():
    if request.method=="GET":
        return render_template('user/userloginpage.html')
    else:
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        deets=db.session.query(User).filter(User.user_email==email).first()
        if deets != None:
            hashed_pwd =deets.user_pwd
            if check_password_hash(hashed_pwd,pwd)==True:
                session['userloggedin']=deets.user_id
                return redirect('/user/dashboard')
            else:
                flash('Invalid credentials, try again',category="error")
                return redirect('/user/login/')
        else:
            flash('Invalid credentials, try again',category='error')
            return redirect('/user/login/')

@app.route("/user/userreg/", methods=['GET','POST'])
def register():
    regform=UserRegForm()
    if request.method=='GET':
        return render_template('user/usersignup.html',regform=regform)
    else:
        if regform.validate_on_submit():
             fullname=request.form.get('fullname')
             email=request.form.get('email')
             pwd=request.form.get('pwd')
             
             hashed_pwd=generate_password_hash(pwd)

             
             u =User(user_fullname=fullname,user_email=email,user_pwd=hashed_pwd)
            #  user_pwd=hashed_pwd
             db.session.add(u)
             db.session.commit()
             flash(f"{fullname} account has been created for you.Please login!",category="success")
             return redirect(url_for('login'))
        
        else:
            return render_template('user/usersignup.html',regform=regform)
    # regform=RegForm()
    # return render_template('user/signup.html',regform=regform)
