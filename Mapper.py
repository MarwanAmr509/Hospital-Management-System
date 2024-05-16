import sqlite3

database_path = 'hospital_management_system_db3.db'

def add_employee_to_db(employee_data,special_data):
    # Establish a connection to the database
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    # Create the INSERT INTO statement for the employee
    insert_employee = """
    INSERT INTO Employee (Employee_ID, First_Name, Last_Name, Phone, Gender, City, Street, Zip_Number, Type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    insert_special = """"""
    
    # Execute the insert statement
    cursor.execute(insert_employee, employee_data)

    if employee_data[-1] == 'Doctor':
        insert_special = """
    INSERT INTO Doctor (Doctor_ID, Department,Fees)
    VALUES (?, ?,?);
    """
         # Execute the insert statement 
        cursor.execute(insert_special, special_data)

    elif employee_data[-1] == 'Nurse':
        insert_special = """
    INSERT INTO Nurse (Nurse_ID, Salary)
    VALUES (?, ?);
    """
         # Execute the insert statement 
        cursor.execute(insert_special, special_data)

    elif employee_data[-1] == 'Ward Boy':

        insert_special = """
    INSERT INTO Ward_boy (Ward_boy_ID, Description,Salary)
    VALUES (?, ?,?);
    """
         # Execute the insert statement 
        cursor.execute(insert_special, special_data)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


# Function to get employee data from the database
def get_employees(employee_type=None):
    conn = sqlite3.connect(database_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    if employee_type == 'Doctor':
        # Adjust the JOIN query as per your database schema
        query = """
        SELECT Employee.Employee_ID, Employee.First_Name, Employee.Last_Name, Employee.Phone, 
               Employee.Gender, Employee.City, Employee.Street, Employee.Zip_Number, 
               Employee.Type, Doctor.Department, Doctor.Fees
        FROM Employee
        JOIN Doctor ON Employee.Employee_ID = Doctor.Doctor_ID
        """
        cursor.execute(query)
    elif employee_type == 'Nurse':
        query = """
            SELECT Employee.Employee_ID, Employee.First_Name, Employee.Last_Name, Employee.Phone, 
                Employee.Gender, Employee.City, Employee.Street, Employee.Zip_Number, 
                Employee.Type, Nurse.Salary
            FROM Employee
            JOIN Nurse ON Employee.Employee_ID = Nurse.Nurse_ID
            """
        cursor.execute(query)
    elif employee_type == 'Ward Boy':
        query = """
            SELECT Employee.Employee_ID, Employee.First_Name, Employee.Last_Name, Employee.Phone, 
                Employee.Gender, Employee.City, Employee.Street, Employee.Zip_Number, 
                Employee.Type, Ward_boy.Description, Ward_boy.Salary
            FROM Employee
            JOIN Ward_boy ON Employee.Employee_ID = Ward_boy.Ward_boy_ID
            """
        cursor.execute(query)
    else:
        query = "SELECT * FROM Employee"
        cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_patient_into_db(patient_id, first_name, last_name, phone, zip_number, city, street, gender, age, disease, birthdate,room_number):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;")

    # SQL INSERT statement
    insert_stmt = """
    INSERT INTO Patient (Patient_ID, First_Name, Last_Name, Phone, Zip_Number, City, Street, Gender, Age, Disease, Birthdate, Room_Number)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        # Execute the insert statement
        cursor.execute(insert_stmt, (patient_id, first_name, last_name, phone, zip_number, city, street, gender, age, disease, birthdate,room_number))
        conn.commit()
        return True, "Patient added successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        # Close the database connection
        cursor.close()
        conn.close()


def get_patients():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;")


    query = "SELECT * FROM Patient"  # Adjust the query as per your database schema
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_room_into_db(room_number, ward_boy_id, room_type, status):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # SQL INSERT statement
    insert_stmt = """
    INSERT INTO Room (Room_Number, Ward_Boy_ID, Room_Type, Status)
    VALUES (?, ?, ?, ?)
    """
    try:
        cursor.execute(insert_stmt, (room_number, ward_boy_id, room_type, status))
        conn.commit()
        return True, "Room added successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        if conn:
            conn.close()


