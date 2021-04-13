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
    print("This is request: ")
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
                cur.execute(f"""select * from "Project" 
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
            Select * from "Professor"
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
    return render_template('professor.html',mentor=mentor,studentGPA=studentGPA,projectsUnderStudents=projectsUnderStudents,studentWorkingProjects=studentWorkingProjects)


######################################################################################
#                                  SPORTS AND CULTURAL
######################################################################################
@app.route('/Sports_Cultural',methods= ['GET', 'POST'])
def Sports_Cultural_Queries():
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
######################################################################################
#                                  ACADEMIC
######################################################################################
@app.route('/Academic',methods= ['GET', 'POST'])
def Academic():
    studentDetails = ""
    form=forms.AddUserForm()
    result=request.form

    if("Academic-submit" in result):
        print("in Academic-submit")
        print(result)
        rollno=result["rollno"]
        gpa=result["gpa"]
        if(result["operation"]=="Update"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                UPDATE "Student"  
                SET "GPA"={gpa}
                Where "RollNo"={rollno} 

                """)
                
                cur.close()
            except Exception as e:
                print(e)
        if(result["operation"]=="Delete"):
            try:
                cur = connect_to_db()
                cur.execute(f"""
                UPDATE "Student"  
                SET "GPA"={0}
                Where "RollNo"={rollno}

                """)
                
                cur.close()
            except Exception as e:
                print(e)
    if("Search-submit" in result):
        if(result["operation2"]=="By Student Roll number"):
            rollno=result["rollno"]
            try:
                cur = connect_to_db()
                print("befor")
                cur.execute(f"""
                Select * from "Student"
                Where "RollNo"={rollno} 
                """)
                studentDetails = cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)

    return render_template('Academic.html', studentDetails = studentDetails)

#######################################################################################################################################
#                             RECRUITER
#######################################################################################################################################

