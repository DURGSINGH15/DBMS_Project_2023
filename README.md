# 🎓 Student Placement Management System  

A web-based application built using **Flask (Python)** and **MySQL (via SQLAlchemy ORM)** for managing students, trainings, companies, job opportunities, and administrators.  

This project was developed as part of my **Database Management Systems coursework**, showcasing practical application of **SQL concepts, relational schema design, and CRUD operations** in a real-world scenario.

---

## ✨ Features  

- 👨‍🎓 **Student Management** – Add, update, delete, and view students with details like academics, training participation, and job situation.  
- 🏫 **Training Management** – Manage training sessions with name, duration, cost, type, and description.  
- 🏢 **Company Management** – Store details of recruiting companies, industry type, and locations.  
- 💼 **Job Management** – Maintain job postings with title, salary, requirements, and descriptions.  

- 🔗 **Relationship Handling**:
  - Many-to-Many between **Students ↔ Trainings**  
  - Many-to-Many between **Companies ↔ Jobs**  

---

## 🛠️ Tech Stack  

- **Backend**: Flask (Python)  
- **Database**: MySQL (handled via SQLAlchemy ORM)  
- **Frontend**: HTML + Jinja2 templates  
- **Tools**: VS Code, Git, Command-Line MySQL Client  

---

## 🗄️ Database Design  

### Entities (Tables)
- `Student`  
- `Training`  
- `Company`  
- `Job`  
- `Admin`  

### Association Tables
- `training_student` → connects Students and Trainings  
- `company_job` → connects Companies and Jobs  

### Relationships
- **Student ↔ Training** (Many-to-Many)  
- **Company ↔ Job** (Many-to-Many)  

---

## ⚙️ Setup Instructions  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DURGSINGH15/DBMS_Project_2023.git
cd DBMS_Project_2023
```

### 2️⃣Create and Activate a Virtual Environment

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```
For **Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3️⃣ Configure Database
Open MySQL and create a database:
```sql
CREATE DATABASE StudentTrainingPlacement_DB;
```
Update the connection string in app.py with your MySQL username & password:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<user>:<password>@localhost/StudentTrainingPlacement_DB"
```

### 4️⃣ Run the Application
```bash
python app.py
```
Now open your browser at:
http://127.0.0.1:5000/
