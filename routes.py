from app import app,db
from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages
from datetime import datetime
import forms
from modules.db import connect_to_db


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
    if form.validate_on_submit():
        name = form.name.data
        cur = connect_to_db()
        # cur.execute(f"""
        #     create user "{name}" with password '{name}';
        # """)
        cur.execute(f"""
            SELECT usename AS role_name,
              CASE 
                 WHEN usesuper AND usecreatedb THEN 
            	   CAST('superuser, create database' AS pg_catalog.text)
                 WHEN usesuper THEN 
            	    CAST('superuser' AS pg_catalog.text)
                 WHEN usecreatedb THEN 
            	    CAST('create database' AS pg_catalog.text)
                 ELSE 
            	    CAST('' AS pg_catalog.text)
              END role_attributes
            FROM pg_catalog.pg_user
            ORDER BY role_name desc;
        """)
        print(cur.fetchall())
        cur.close()
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/student')
def student():
    return render_template('users.html')
