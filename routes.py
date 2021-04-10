from app import app, db
from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages, request
from datetime import datetime
import forms
from modules.db import connect_to_db
from datetime import datetime


@app.route('/')
@app.route('/index', methods=['GET', ])
def index():
    name = "Sudeeep"
    return render_template('base.html', name=name)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
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
    return render_template('signup.html', form=form, name=name)


@app.route('/student')
def student():
    return render_template('users.html')

@app.route('/parent',methods=['GET', 'POST'])
def parentQueries():
    result=request.form
    x=""
    try:
        cur=connect_to_db()
        cur.execute(f""" select * from "Achievement"
        where "StudentId" in (
        Select "RollNo" from "Student"
	        where "ParentId"='{result['parentdID']}'
        );
        """)
        x=cur.fetchall()
        cur.close()
    except Exception as e:
        print(e)
    return render_template('parents.html',achievements=x)

@app.route('/professor', methods=['GET', 'POST'])
def professorQueries():
    result = request.form
    mentor=""
    studentWorkingProjects=""
    projectsUnderStudents=""
    studentGPA=""
    if('assignStudent' in result):
        try:
            cur=connect_to_db()
            cur.execute(f""" Insert into "Indulged" ("ProjectId", "StudentId") values ({result['projectID']},{result['rollno']})""")
            cur.close()
        except Exception as e:
            print(e)
    if("project_underStudent" in result):
        print(" inproject_underStudent")
        print(result)
        if(result['rollnoGPA'] != ''):
            try:
                cur = connect_to_db()
                cur.execute(
                    f"""Select  "GPA" from "Student" where "RollNo" = {result['rollnoGPA']};""")
                studentGPA=cur.fetchall()
                # print(cur.fetchall())
                cur.close()
            except Exception as e:
                print(e)
        
        if(result['rollnoPID'] != ''):
            try:
                cur = connect_to_db()
                cur.execute(f"""select "Title" from "Project" 
where "ProjectId" in(
Select "ProjectId" from "Indulged"
Where "StudentId"= {result['rollnoPID']} 
);
""")
                studentWorkingProjects=cur.fetchall()
                
                cur.close()
            except Exception as e:
                print(e)
        try:
            cur = connect_to_db()
            if(result['projectID'] != ''):
                cur.execute(f"""
            select * from "Student"
                Where "RollNo" in (
            Select "StudentId" from "Indulged"
	            Where "ProjectId"={result['projectID']}
                );
                """)
            projectsUnderStudents=cur.fetchall()
            cur.close()
        except Exception as e:
            print(e)
    ##########################Mentor Stuff##################
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
            mentor=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    ################################# education related quesries####################
    if("education-submit" in result):
        print("in education-submit")
        print(result)
        educationID = result["educationID"]
        professorID = result["professorID"]
        if(result["operation"] == "Insert"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                INSERT INTO "Attended_Professor" ("EducationId","ProfessorId") VALUES ({educationID},{professorID})
                """)

                cur.close()
            except Exception as e:
                print(e)
        if(result["operation"] == "Update"):
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
        if(result["operation"] == "Delete"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                Delete from "Attended_Professor" 
                Where "ProfessorId" ={professorID} and "EducationId"={educationID};

                """)

                cur.close()
            except Exception as e:
                print(e)
    ######################################### Adding projects####################################
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

######################################################################################
@app.route('/Sports_Cultural',methods= ['GET', 'POST'])
def professorQueries2():
    form=forms.AddUserForm()
    result=request.form

    if("Achievement-submit" in result):
        print("in Achievement-submit")
        print(result)
        studentID=result["studentID"]
        title=result["title"]
        proof=result["proof"]

        if(result["operation"]=="Update"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                UPDATE "Achievement"  
                SET "Proof"={proof}
                Where "StudentId"={studentID} AND "Title"={title} AND "Technical"=false 

                """)
                
                cur.close()
            except Exception as e:
                print(e)
        if(result["operation"]=="Delete"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                Delete from "Achievement" 
                Where "StudentId" ={studentID} and "Title"={title};

                """)
                
                cur.close()
            except Exception as e:
                print(e)
    if("Search-submit" in result):
        if(result["operation2"]=="By StudentId"):
            studentID=result["studentID"]
            try:
                cur = connect_to_db()
                print("befor")
                cur.execute(f"""
                Select * from "Achievement"
                Where "StudentId"={studentID} AND "Technical"=false 
                """)
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)

        if(result["operation2"]=="By Title"):
            title=result["title"]
            try:
                cur = connect_to_db()
                print("befor")
                cur.execute(f"""
                Select * from "Achievement"
                Where "Title"={title} AND "Technical"=false 
                """)
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)

        if(result["operation2"]=="By Institution"):
            institution=result["institution"]
            try:
                cur = connect_to_db()
                print("befor")
                cur.execute(f"""
                Select * from "Achievement"
                Where "Institution"={institution} AND "Technical"=false 
                """)
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)

    return render_template('Sports_Cultural.html')

############################
    return render_template('professor.html',mentor=mentor,studentGPA=studentGPA,projectsUnderStudents=projectsUnderStudents,studentWorkingProjects=studentWorkingProjects)