@app.route('/Recruiter',methods=['GET', 'POST'])
def RecruiterQueries():
    result=request.form
    x=""
    y=""
    z=""
    u=""
    v=""
    a=""
    b=""
    d=""
    g=""
    f=""
    ##Finding GPA of particular student Query
    print(result)
    if("GPA" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select u."Name" ,s."RollNo", s."GPA" from "Student" as "s" , "User" as "u" where    s."RollNo" = '{result['RollNo']}' 
            and s."UserId" = u."EmailID" ; 
            """)
            x=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    ##Skills query
    if("Skills" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select "StudentId" from "Skill" where "Title" = '{result['Skill']}';
            """)
            y=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)

    ##Range of GPA with degree
    if("Student_under_Degree" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select u."Name", s."RollNo", s."Batch" from "Student" as "s","User" as "u" where s."GPA" >= '{result['GPAA']}' and s."UserId" = u."EmailID" and s."Degree" = '{result['Degree']}';
            """)
            z=cur.fetchall()
            u=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)

    if("Student_under_Degree" in result):
        print("before")
        print(result)
        if(result["Degree_Req1"] == "Bachelors"):
            try:
                cur=connect_to_db()
                cur.execute(f""" select u."Name", s."RollNo", s."Batch" from "Student" as "s","User" as "u" where s."GPA" >= '{result['GPAA']}' and s."UserId" = u."EmailID" and s."Degree" = 'Bachelors';
                """)
                
                u=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)            
        if(result["Degree_Req1"] == "Masters"):
            try:
                cur=connect_to_db()
                cur.execute(f""" select u."Name", s."RollNo", s."Batch" from "Student" as "s","User" as "u" where s."GPA" >= '{result['GPAA']}' and s."UserId" = u."EmailID" and s."Degree" = 'Masters';
                """)
                
                u=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)    
        if(result["Degree_Req1"] == "PHD"):
            try:
                cur=connect_to_db()
                cur.execute(f""" select u."Name", s."RollNo", s."Batch" from "Student" as "s","User" as "u" where s."GPA" >= '{result['GPAA']}' and s."UserId" = u."EmailID" and s."Degree" = 'PHD';
                """)
                u=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)            
        

        



    if("Skillset_Proof" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select * from "Skill" where "StudentId" = '{result['RollNo1']}';

            """)
            v=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)


    if("Verification_Proof" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select "StudentId","Title","Institution" from "Achievement" where "Proof" ='{result['Proof_Req']}' and "StudentId" = '{result['RollNo2']}';
            """)
            a=cur.fetchall()
            b=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    
    

    
    if("Project_under_Field" in result):
        print("before")
        print(result)
        
        if(result["Degree_Req"] == "Bachelors"):
            try:
                print("before")
                cur=connect_to_db()
                cur.execute(f""" select  u."Name" , s."RollNo" from "Student" as "s", "Indulged" as "i" ,"User" as "u", "Project" as "p" where p."Field" = '{result['Field1']}' and p."ProjectId" = i."ProjectId" and i."StudentId" = s."RollNo" and s."Degree" = 'Bachelors' and s."UserId" = u."EmailID";
                """)
                d=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)


        if(result["Degree_Req"] == "Masters"):
            try:
                print("before")
                cur=connect_to_db()
                cur.execute(f""" select  u."Name" , s."RollNo" from "Student" as "s", "Indulged" as "i" ,"User" as "u", "Project" as "p" where p."Field" = '{result['Field1']}' and p."ProjectId" = i."ProjectId" and i."StudentId" = s."RollNo" and s."Degree" = 'Masters' and s."UserId" = u."EmailID";
                """)
                d=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)
        
        if(result["Degree_Req"] == "PHD"):
            try:
                print("before")
                cur=connect_to_db()
                cur.execute(f""" select  u."Name" , s."RollNo" from "Student" as "s", "Indulged" as "i" ,"User" as "u", "Project" as "p" where p."Field" = '{result['Field1']}' and p."ProjectId" = i."ProjectId" and i."StudentId" = s."RollNo" and s."Degree" = 'PHD' and s."UserId" = u."EmailID";
                """)
                d=cur.fetchall()
                print(cur.fetchall())
                print("after")
                cur.close()
            except Exception as e:
                print(e)



    if("Project_under_Proof" in result):
        print("before")
        print(result)
        
        if(result["Proof_Req"] == "Verified"):
            try:
                cur = connect_to_db()
                cur.execute(f""" select "StudentId","Title","Institution" from "Achievement" where "Proof" =  
                'Verified' and "StudentId" = '{result['RollNo3']}';                
                """)
                f = cur.fetchall()
                print(cur.fetchall())

                cur.close()
            except Exception as e:
                print(e)
        if(result["Proof_Req"] == "File Uploaded"):
            try:
                cur = connect_to_db()
                cur.execute(f""" select "StudentId","Title","Institution" from "Achievement" where "Proof" =  
                'File Uploaded' and "StudentId" = '{result['RollNo3']}';                
                """)
                f = cur.fetchall()
                print(cur.fetchall())
                cur.close()
            except Exception as e:
                print(e)
        if(result["Proof_Req"] == "Pending"):
            try:
                cur = connect_to_db()
                cur.execute(f""" select "StudentId","Title","Institution" from "Achievement" where "Proof" =  
                'Pending' and "StudentId" = '{result['RollNo3']}';                
                """)
                f = cur.fetchall()
                print(cur.fetchall())

                cur.close()
            except Exception as e:
                print(e)

    if("Profile" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select * from "Recruiter" where "UserId"='{result['Id']}';
            """)
            g=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)

    if("Show_Details" in result):
        try:
            print("before")
            cur=connect_to_db()
            cur.execute(f""" select a."EducationId",d."Institution",d."Degree" from "Education" as "d" , "Attended_Student" as "a" where a."StudentId" = '{result['RollNo5']}' and a."EducationId" = d."EducationId";
            """)
            z=cur.fetchall()
            print(cur.fetchall())
            print("after")
            cur.close()
        except Exception as e:
            print(e)
    
    



    return render_template('Recruiter.html',x=x,y=y,z=z,u=u,v=v,a=a,b=b,d=d,g=g,f=f)