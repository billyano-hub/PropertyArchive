import json,bcrypt
from functools import wraps
from flask import render_template,request,abort,redirect,flash, make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Message


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
   pros=db.session.query(Property).filter(Property.property_status=="1").all()
#    pros=db.session.query(Property.property_status=="1").all()
   return render_template("user/propertylist.html",pros=pros)


@app.route("/user/contactus/")
def contactus(): 
    return render_template("user/contact.html")

@app.route("/")
def home():
    pros=db.session.query(Property).filter(Property.property_status=="1").limit(10).all()

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
        

@app.route('/user/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # If the user is already logged in, redirect them to another page
        if session.get('userloggedin'):
            return redirect('/user/dashboard')
        return render_template('user/userloginpage.html')
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
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
            flash('Invalid credentials, try again', category='error')
            return redirect('/user/login/')
        

@app.route('/user/dashboard')
def dashboard():
    if session.get('userloggedin'):
        return render_template('/user/dashboard.html')
    flash('Please log in first.', category='info')
    return redirect('/user/login/')


def send_email(user):
    token=user.get_token()
    msg=Message('Password Reset Request',recipients=[user.user_email],sender="ayodejiowoseni001@gmail.com")
    msg_body=f''' 
        To reset your password, follow the link below.

    {url_for('reset_token',token=token,_external=True)}

    please if you didn't send a password request, kindly ignore this mail.

'''
@app.route("/reset_password", methods=['GET', 'POST'])
def forgot_password():
    resform =ResetRequestForm()
    if resform.validate_on_submit():
        user=User.query.filter_by(user_email=resform.email.data).first_or_404()
        if user:
            try:
                send_email(user)
                flash("Reset request sent, Check your mail", 'Success')
                return redirect(url_for('login'))
            except:
                return (url_for ('forgot_password'))
    
    return render_template('/user/resetrequest.html',resform=resform)  # Display the form

@app.route("/rest_password<token>", methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user==None:
        flash('That is invalid token, please try again','warning')
        return redirect(url_for('forgot_password'))

    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit
        flash('pasword changed!','success')
        return redirect(url_for('login'))
    return render_template('/user/changepassword.html',form=form)



@app.route("/user/userreg/", methods=['GET','POST'])
def register():
    regform=UserRegForm()
    if request.method=='GET':
        if session.get('userloggedin'):
            return redirect('/user/dashboard')
        return render_template('user/usersignup.html',regform=regform)
    else:
        if regform.validate_on_submit():
             fullname=request.form.get('fullname')
             email=request.form.get('email')
             pwd=request.form.get('pwd')


             # Check if the email already exists in the database
             existing_user = User.query.filter_by(user_email=email).first()
             if existing_user:
                flash("Email already exists! Please log in.", category='info')
                return render_template('agent/agentsignup.html', agform=agform)

             hashed_pwd = generate_password_hash(pwd)
             new_user = User(user_fullname=fullname, user_email=email, user_pwd=hashed_pwd)
             db.session.add(new_user)
             db.session.commit()
             
             
             flash(f"{fullname} account has been created for you.Please login!",category="success")
             return redirect(url_for('login'))
        
        else:
            flash("Invalid form data. Please try again.", category='danger')
            return render_template('user/usersignup.html',regform=regform)
    # regform=RegForm()
    # return render_template('user/signup.html',regform=regform)
        
    
