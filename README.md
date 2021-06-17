# TickSy Server

## Get Start :

#### **1. git clone https://gitlab.com/amiralifmj/ticksy.git** (terminal)

#### **2. pip install -r requirements.txt** (terminal, with active virtualenv)

#### **3. create database with this info:**  (mysql)

    'NAME': 'ticksy_db'
    
    'USER': 'ticksy'
    
    'PASSWORD': 'Ticksy_1234'
    
    - Set the **Charset to utf8mb4**, and **Collaction to utf8mb4_general** when creating database in mysql.

##### **3.1. for convenience :**

    CREATE USER 'ticksy'@'%' IDENTIFIED BY 'Ticksy_1234';
    
    GRANT ALL PRIVILEGES ON *.* TO 'ticksy'@'%';
    
    CREATE DATABASE ticksy_db DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_general_ci;


#### **4. python manage.py makemigrations** (terminal)

#### **5. python manage.py migrate** (terminal)

#### **6. python manage.py runserver** (terminal)

- **Admin panel**:
    - http://localhost:8000/admin/ 
- **API Documentation**: (pick one)
    - http://localhost:8000/swagger/
    - http://localhost:8000/redoc/

## Done!