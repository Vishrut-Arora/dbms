from app import app,db
from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages, request
from datetime import datetime
import forms
from modules.db import connect_to_db
from datetime import datetime 


@app.route('/')
@app.route('/index', methods = ['GET',])
def index():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods= ['GET', 'POST'])
def register():
    form = forms.AddUserForm()
    print(request.form)
    # print(request.json.get('na
    # me'))
    for i in request.form:
        print(request.form[i])
    # print(request.args)
    # if form.validate_on_submit():
    try:
        name = request.form['name']
        cur = connect_to_db()
        print("before")
        cur.execute(f"""
            create user "{name}_{request.form['designation']}" with password '{name}';
            Grant all on "User" to '{name}_{request.form['designation']}';
            INSERT INTO "User" ("Name","Age","EmailID","Gender","Designation","Password","LastLogin","Admin","Contact") 
            VALUES ('{name}, {request.form['age']} ,'{request.form['email']}', {request.form['gender']}, {request.form['designation']}, {request.form['password']}, '{datetime.now()}', false, {request.form['contact']});
        """)
        print("after")
        cur.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return render_template('signup.html', form=form)

@app.route('/student')
def student():
    return render_template('users.html')
