from flask import render_template,request,abort,redirect,flash, make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash


# local imports
from propertyapp import app,csrf
from propertyapp.models import db,Admin,User,Agent
from propertyapp.forms import *

@app.route("/admin/delet/<id>/")
def agent_delete(id):
    
    agent=db.session.query(Agent).get_or_404(id)
   

    db.session.delete(agent)
    db.session.commit()
    flash("agent has been deleted!")
    return redirect(url_for("all_users"))

@app.route("/admin/delete/<id>/")
def user_delete(id):
    user=db.session.query(User).get_or_404(id)
    
   
    db.session.delete(user)

    db.session.commit()
    flash("user has been deleted!")
    return redirect(url_for("all_users"))

@app.route("/admin/users/")
def all_users():
    if session.get("adminuser")==None or session.get('role') !='admin':#means he is not logged in'
        return redirect(url_for('admin_login'))
    else:
    
        users = db.session.query(User).all()
        agents =db.session.query(Agent).all()
        return render_template("admin/allusers.html",users=users,agents=agents)
    
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("adminuser")==None or session.get('role') !='admin':#means he is not logged in'
        return redirect(url_for('admin_login'))
    else:
        return render_template('admin/admindashboard.html')


@app.route("/admin/logout")
def admin_logout():
    if session.get('adminuser') !=None: #he is still logged in
        session.pop('adminuser',None)
        session.pop('role',None)
        flash('You have logged out', category='info')
        return redirect(url_for('admin_login'))
    else:#she is logged out already
        return redirect(url_for("admin_login"))
@app.route("/admin/login/",methods=["POST","GET"])
def admin_login():
        if request.method=="GET":
                return render_template("admin/adminlogin.html")
        else:
                #retrieve form data
                username=request.form.get("username")
                pwd=request.form.get('pwd')
                #check if it is in database,
                check=db.session.query(Admin).filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
                #if it is in db, save in session and redirect to dashboard
                if check:#it is in db, save session
                        session["adminuser"]=check.admin_id
                        session['role']='admin'
                        return redirect(url_for("admin_dashboard"))
                else:#id=if not, save message in flash, redirect to login again
                        flash('Invalid Login',category='error')
                return render_template('admin/adminlogin.html')


       


@app.after_request
def after_request(response):
    #To solve he problem of loggedout user's details being cached in the browser
    response.headers['cache-control']='no-cache,no-store, must-revalidate'
    return response
