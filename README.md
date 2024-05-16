## Hospital Management System

This project implements a Hospital Management System with a user-friendly Tkinter GUI for managing patients, doctors, ward boys, appointments, and rooms.

### Functionalities

* **Staff Management:**
  * CRUD operations (Create, Read, Update, Delete) for Doctors, Nurses, and Ward Boys.
  * Stores data including ID, name, contact details, and salary. (Replace CRUD with more specific functionalities if implemented)
* **Patient Management:**
  * CRUD operations for patients.
  * Stores data including ID, name, demographics, and disease information.
* **Room Management:**
  * CRUD operations for rooms.
  * Tracks room availability with unique identifiers and status indicators.
* **Appointment Management:**
  * Functionality to schedule appointments linking patients and doctors. 
* **Staff Relationships:**
  * Defines relationships between doctors and nurses (one-to-many).
  * Assigns nurses and ward boys to govern specific rooms (one-to-many/many-to-one).
* **Patient Room Assignment:**
  * Assigns patients to rooms, ensuring each patient has a designated room and rooms can be marked as occupied or empty.
 

### Database Design and Queries

This section details the database design and sample queries used in the Hospital Management System.

**Indexing:**

Indexes are created on specific columns in tables to improve the performance of queries that frequently filter or join data based on those columns. Here are the indexes implemented:

* **idx_Appointment_Doctor_ID:** Speeds up queries filtering appointments by doctor ID.
* **idx_Appointment_Patient_ID:** Improves performance for queries searching appointments by patient ID.
* **idx_Helping_Doctor_ID & idx_Helping_Nurse_ID:** Optimizes queries filtering the "Helping" table by doctor or nurse ID.
* **idx_Govers_Nurse_ID & idx_Govers_Room_Number:** Enhances query performance when searching the "Govers" table by nurse ID or room number.

**Selection Queries: (All queries in the report)**

This query retrieves information about patients and their assigned staff (nurse and ward boy) based on room assignments. It utilizes LEFT JOINs to include patients even without assigned staff.

```sql
SELECT 
          Patient.Patient_ID, Patient.First_Name AS Patient_First_Name,                                              
          Patient.Last_Name AS Patient_Last_Name,
          Nurse.Nurse_ID, Nurse.Salary AS Nurse_Salary, Ward_boy.Ward_boy_ID,                
          Ward_boy.Description AS Ward_boy_Description,
          Ward_boy.Salary AS Ward_boy_Salary FROM Patient
   LEFT JOIN Room ON Patient.Room_Number = Room.Room_Number 
   LEFT JOIN Govers ON Govers.Room_Number = Room.Room_Number
   LEFT JOIN Nurse ON Govers.Nurse_ID = Nurse.Nurse_ID 
   LEFT JOIN Ward_boy ON Ward_boy.Ward_boy_ID = Room.Ward_boy_ID;
```

This system provides a comprehensive solution for hospital administration by managing staff, patients, appointments, rooms, and staff assignments.

### Dependencies

* Tkinter (GUI library)
### How to Run

1. Install required dependencies (refer to documentation for each library).
2. Clone or download the project repository.
3. Open the main Python file (e.g., main.py) in a code editor.
4. Run the script.

