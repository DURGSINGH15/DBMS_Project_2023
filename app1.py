from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import redirect, url_for

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1001@localhost/StudentTrainingPlacement_DB"   
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)     #Initialize the SQLAlchemy extension 

@app.route('/')
def about():
    return render_template("about.html")


#association table is above the two tables so that it can be found in the relationship defined in Student.
training_student = db.Table('training_student',
    db.Column('student_id', db.String(200), db.ForeignKey('student.student_id')),
    db.Column('training_id', db.Integer, db.ForeignKey('training.training_id'))
)

class Student(db.Model):
    student_id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    academics = db.Column(db.String(200), nullable=False)
    training_details = db.Column(db.Text, nullable=True)
    job_situation = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    get_training = db.relationship('Training', secondary='training_student', backref='took_by')

    def __repr__(self) -> str:
        return f"Student(student_id='{self.student_id}', name='{self.name}', email='{self.email}', academics='{self.academics}', training_details='{self.training_details}', job_situation='{self.job_situation}', date_created='{self.date_created}')"

class Training(db.Model):
    training_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"Training(training_id={self.training_id}, name='{self.name}', duration='{self.duration}', cost={self.cost}, type='{self.type}', description='{self.description}')"
    
#association table is above the two tables so that it can be found in the relationship defined in company.
company_job = db.Table('company_job',
            db.Column('company_id',db.Integer, db.ForeignKey('company.company_id')),
            db.Column('job_id',db.Integer, db.ForeignKey('job.job_id'))                       
)

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    has_jobs = db.relationship('Job',secondary=company_job, backref='can_from') #backref is a fake column created in the second table which is the first argument in relationship.

    def __repr__(self) -> str:
        return f"Company name='{self.name}' "

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Job name='{self.name}' "

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"Admin(name='{self.name}', email='{self.email}')"


# Import the Flask app and SQLAlchemy object
#from app1 import app, db #app- flask appln. instance, db-SQLAlchemy object
# Create the database tables
with app.app_context():
    db.create_all()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#to request entries from FORMS to put into mysql table
from flask import request

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/table0', methods=['GET', 'POST'])  #associative entity

def training_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        training_id = request.form['training_id']

        student = Student.query.get(student_id)
        training = Training.query.get(training_id)

        if student and training:
            if not hasattr(student, 'get_training'):
                student.get_training = []
            student.get_training.append(training)
            db.session.commit()
            return redirect("/table0")
        else:
            error_message = "Student or training not found!"
            return render_template("index0.html", error_message=error_message)

    allStudents = Student.query.all()
    allTrainings = Training.query.all()

    return render_template("index0.html", allStudents=allStudents, allTrainings=allTrainings)