def get_rooms():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT Room_Number, Ward_Boy_ID, Room_Type, Status FROM Room"  # Adjust the query to match your database schema
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_appointment_into_db(appointment_id, doctor_id, patient_id, cost, date):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    insert_stmt = """
        INSERT INTO Appointment (Appointment_ID, Doctor_ID, Patient_ID, Cost, Date)
        VALUES (?, ?, ?, ?, ?)
        """


    try:
        cursor.execute(insert_stmt, (appointment_id, doctor_id, patient_id, cost, date))
        conn.commit()
        return True, "Appointment added successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        # Close the database connection
        if conn:
            conn.close()

def does_doctor_exist(doctor_id):
    """
    Checks if a doctor with the given ID exists in the database.

    :param doctor_id: The ID of the doctor to check.
    :return: True if the doctor exists, False otherwise.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        query = "SELECT EXISTS(SELECT 1 FROM Doctor WHERE Doctor_ID = ? LIMIT 1)"
        cursor.execute(query, (doctor_id,))
        exists = cursor.fetchone()[0]
        return exists == 1
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def does_patient_exist(patient_id):
    """
    Checks if a patient with the given ID exists in the database.

    :param patient_id: The ID of the patient to check.
    :return: True if the patient exists, False otherwise.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        query = "SELECT EXISTS(SELECT 1 FROM Patient WHERE Patient_ID = ? LIMIT 1)"
        cursor.execute(query, (patient_id,))
        exists = cursor.fetchone()[0]
        return exists == 1
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def does_nurse_exist(nurse_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        query = "SELECT EXISTS(SELECT 1 FROM Nurse WHERE Nurse_ID = ? LIMIT 1)"
        cursor.execute(query, (nurse_id,))
        exists = cursor.fetchone()[0]
        return exists == 1
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def does_room_exist(room_number):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        query = "SELECT EXISTS(SELECT 1 FROM Room WHERE Room_Number = ? LIMIT 1)"
        cursor.execute(query, (room_number,))
        exists = cursor.fetchone()[0]
        return exists == 1
    finally:
        cursor.close()
        conn.close()

def does_ward_boy_exist(ward_boy_id):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        query = "SELECT EXISTS(SELECT 1 FROM Ward_boy WHERE Ward_boy_ID = ? LIMIT 1)"
        cursor.execute(query, (ward_boy_id,))
        exists = cursor.fetchone()[0]
        return exists == 1
    finally:
        cursor.close()
        conn.close()

def get_appointments():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT Appointment_ID, Doctor_ID, Patient_ID, Cost, Date FROM Appointment"
    cursor.execute(query)

    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    return appointments

def insert_helping_into_db(doctor_id, nurse_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # SQL INSERT statement
        insert_stmt = """
        INSERT INTO Helping (Doctor_ID, Nurse_ID)
        VALUES (?, ?)
        """
        cursor.execute(insert_stmt, (doctor_id, nurse_id))
        conn.commit()

        return True, "Association added successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        # Close the database connection
        if conn:
            conn.close()

def get_helpings():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT Doctor_ID, Nurse_ID FROM Helping"  # Adjust the query as per your database schema
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def insert_gover_into_db(nurse_id, room_number):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        insert_stmt = """
        INSERT INTO Govers (Nurse_ID, Room_Number)
        VALUES (?, ?)
        """
        cursor.execute(insert_stmt, (nurse_id, room_number))
        conn.commit()

        return True, "Record added to Governs successfully"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    finally:
        if conn:
            conn.close()


def get_govers():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT Nurse_ID, Room_Number FROM Govers"  # Adjust the query as per your database schema
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


