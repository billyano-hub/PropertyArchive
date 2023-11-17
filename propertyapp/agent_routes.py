import json,random,string,os
from functools import wraps
from flask import render_template,request,abort,redirect,flash, make_response,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
#local imports
from propertyapp import app,csrf,mail
from propertyapp.models import db,User,Category,State,Lga,Reviews,Property,Agent
from propertyapp.forms import *

    
@app.route("/agent/edit/property/<id>", methods=["GET","POST"])
def editpro(id):
     if session.get("agentloggedin")==None:
        return redirect(url_for('log'))
     else:
        if request.method=="GET":
            deets=db.session.query(Property).filter(Property.property_id==id).first_or_404(id)
            # deets=db.session.query(property).get_or_404(id)
            cats=db.session.query(Category).all()
            return render_template("agent/edit_pro.html",deets=deets,cats=cats)
        else:#in order to update the property details,
            property_2update=Property.query.get(id)
            current_filename=property_2update.property_cover#name of the old cover
            # retrieve form data here..
            property_2update.property_title=request.form.get('title')
            property_2update.property_catid=request.form.get('category')
            property_2update.property_status=request.form.get('status')
            property_2update.property_desc=request.form.get('description')
            property_2update.property_publication=request.form.get('yearpub')

            cover=request.files.get('cover')
            #check if file was selected for upload
            if cover.filename != "":
                #let the file name remain the same on the db
                name,ext=os.path.splitext(cover.filename)
                if ext.lower() in ['.jpg','.png','.jpeg']:
                    #uploas the fileits allowed
                    newfilename=generate_string(10) + ext
                    cover.save("propertyapp/static/uploads/"+newfilename)
                    # if filename !=None and filename !='default.png' and os.path.isfile("propertyapp/static/uploads/"+filename):
                    #os.remove("propertyapp/static/uploads/"+current_filename)
                    #delete current filename here writing a query!important
                    property_2update.property_cover=newfilename
                else:
                    flash("The extension of the property cover wasnt included")
            db.session.commit()
            flash('property details was updated')
            return redirect("/agent/prolist/")
def generate_string(howmany):
    x=random.sample(string.ascii_lowercase,howmany)
    return ''.join(x)
@app.route("/admin/delete/<id>/")
def property_delete(id):
    property=db.session.query(Property).get_or_404(id)
    #lets get the name of the file attached to this property
    filename=property.property_cover
    #first delete the file before deleting the property from db
    if filename !=None and filename !='default.png' and os.path.isfile("propertyapp/static/uploads/"+filename):
        os.remove("propertyapp/static/uploads/"+filename)#import os at the top
    db.session.delete(property)
    db.session.commit()
    flash("property has been deleted!")
    return redirect(url_for("prolist"))
@app.route("/agent/prolist/")
def prolist():
    if session.get("agentloggedin")==None:
        return redirect(url_for('log'))
    else:
    
        pros = db.session.query(Property).all()
        return render_template("agent/propertylist.html",pros=pros)
@app.route('/agent/addpro',methods=['GET','POST'])
def addpro():
    if session.get("agentloggedin")==None:#means he is not logged in'
        return redirect(url_for('log'))
    else:
        if request.method=="GET":
            deets=db.session.query(Property).filter(Property.property_status).first_or_404()

            cats=db.session.query(Category).all()
            return render_template("agent/addpro.html",cats=cats,deets=deets)
        else:
            # retrieve file
            allowed=['jpg','png']
            filesobj=request.files['cover'] 
            filename=filesobj.filename 

            newname='default.png' #default cover
            if filename=='':
                flash("Property Cover not included",category='error')
            else:#file was selected
                pieces=filename.split('.')
                ext=pieces[-1].lower()
                if ext in allowed:
                    newname=str(int(random.random()*1000000000))+ filename #to make sure it is random

                    filesobj.save("propertyapp/static/uploads/"+newname)
                else:
                    flash("File extension not allowed, file was not uploaded", category='error')
                 
            # retrieve all the form data
            title=request.form.get('title')
            category=request.form.get('category')
            status=request.form.get('status')
            description =request.form.get('description')
            yearpub=request.form.get('yearpub')
            newname=request.form.get('cover')
            type=request.form.get('type')
            beds=request.form.get('beds')
            baths=request.form.get('baths')
            garage=request.form.get('garage')
            location=request.form.get('location')
            price=request.form.get('price')

            pro=Property(property_type=type,property_beds=beds,property_baths=baths,property_garage=garage,property_location=location,property_price=price,property_cover=newname,property_status=status,property_title=title,property_desc=description,property_publication=yearpub,property_catid=category)
            db.session.add(pro)
            db.session.commit()
            if pro.property_id:
                flash(" Property added successfully!")
            else:
                flash("Please try again")
            #  return 'done'
            return redirect(url_for("addpro"))