#------------------------------------------------------------------------------------------------------------------
#Student- /table1
#For POST requests, it retrieves data submitted through a form on your HTML page, creates a new Student object with that data,
# adds it to the database session, and commits the changes to the database.
#For GET requests, it retrieves all the students from the database and passes them to the HTML template index1.html to be displayed.
@app.route('/table1', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        email = request.form['email']
        academics = request.form['academics']
        training_details = request.form['training_details']
        job_situation = request.form['job_situation']


        # Create a new Student object with the submitted details            
        student = Student(student_id=student_id, name=name, email=email, academics=academics, training_details=training_details, job_situation=job_situation)

        # Add the new student to the database session   
        db.session.add(student)
        # Commit the changes to the database
        db.session.commit()

    # Retrieve all students from the database
    allStudents = Student.query.all()

    return render_template("index1.html", allStudents=allStudents)# LHS allStudents(variable referenced from HTML template index1.html) and
                                                                  #RHS allStudents(python variable ) is the actual data we pass to index1.html
@app.route('/update1/<string:student_id>', methods=['GET','POST']) 
def update_student(student_id):
    if request.method=="POST":
        name = request.form['name']
        email = request.form['email']
        academics = request.form['academics']
        training_details = request.form['training_details']
        job_situation = request.form['job_situation']

        student = Student.query.filter_by(student_id=student_id).first()
        student.name = name
        student.email = email
        student.academics = academics
        student.training_details = training_details
        student.job_situation = job_situation

        db.session.commit()
        return redirect('/table1')

    student = Student.query.filter_by(student_id=student_id).first()
    return render_template("update1.html", student=student)
                                                              
@app.route('/delete1/<string:student_id>')
def delete(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    db.session.delete(student)
    db.session.commit()

    return redirect("/table1")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/table2', methods=['GET', 'POST'])
def add_training():
    if request.method == 'POST':
        training_id = request.form['training_id']
        name = request.form['name']
        duration = request.form['duration']
        cost = request.form['cost']
        type = request.form['type']
        description = request.form['description']

        # Create a new Training object with the submitted details            
        training = Training(training_id=training_id, name=name, duration=duration, cost=cost, type=type, description=description)

        # Add the new training to the database session   
        db.session.add(training)
        # Commit the changes to the database
        db.session.commit()

    # Retrieve all trainings from the database
    allTrainings = Training.query.all()

    return render_template("index2.html", allTrainings=allTrainings)

@app.route('/update2/<int:training_id>', methods=['GET', 'POST'])
def update_training(training_id):
    if request.method == "POST":
        name = request.form['name']
        duration = request.form['duration']
        cost = request.form['cost']
        training_type = request.form['type']
        description = request.form['description']

        training = Training.query.filter_by(training_id=training_id).first()
        training.name = name
        training.duration = duration
        training.cost = cost
        training.type = training_type
        training.description = description

        db.session.commit()
        return redirect('/table2')

    training = Training.query.filter_by(training_id=training_id).first()
    return render_template("update2.html", training=training)

@app.route('/delete2/<int:training_id>')
def delete2(training_id):
    training = Training.query.filter_by(training_id=training_id).first()
    db.session.delete(training)
    db.session.commit()

    return redirect("/table2")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/table3', methods=['GET', 'POST'])
def company_job():
    if request.method == 'POST':
        company_id = request.form['company_id']
        job_id = request.form['job_id']

        company = Company.query.get(company_id)
        job = Job.query.get(job_id)

        if company and job:
            if not hasattr(company, 'has_jobs'):
                company.has_jobs = []
            company.has_jobs.append(job)
            db.session.commit()
            return redirect("/table3")
        else:
            error_message = "Company or job not found!"
            return render_template("index3.html", error_message=error_message)

    allCompanies = Company.query.all()
    allJobs = Job.query.all()

    return render_template("index3.html", allCompanies=allCompanies, allJobs=allJobs)

#No need of delete and update operations in company_job as if some primary key gets deleted the record here gets deleted accordingly!
#----------------------------------------------------------------------
@app.route('/table4', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_id = request.form['company_id']
        name = request.form['name']
        industry = request.form['industry']
        location = request.form['location']

        company = Company(company_id=company_id, name=name, industry=industry, location=location)
        db.session.add(company)
        db.session.commit()

    allCompanies = Company.query.all()

    return render_template("index4.html", allCompanies=allCompanies)

@app.route('/update4/<int:company_id>', methods=['GET', 'POST'])
def update_company(company_id):
    if request.method == "POST":
        name = request.form['name']
        industry = request.form['industry']
        location = request.form['location']

        company = Company.query.filter_by(company_id=company_id).first()
        company.name = name
        company.industry = industry
        company.location = location

        db.session.commit()
        return redirect('/table4')

    company = Company.query.filter_by(company_id=company_id).first()
    return render_template("update4.html", company=company)

@app.route('/delete4/<int:company_id>')
def delete4(company_id):
    company = Company.query.get(company_id)
    db.session.delete(company)
    db.session.commit()

    return redirect("/table4")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/table5', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        job_id = request.form['job_id']
        name = request.form['name']
        title = request.form['title']
        salary = request.form['salary']
        requirements = request.form['requirements']
        description = request.form['description']
        

        job = Job(job_id=job_id, name=name, title=title, salary=salary, requirements=requirements, description=description)
        db.session.add(job)
        db.session.commit()

    allJobs = Job.query.all()

    return render_template("index5.html", allJobs=allJobs)

@app.route('/update5/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    if request.method == "POST":
        name = request.form['name']
        title = request.form['title']
        salary = request.form['salary']
        requirements = request.form['requirements']
        description = request.form['description']

        job = Job.query.filter_by(job_id=job_id).first()
        job.name = name
        job.title = title
        job.salary = salary
        job.requirements = requirements
        job.description = description

        db.session.commit()
        return redirect('/table5')

    job = Job.query.filter_by(job_id=job_id).first()
    return render_template("update5.html", job=job)

@app.route('/delete5/<int:job_id>')
def delete5(job_id):
    job = Job.query.get(job_id)
    db.session.delete(job)
    db.session.commit()

    return redirect("/table5")

#---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/table6', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        admin = Admin(admin_id=admin_id, name=name, email=email, password=password)
        db.session.add(admin)
        db.session.commit()

    allAdmins = Admin.query.all()

    return render_template("index6.html", allAdmins=allAdmins)

@app.route('/delete6/<int:admin_id>')
def delete6(admin_id):
    admin = Admin.query.get(admin_id)
    db.session.delete(admin)
    db.session.commit()

    return redirect("/table6")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    app.run(debug=True, port=5000)

