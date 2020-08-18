from flask import render_template, url_for, flash, redirect
from green_corridor.forms import LoginForm, NewDriver, PlaceCordinate   
from green_corridor import app, db #, bcrypt #, login_manager
#from flask_login import UserMixin
from google.cloud.firestore import GeoPoint
from flask import session 
import os
import json

#from flask_login import login_user, current_user, logout_user, login_required

# @login_manager.user_loader   
# def load_user(user_id):
#     return db.collection('Admin').document(user_id).get().to_dict()

app.secret_key=os.urandom(24) 



@app.route("/",methods=['GET', 'POST'])
def login():
    if 'user' not in session:
        form = LoginForm()
        if form.validate_on_submit():
            temp = db.collection('Admin').document(form.username.data).get().to_dict()
            if temp and temp['password']==form.password.data:
                #login_user(form.username.data,remember=form.remember.data)
                #if request.method == 'POST':
                session['user']=form.username.data 
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)
    else:
        return redirect(url_for('home'))
   
@app.route("/home")
def home():
    if 'user' in session: 
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route("/driverManagement",methods=['GET', 'POST'])
def driverManagement():
    form = NewDriver()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.assign_password.data).decode('utf-8')
        doc_ref = db.collection('Driver')
        doc_ref.document(form.email.data).set({
            'd_name':form.name.data,
            'd_mobile':form.mobile_no.data,
            #'Location': GeoPoint(0, 0),
            'd_latitude':'0',
            'd_longitude':'0',
            'p_email':'',
            #'d_password': hashed_password ,
            'd_password': form.assign_password.data,
        })  # insert with 'email' document name (override if already exist)
        flash(f'Account with username "{form.name.data}" created successfully!', 'success')
        return redirect(url_for('driverManagement'))     
    doc_ref = db.collection('Driver')
    doc=[]
    for i in doc_ref.get():
        doc.append(i.to_dict())
        doc[-1]['d_email'] = i.id
    return render_template('driverManagement.html', form=form, docs=doc)

@app.route('/createGreenCorridor')
def createGreenCorridor():
    if 'user' in session:
        form=PlaceCordinate()
        if form.validate_on_submit():   
            url_source=f"https://maps.googleapis.com/maps/api/geocode/json?address={form.source.data}&key=AIzaSyB5InCXr1LJmo9xOvoLX21AanL2bImGPoU"
            url_destination=f"https://maps.googleapis.com/maps/api/geocode/json?address={form.destination.data}&key=AIzaSyB5InCXr1LJmo9xOvoLX21AanL2bImGPoU"
            data_source = requests.get(url_source).text
            data_source = json.loads(data_source)
            data_destination = requests.get(url_destination).text
            data_destination = json.loads(data_destination)
            [source_latitude,source_longitude]=[data_source["results"][0]["geometry"]["location"]["lat"],data_source["results"][0]["geometry"]["location"]["lng"]]
            [destination_latitude,destination_longitude]=[data_destination["results"][0]["geometry"]["location"]["lat"],data_destination["results"][0]["geometry"]["location"]["lng"]]

            #

        return render_template('createGreenCorridor.html',form=form)
    else:
        return redirect(url_for('login'))       

@app.route("/piManagement")
def piManagement():
    if 'user' in session: 
        return render_template('piManagement.html')
    else:
        return redirect(url_for('login'))

@app.route("/patientManagement")
def patientManagement():
    if 'user' in session:
        return render_template('patientManagement.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user', None)
   return redirect(url_for('login'))    





#user is  session key  


# return redirect(url_for('www'))

# @app.route('/welcome')
# def www():
#     return render_template('www.html')