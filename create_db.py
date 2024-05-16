import sqlite3


# Define your SQLite script as a multi-line string
sqlite_script = """
-- Employee table
CREATE TABLE IF NOT EXISTS Employee (
    Employee_ID INTEGER PRIMARY KEY,
    First_Name TEXT,
    Last_Name TEXT,
    Phone TEXT,
    Zip_Number TEXT,
    City TEXT,
    Street TEXT,
    Gender TEXT,
    Type TEXT
);

-- Doctor table
CREATE TABLE IF NOT EXISTS Doctor (
    Doctor_ID INTEGER PRIMARY KEY,
    Department TEXT,
    Fees INTEGER,
    FOREIGN KEY (Doctor_ID) REFERENCES Employee (Employee_ID)
);

-- Nurse table
CREATE TABLE IF NOT EXISTS Nurse (
    Nurse_ID INTEGER PRIMARY KEY,
    Salary REAL,
    FOREIGN KEY (Nurse_ID) REFERENCES Employee (Employee_ID)
);

-- Ward boy table
CREATE TABLE IF NOT EXISTS Ward_boy (
    Ward_boy_ID INTEGER PRIMARY KEY,
    Description TEXT,
    Salary REAL,
    FOREIGN KEY (Ward_boy_ID) REFERENCES Employee (Employee_ID)
);

-- Room table
CREATE TABLE IF NOT EXISTS Room (
    Room_Number INTEGER PRIMARY KEY,
    Ward_boy_ID INTEGER,
    Room_Type TEXT,
    Status TEXT,
    FOREIGN KEY (Ward_boy_ID) REFERENCES Ward_boy (Ward_boy_ID)
);

-- Patient table
CREATE TABLE IF NOT EXISTS Patient (
    Patient_ID INTEGER PRIMARY KEY,
    First_Name TEXT,
    Last_Name TEXT,
    Phone TEXT,
    Zip_Number TEXT,
    City TEXT,
    Street TEXT,
    Gender TEXT,
    Age INTEGER,
    Disease TEXT,
    Birthdate TEXT
);

-- Appointment table
CREATE TABLE IF NOT EXISTS Appointment (
    Appointment_ID INTEGER PRIMARY KEY,
    Doctor_ID INTEGER,
    Patient_ID INTEGER,
    Cost REAL,
    Date TEXT,
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor (Doctor_ID),
    FOREIGN KEY (Patient_ID) REFERENCES Patient (Patient_ID)
);

-- Helping table (Association table for Doctor and Nurse)
CREATE TABLE IF NOT EXISTS Helping (
    Doctor_ID INTEGER,
    Nurse_ID INTEGER,
    PRIMARY KEY (Doctor_ID, Nurse_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Doctor (Doctor_ID),
    FOREIGN KEY (Nurse_ID) REFERENCES Nurse (Nurse_ID)
);

-- Govers table (Association table for Nurse and Room)
CREATE TABLE IF NOT EXISTS Govers (
    Nurse_ID INTEGER,
    Room_Number INTEGER,
    PRIMARY KEY (Nurse_ID, Room_Number),
    FOREIGN KEY (Nurse_ID) REFERENCES Nurse (Nurse_ID),
    FOREIGN KEY (Room_Number) REFERENCES Room (Room_Number)
);

"""

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('hospital_management_system_db3.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute the script
cursor.executescript(sqlite_script)

# Commit the changes
conn.commit()

# Close the cursor and connection to the database
cursor.close()
conn.close()
