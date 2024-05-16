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


This system provides a comprehensive solution for hospital administration by managing staff, patients, appointments, rooms, and staff assignments.

### Dependencies

* Tkinter (GUI library)
### How to Run

1. Install required dependencies (refer to documentation for each library).
2. Clone or download the project repository.
3. Open the main Python file (e.g., main.py) in a code editor.
4. Run the script.

