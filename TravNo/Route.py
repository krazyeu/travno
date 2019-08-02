from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from TravNo.Models import User, Info, Sub_User
from TravNo import app, db, bcrypt
from TravNo.Form import RegistrationForm, LoginForm, SetupForm, WhoForm, who_login
from PIL import Image
import pandas as pd
import random
import json
import datetime

country_code = pd.read_csv('/Users/D3m0cr0/Downloads/lists_of_iso_3166-1_codes_of_countries-2360j.csv',encoding = 'unicode_escape'
, index_col="Full Name")

sub_user = Sub_User.query.all()
print(sub_user)

@app.route("/")
@app.route("/home")
def home():
    form = SetupForm()
    return render_template('home.html', form=form)

@app.route("/about")
def about():
    return render_template('cities.html', title='About')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("itinerary", iti_code=current_user.iti_code))
    form = RegistrationForm()
    if form.validate_on_submit():
        if country_code[country_code.index == form.depart.data].index.tolist():
            if country_code[country_code.index == form.arr.data].index.tolist():
                db.create_all()
                iti_code = country_code.loc[form.depart.data, "Alpha-3 code"] + \
                           country_code.loc[form.arr.data, "Alpha-3 code"] + str(random.randrange(1000,9999))
                hashed_password = bcrypt.generate_password_hash(form.code.data).decode('utf-8')
                user = User(iti_code=iti_code, email=form.email.data, departure=form.depart.data, arrival=form.arr.data,
                            code=hashed_password)
                db.session.add(user)
                db.session.commit()
                print(iti_code, form.code.data)
                flash('Itinerary Code has been created!', 'success')
                return redirect(url_for('login'))
            else:
                flash("Opp's only enter Country name", 'danger')
        else:
            flash("Opp's only enter Country name", 'danger')
    return render_template('register.html' , title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("itinerary", iti_code=current_user.iti_code))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(iti_code=form.iti_code.data).first()
        if user and bcrypt.check_password_hash(user.code, form.code.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('profile'))
        else:
            flash("Entered either wrong Itinerary or Code", 'danger')
    return render_template('login.html' , title="Login", form=form)

@app.route("/login/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if db.session.query(Sub_User.name).filter_by(iti_code=current_user.iti_code):
        form = who_login()
        if form.validate_on_submit():
            if current_user.iti_code in db.session.query(Sub_User.iti_code).filter_by(iti_code=current_user.iti_code).first():
                return redirect(url_for("set_up", iti_code=current_user.iti_code))
            else:
                return redirect(url_for("itinerary", iti_code=current_user.iti_code))
        return render_template('profile.html', title="Choose Profile", form=form)
    else:
        redirect(url_for('who'))

@app.route("/login/create_profile", methods=["GET","POST"])
@login_required
def who():
    form = WhoForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.create_all()
        iti_code = current_user.iti_code
        name = form.name.data
        email = form.email.data
        sub_user = Sub_User(iti_code=iti_code, name=name, email=email)
        db.session.add(sub_user)
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template('Who_reg.html', title="Create Profile", form=form)

@app.route("/set_up/<iti_code>", methods=["GET", 'POST'])
@login_required
def set_up(iti_code):
        iti_code1 = db.session.query(Info.iti_code).filter_by(iti_code=current_user.iti_code).first()
        if current_user.iti_code in iti_code1:
            return redirect(url_for('itinerary', iti_code=current_user.iti_code))
        else:
            form = SetupForm()
            if form.validate_on_submit():
                db.create_all()
                iti_code = current_user.iti_code
                start_travel = form.start_travel.data
                end_travel = form.end_travel.data
                departure_airport = form.depart_airport.data
                arr_airport = form.arrival_airport.data
                pax = form.pax.data
                flight_tix = form.flight_tix.data
                accommodation = form.accommodation.data
                accom_style = form.style_accommodation.data
                info = Info(iti_code=iti_code, start_travel=start_travel, end_travel=end_travel, departure_airport=departure_airport,
                            arr_airport=arr_airport, pax=pax, flight_tix=flight_tix, accommodation=accommodation, accom_style=accom_style)
                db.session.add(info)
                db.session.commit()
                flash('Information has been added successfully', 'success')
                return redirect(url_for('itinerary', iti_code=current_user.iti_code))
        return render_template('setup.html' , title="Information page", form=form)

@app.route("/itinerary")
@login_required
def bypass():
    return redirect(url_for('itinerary', iti_code=current_user.iti_code))

@app.route("/itinerary/<iti_code>", methods=['GET','POST'])
@login_required
def itinerary(iti_code):
    return render_template('itinerary.html', title=current_user.iti_code)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))