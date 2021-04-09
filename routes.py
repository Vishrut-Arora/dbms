from app import app,db
from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages, request
from datetime import datetime
import forms
from modules.db import connect_to_db
from datetime import datetime 


@app.route('/')
@app.route('/index', methods = ['GET',])
def index():
    name = "Sudeeep"
    return render_template('parents.html', name = name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods= ['GET', 'POST'])
def register():
    print("start")
    form = forms.AddUserForm()
    print(request.form)
    # print(request.json.get('na
    # me'))
    for i in request.form:
        print(request.form[i])
    print(request.method)
    try:
        name = request.form['name']
        cur = connect_to_db()
        print("befor")
        
        cur.execute(f"""
            create user "{name}_{request.form['designation']}" with password '{name}';
            Grant all on "User" to "{name}_{request.form['designation']}";
            INSERT INTO "User" ("Name","Age","EmailID","Gender","Designation","Password","LastLogin","Admin","Contact") 
            VALUES ('{name}', {request.form['age']} ,'{request.form['email']}', {request.form['gender']}, {request.form['designation']}, {request.form['password']}, '{datetime.now()}', false, {request.form['phone']});
        """)
        print("after")
        cur.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        name = "Sudeep"
    return render_template('signup.html', form=form, name = name)

@app.route('/student')
def student():
    return render_template('users.html')

@app.route('/professor',methods= ['GET', 'POST'])
def professorQueries():
    form=forms.AddUserForm()
    result=request.form
    # Mentors Stuff starts
    if("mentors-submits" in result):
        print("in mentors-submits")
        print(result)
        try:
            cur = connect_to_db()
            print("befor")
            cur.execute(f"""
            Select "UserId" from "Professor"
            Where "EmployeeId" In (
            Select "MentorId" from "Project"
	            where "ProjectId"={result['Mentor-Project']}
            );
            """)
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    # education related quesries
    if("education-submit" in result):
        print("in education-submit")
        print(result)
        educationID=result["educationID"]
        professorID=result["professorID"]
        if(result["operation"]=="Insert"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                INSERT INTO "Attended_Professor" ("EducationId","ProfessorId") VALUES ({educationID},{professorID})
                """)
                
                cur.close()
            except Exception as e:
                print(e)
        if(result["operation"]=="Update"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                UPDATE "Attended_Professor" 
                SET "EducationId"={educationID}
                Where "ProfessorId"={professorID}

                """)
                
                cur.close()
            except Exception as e:
                print(e)
        if(result["operation"]=="Delete"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                Delete from "Attended_Professor" 
                Where "ProfessorId" ={professorID} and "EducationId"={educationID};

                """)
                
                cur.close()
            except Exception as e:
                print(e)
    # Adding projects
    if("addProject-submit" in result):
        print("in addProject-submit")
        print(result)
        try:
            cur = connect_to_db()
            print("befor")
        
            cur.execute(f"""
            INSERT INTO "Project" ("ProjectId","Title","MentorId","Duration","StartDate","EndDate","Field","Domain") VALUES 
	        ({result['AprojectID']},'{result['Title']}',{result['EmployeeId']},'{result['Duration']}','{result['StartDate']}',null,'{result['Field']}','{result['Domain']}')
            """)
            cur.execute("""Select * from "Project" """)
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    return render_template('professor.html')