@app.route("/agent/profile", methods=["GET","POST"])
def agentprofile():
    id= session.get("agentloggedin")
    agentdeets=db.session.query(Agent).get(id)
    apform =AgentProfileForm()
    if request.method=="GET":
        return render_template('agent/agentmyprofile.html',apform=apform,agentdeets=agentdeets)
    else:
        if apform.validate_on_submit():
             fullname=request.form.get('fullname')
             email=request.form.get('email')
             agentdeets.user_fullname=fullname
             agentdeets.user_email=email
             db.session.commit()
             flash("Profile Updated Successfully!", category="success")
             return redirect(url_for("agentdashboard"))
        else:
            return render_template("agent/agentmyprofile.html",apform=apform,agentdeets=agentdeets)

@app.route("/agent/dashboard/")
def agentdashboard():
    return render_template("agent/agentdashboard.html")
@app.route("/agent/chgpwd/")
def agentcnangepassword():
    return render_template("agent/agentchgpassword.html")

@app.route("/agent/logout")
def agentlogout():
    if session.get('agentloggedin')!=None:
        session.pop('agentloggedin',None)
    return redirect("/")
# @app.route("/agent/profile", methods=["GET","POST"])
# def agentprofile():
#     id= session.get("agentloggedin")
#     agentdeets=db.session.query(Agent).get(id)
#     agentpform =AgentProfileForm()
#     if request.method=="GET":
#         return render_template('agent/agentprofile.html',agentpform=agentpform,agentdeets=agentdeets)
#     else:
#         if agentpform.validate_on_submit():
#              fullname=request.form.get('fullname')
#              email=request.form.get('email')
#              agentdeets.agent_fullname=fullname
#              agentdeets.agent_email=email
#              db.session.commit()
#              flash("Profile Updated Successfully!", category="success")
#              return redirect(url_for("agentdashboard"))
#         else:
#             return render_template("agent/agentprofile.html",agentpform=agentpform,agentdeets=agentdeets)


@app.route("/agent/login/", methods=['POST','GET'])
def log():
    if request.method=="GET":
        return render_template('agent/agentloginpage.html')
    else:
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        deets=db.session.query(Agent).filter(Agent.agent_email==email).first()
        if deets != None:
            hashed_pwd =deets.agent_pwd
            if check_password_hash(hashed_pwd,pwd)==True:
                session['agentloggedin']=deets.agent_id
                return redirect('/agent/dashboard/')
            else:
                flash('Invalid credentials, try again',category="error")
                return redirect('/agent/login/')
        else:
            flash('Invalid credentials, try again',category='error')
            return redirect('/agent/login/')



@app.route("/agent/agentreg/", methods=['GET','POST'])
def signup():
    agform=AgentRegForm()
    if request.method=='GET':
        return render_template("agent/agentsignup.html",agform=agform)
    else:
        if agform.validate_on_submit():
             fullname=request.form.get('fullname')
             email=request.form.get('email')
             pwd=request.form.get('pwd')
             
             hashed_pwd=generate_password_hash(pwd)

             
             a =Agent(agent_fullname=fullname,agent_email=email,agent_pwd=hashed_pwd)
            #  user_pwd=hashed_pwd
             db.session.add(a)
             db.session.commit()
             flash(f"{fullname.capitalize()} account has been created for you.Please login",category="success")
             return redirect(url_for('log'))
        
        else:
            return render_template('agent/agentsignup.html',agform=agform)
    # regform=RegForm()
    # return render_template('user/signup.html',regform=regform)
