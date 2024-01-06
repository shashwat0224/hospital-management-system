import mysql.connector as mc
mysql = mc.connect(
    host = "localhost",
    user = "root",
    passwd = "20357",
    database = "hospital"
    )
if mysql.is_connected():
    print("Connection successfully established !")

cursor = mysql.cursor()

# cursor.execute('''CREATE TABLE patient (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     age INT,
#     sex VARCHAR(10),
#     blood_group VARCHAR(10),
#     email VARCHAR(100),
#     contact VARCHAR(20),
#     address VARCHAR(255),
#     illness_injury VARCHAR(255),
#     status ENUM('outpatient', 'inpatient')
# );
# ''')

# cursor.execute('''CREATE TABLE doctor (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     specialization VARCHAR(100),
#     fees DECIMAL(10, 2),
#     contact VARCHAR(20),
#     address VARCHAR(255),
#     email VARCHAR(100)
# );
# ''')
# cursor.execute('''CREATE TABLE staff (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     job_title VARCHAR(100),
#     contact VARCHAR(20),
#     address VARCHAR(255),
#     email VARCHAR(100)
# );
# ''')
# cursor.execute('''CREATE TABLE admitted (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     patient_id INT,
#     doctor_id INT,
#     admit_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#     discharged_date DATETIME,
#     FOREIGN KEY (patient_id) REFERENCES patient(id),
#     FOREIGN KEY (doctor_id) REFERENCES doctor(id)
# );
# ''')
# cursor.execute('''CREATE TABLE appointments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     patient_id INT,
#     doctor_id INT,
#     appointment_date DATE,
#     appointment_time TIME,
#     FOREIGN KEY (patient_id) REFERENCES patient(id),
#     FOREIGN KEY (doctor_id) REFERENCES doctor(id)
#     -- Add any additional columns as needed
# );
# ''')

# cursor.execute("ALTER TABLE staff AUTO_INCREMENT = 346000;")
# cursor.execute("ALTER TABLE doctor AUTO_INCREMENT = 157000;")
# cursor.execute("ALTER TABLE patient AUTO_INCREMENT = 736090;")

# cursor.execute('''INSERT INTO staff (name, job_title, contact, address, email)
# VALUES
#     ('John Doe', 'Nurse', '1234567890', '123 Staff St, City', 'john@example.com'),
#     ('Jane Smith', 'Receptionist', '9876543210', '456 Office Ave, Town', 'jane@example.com'),
#     ('Michael Johnson', 'Janitor', '5551237890', '789 Maintenance Rd, Village', 'michael@example.com'),
#     ('Sarah Adams', 'Pharmacist', '7779998888', '321 Pharmacy Lane, County', 'sarah@example.com'),
#     ('David Wilson', 'Technician', '4443332222', '654 Tech Blvd, Hamlet', 'david@example.com');
# ''')

# cursor.execute('''INSERT INTO doctor (name, specialization, fees, contact, address, email)
# VALUES
#     ('Dr. Alex Brown', 'Cardiologist', 250.00, '1112223333', '789 Heart St, City', 'alex@example.com'),
#     ('Dr. Emily Davis', 'Dermatologist', 200.00, '4445556666', '456 Skin Ave, Town', 'emily@example.com'),
#     ('Dr. Robert Lee', 'Orthopedic Surgeon', 300.00, '7778889999', '123 Bone Rd, Village', 'robert@example.com'),
#     ('Dr. Sophia Garcia', 'Pediatrician', 180.00, '3334445555', '321 Kids Lane, County', 'sophia@example.com'),
#     ('Dr. William Clark', 'Neurologist', 280.00, '6667778888', '654 Brain Blvd, Hamlet', 'william@example.com');
# ''')

# cursor.execute('''INSERT INTO patient (name, age, sex, blood_group, email, contact, address, illness_injury, status)
# VALUES
#     ('Alice Johnson', 25, 'Female', 'O+', 'alice@example.com', '1112223333', '123 Health St, City', 'Fever', 'inpatient'),
#     ('Bob Williams', 40, 'Male', 'A-', 'bob@example.com', '4445556666', '456 Wellness Ave, Town', 'Fractured Arm', 'outpatient'),
#     ('Eva Miller', 30, 'Female', 'B+', 'eva@example.com', '7778889999', '789 Care Rd, Village', 'Allergies', 'inpatient'),
#     ('Jack Davis', 35, 'Male', 'AB+', 'jack@example.com', '3334445555', '321 Cure Lane, County', 'Migraine', 'outpatient'),
#     ('Sophie Wilson', 50, 'Female', 'A+', 'sophie@example.com', '6667778888', '654 Recovery Blvd, Hamlet', 'Sprained Ankle', 'inpatient');
# ''')

# cursor.execute('''INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time)
# VALUES
#     (736090, 157000, '2024-01-15', '10:00:00'),
#     (736091, 157001, '2024-01-18', '14:30:00'),
#     (736092, 157002, '2024-01-20', '11:45:00');
# ''')

# cursor.execute('''INSERT INTO admitted (patient_id, doctor_id, admit_date, discharged_date)
# VALUES
#     (736090, 157003, '2024-01-10 08:00:00', NULL),
#     (736091, 157001, '2024-01-05 10:30:00', '2024-01-10 16:00:00');
# ''')

# mysql.commit()

# print("commited")
# patient_id = "736090"
# query = f"SELECT discharged_date FROM admitted WHERE patient_id = {patient_id};"
# cursor.execute(query)
# patient = cursor.fetchone()
# if patient[0] is not None:
#     print(patient)  
