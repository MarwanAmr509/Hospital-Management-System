import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import Mapper
import re

database_path = 'hospital_management_system_db3.db'



def login_window():
    # Function to check credentials
    def check_credentials():
        username = entry_username.get()
        password = entry_password.get()
        
        # Normally you would hash and check these against a secure database
        if username == 'admin' and password == 'admin123':
            login_window.destroy()  # Close the login window
            main_window.deiconify()  # Show the main window
        else:
            messagebox.showwarning("Login Failed", "Incorrect username or password")
    # Login window
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry('300x300')

    # Username field
    tk.Label(login_window, text="Username:").pack()
    entry_username = tk.Entry(login_window)
    entry_username.pack()

    # Password field
    tk.Label(login_window, text="Password:").pack()
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack()

    # Login button
    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    login_button.pack()

# Global update function
def update_treeview(tree, fetch_data_function):
    tree.delete(*tree.get_children())  # Clear existing data
    for item in fetch_data_function():
        tree.insert('', 'end', values=item)

def Add_Employee_Window():
    # Function to add an employee to the database
    def add_employee():
        # Here you'd retrieve the form data
        employee_id = entry_id.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        phone = entry_phone.get()
        gender = gender_var.get()
        city = entry_city.get()
        street = entry_street.get()
        zip_number = entry_zip_number.get()
        employee_type = type_var.get()
        department = entry_department.get() if employee_type == 'Doctor' else None
        fees = entry_fees.get() if employee_type == 'Doctor' else None
        salary = entry_salary.get() if (employee_type == 'Nurse') or (employee_type == 'Ward Boy') else None
        description = text_description.get("1.0", tk.END).strip() if employee_type == 'Ward Boy' else None

        # Collect the employee data in a tuple
        employee_data = (employee_id, first_name, last_name, phone, gender, city, street, zip_number, employee_type)
        special_data = ''

        if employee_type == 'Doctor':
            special_data = (employee_id,department,fees)
        elif employee_type == 'Nurse':
            special_data = (employee_id,salary)
        elif employee_type == 'Ward Boy':
            special_data = (employee_id,description,salary)
        

        # You would normally validate and process these values here
        # For now, let's just print them to the console
        print(f"ID: {employee_id}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Phone: {phone}")
        print(f"Gender: {gender}")
        print(f"City: {city}")
        print(f"Street: {street}")
        print(f"Zip Number: {zip_number}")
        print(f"Employee Type: {employee_type}")
        print(f"Department: {department}")
        print(f"Fees: {fees}")
        print(f"Salary: {salary}")
        print(f"Description: {description}")


        # Insert the data into the database by calling Mapper Module
        try:
            Mapper.add_employee_to_db(employee_data,special_data)
            update_treeview(employee_tree, Mapper.get_employees)  # Update the employee tree view
            messagebox.showinfo("Success", "Employee added successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to show/hide the Department field based on Employee Type
    def on_type_changed(event):
        employee_type = type_var.get()
        # Hide all fields first
        department_label.grid_remove()
        entry_department.grid_remove()
        salary_label.grid_remove()
        entry_salary.grid_remove()
        fees_label.grid_remove()
        entry_fees.grid_remove()
        description_label.grid_remove()
        text_description.grid_remove()

        # Then show the field relevant to the selected employee type
        if employee_type == 'Doctor':
            department_label.grid(row=10, column=0, sticky=tk.W, pady=2)
            entry_department.grid(row=10, column=1, sticky=tk.EW, pady=2)

            fees_label.grid(row=11, column=0, sticky=tk.W, pady=2)
            entry_fees.grid(row=11, column=1, sticky=tk.EW, pady=2)
        elif employee_type == 'Nurse':
            salary_label.grid(row=10, column=0, sticky=tk.W, pady=2)
            entry_salary.grid(row=10, column=1, sticky=tk.EW, pady=2)
        elif employee_type == 'Ward Boy':
            description_label.grid(row=10, column=0, sticky=tk.W, pady=2)
            text_description.grid(row=10, column=1, sticky=tk.EW, pady=2)

            salary_label.grid(row=11, column=0, sticky=tk.W, pady=2)
            entry_salary.grid(row=11, column=1, sticky=tk.EW, pady=2)
    # Frame for the Employee form
    employee_form_frame = ttk.Frame(tab_employee)
    employee_form_frame.pack(padx=11, pady=10, fill='x', expand=True)

 # 'Add Employee' label at the top
    add_employee_label = ttk.Label(employee_form_frame, text="Add Employee", font=('TkDefaultFont', 16))
    add_employee_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
    # ID field
    ttk.Label(employee_form_frame, text="ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_id = ttk.Entry(employee_form_frame)
    entry_id.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # First Name field
    ttk.Label(employee_form_frame, text="First Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_first_name = ttk.Entry(employee_form_frame)
    entry_first_name.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Last Name field
    ttk.Label(employee_form_frame, text="Last Name:").grid(row=3, column=0, sticky=tk.W, pady=2)
    entry_last_name = ttk.Entry(employee_form_frame)
    entry_last_name.grid(row=3, column=1, sticky=tk.EW, pady=2)

    # Phone field
    ttk.Label(employee_form_frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, pady=2)
    entry_phone = ttk.Entry(employee_form_frame)
    entry_phone.grid(row=4, column=1, sticky=tk.EW, pady=2)

    # Gender field
    ttk.Label(employee_form_frame, text="Gender:").grid(row=5, column=0, sticky=tk.W, pady=2)
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(employee_form_frame, textvariable=gender_var, state='readonly')
    gender_combobox['values'] = ('Male', 'Female')
    gender_combobox.grid(row=5, column=1, sticky=tk.EW, pady=2)

    # City field
    ttk.Label(employee_form_frame, text="City:").grid(row=6, column=0, sticky=tk.W, pady=2)
    entry_city = ttk.Entry(employee_form_frame)
    entry_city.grid(row=6, column=1, sticky=tk.EW, pady=2)

    # Street field
    ttk.Label(employee_form_frame, text="Street:").grid(row=7, column=0, sticky=tk.W, pady=2)
    entry_street = ttk.Entry(employee_form_frame)
    entry_street.grid(row=7, column=1, sticky=tk.EW, pady=2)

    # Zip Number field
    ttk.Label(employee_form_frame, text="Zip Number:").grid(row=8, column=0, sticky=tk.W, pady=2)
    entry_zip_number = ttk.Entry(employee_form_frame)
    entry_zip_number.grid(row=8, column=1, sticky=tk.EW, pady=2)

    # Employee Type field
    ttk.Label(employee_form_frame, text="Employee Type:").grid(row=9, column=0, sticky=tk.W, pady=2)
    type_var = tk.StringVar()
    type_combobox = ttk.Combobox(employee_form_frame, textvariable=type_var, state='readonly')
    type_combobox['values'] = ('Doctor', 'Nurse', 'Ward Boy')
    type_combobox.grid(row=9, column=1, sticky=tk.EW, pady=2)
    type_combobox.bind('<<ComboboxSelected>>', on_type_changed)

    # Department field (initially hidden)
    department_label = ttk.Label(employee_form_frame, text="Department:")
    entry_department = ttk.Entry(employee_form_frame)

    # Fees field (initially hidden)
    fees_label = ttk.Label(employee_form_frame, text="Fees:")
    entry_fees = ttk.Entry(employee_form_frame)

    # Salary field (initially hidden)
    salary_label = ttk.Label(employee_form_frame, text="Salary:")
    entry_salary = ttk.Entry(employee_form_frame)

    # Description field (initially hidden)
    description_label = ttk.Label(employee_form_frame, text="Description:")
    text_description = tk.Text(employee_form_frame, height=3, width=30)

    # Add Employee button
    add_button = ttk.Button(employee_form_frame, text="Add Employee", command=add_employee)
    add_button.grid(row=13, column=0, columnspan=2, pady=10)

    # Configure the grid
    employee_form_frame.columnconfigure(1, weight=1)



def View_Employee_Window():
    # global employee_tree
    def update_treeview():

        employee_type_filter = filter_var.get()

        # Define the default columns
        columns = ['Employee_ID', 'First_Name', 'Last_Name', 'Phone', 'Gender', 'City', 'Street', 'Zip_Number', 'Type']

        # Update columns based on the selected employee type
        if employee_type_filter == 'Doctor':
            columns += ['Department', 'Fees']
        elif employee_type_filter == 'Nurse':
            columns += ['Salary']
        elif employee_type_filter == 'Ward Boy':
            columns += ['Description', 'Salary']


        # Configure treeview columns
        employee_tree['columns'] = columns
        for col in employee_tree['columns']:
            employee_tree.heading(col, text=col.replace('_', ' '))
            employee_tree.column(col, width=70, anchor=tk.CENTER)

        # Clear the existing entries in the treeview
        for item in employee_tree.get_children():
            employee_tree.delete(item)

        # Fetch and insert data
        employees = Mapper.get_employees(employee_type_filter if employee_type_filter != 'All' else None)
        for employee in employees:
            # Adjust the data insertion based on the employee type
            if employee_type_filter == 'Doctor':
                employee_tree.insert('', 'end', values=employee)
            elif employee_type_filter == 'Nurse':
                employee_tree.insert('', 'end', values=employee)
            else:
                # Handle other employee types
                swapped_employee = employee[:4] + (employee[7],) + employee[5:7] + (employee[4],) + employee[8:]
                employee_tree.insert('', 'end', values=swapped_employee)


    # Frame for the View Employees section
    view_employee_frame = ttk.Frame(tab_view_employee)
    view_employee_frame.pack(fill='both', expand=True)

    # Combobox for filtering
    filter_var = tk.StringVar()
    employee_filter_combobox = ttk.Combobox(view_employee_frame, textvariable=filter_var, state='readonly', values=('All', 'Doctor', 'Nurse', 'Ward Boy'))
    employee_filter_combobox.pack(fill='x', padx=10, pady=5)
    employee_filter_combobox.set('All')
    employee_filter_combobox.bind('<<ComboboxSelected>>', lambda e: update_treeview())

    # # Treeview widget
    # columns = ('Employee_ID', 'First_Name', 'Last_Name', 'Phone', 'Gender', 'City', 'Street', 'Zip_Number', 'Type')
    # tree = ttk.Treeview(view_employee_frame, columns=columns, show='headings')
    employee_tree = ttk.Treeview(view_employee_frame, show='headings')
    employee_tree.pack(fill='both', expand=True)


    update_treeview()
    

def is_valid_date(date_str):
    """Check if the date string is in the format YYYY-MM-DD."""
    return bool(re.match(r'\d{4}-\d{2}-\d{2}', date_str))

def Add_Patient_Window():
    # Function to add a patient to the database
    def add_patient():
        # Here you'd retrieve the form data
        patient_id = entry_patient_id.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        phone = entry_phone.get()
        zip_number = entry_zip_number.get()
        city = entry_city.get()
        street = entry_street.get()
        gender = gender_var.get()
        age = entry_age.get()
        disease = entry_disease.get()
        birthdate = entry_birthdate.get()
        room_number = entry_room_number.get()

        if room_number and not Mapper.does_room_exist(room_number):
            messagebox.showerror("Error", "Room Number does not exist.")
            return
        
         # Check if nurse and room exist
        if not Mapper.does_room_exist(room_number):
            messagebox.showerror("Error", "Room Number does not exist.")
            return

        # You would normally validate and process these values here
        # For now, let's just print them to the console
        print(f"Patient ID: {patient_id}, First Name: {first_name}, Last Name: {last_name}, Phone: {phone}, Zip Number: {zip_number}, City: {city}, Street: {street}, Gender: {gender}, Age: {age}, Disease: {disease}, Birthdate: {birthdate}")

        

        # Insert the data into the database
        success, message = Mapper.insert_patient_into_db(patient_id, first_name, last_name, phone, zip_number, city, street, gender, age, disease, birthdate,room_number)
        if success:
            update_treeview(employee_tree, Mapper.get_patients)
            messagebox.showinfo("Success", message)

        else:
            messagebox.showerror("Error", message)

    # Frame for the Patient form
    patient_form_frame = ttk.Frame(tab_add_patient)
    patient_form_frame.pack(padx=10, pady=10, fill='x', expand=True)

    # 'Add Patient' label at the top
    add_patient_label = ttk.Label(patient_form_frame, text="Add Patient", font=('TkDefaultFont', 16))
    add_patient_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Patient_ID field
    ttk.Label(patient_form_frame, text="Patient ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_patient_id = ttk.Entry(patient_form_frame)
    entry_patient_id.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # First Name field
    ttk.Label(patient_form_frame, text="First Name:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_first_name = ttk.Entry(patient_form_frame)
    entry_first_name.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Last Name field
    ttk.Label(patient_form_frame, text="Last Name:").grid(row=3, column=0, sticky=tk.W, pady=2)
    entry_last_name = ttk.Entry(patient_form_frame)
    entry_last_name.grid(row=3, column=1, sticky=tk.EW, pady=2)

    # Phone field
    ttk.Label(patient_form_frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, pady=2)
    entry_phone = ttk.Entry(patient_form_frame)
    entry_phone.grid(row=4, column=1, sticky=tk.EW, pady=2)

    # Zip Number field
    ttk.Label(patient_form_frame, text="Zip Number:").grid(row=5, column=0, sticky=tk.W, pady=2)
    entry_zip_number = ttk.Entry(patient_form_frame)
    entry_zip_number.grid(row=5, column=1, sticky=tk.EW, pady=2)

    # City field
    ttk.Label(patient_form_frame, text="City:").grid(row=6, column=0, sticky=tk.W, pady=2)
    entry_city = ttk.Entry(patient_form_frame)
    entry_city.grid(row=6, column=1, sticky=tk.EW, pady=2)

    # Street field
    ttk.Label(patient_form_frame, text="Street:").grid(row=7, column=0, sticky=tk.W, pady=2)
    entry_street = ttk.Entry(patient_form_frame)
    entry_street.grid(row=7, column=1, sticky=tk.EW, pady=2)

    # Gender field
    ttk.Label(patient_form_frame, text="Gender:").grid(row=8, column=0, sticky=tk.W, pady=2)
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(patient_form_frame, textvariable=gender_var, state='readonly', values=('Male', 'Female'))
    gender_combobox.grid(row=8, column=1, sticky=tk.EW, pady=2)

    # Age field
    ttk.Label(patient_form_frame, text="Age:").grid(row=9, column=0, sticky=tk.W, pady=2)
    entry_age = ttk.Entry(patient_form_frame)
    entry_age.grid(row=9, column=1, sticky=tk.EW, pady=2)

    # Disease field
    ttk.Label(patient_form_frame, text="Disease:").grid(row=10, column=0, sticky=tk.W, pady=2)
    entry_disease = ttk.Entry(patient_form_frame)
    entry_disease.grid(row=10, column=1, sticky=tk.EW, pady=2)

    # Birthdate field
    ttk.Label(patient_form_frame, text="Birthdate (YYYY-MM-DD):").grid(row=11, column=0, sticky=tk.W, pady=2)
    entry_birthdate = ttk.Entry(patient_form_frame)
    entry_birthdate.grid(row=11, column=1, sticky=tk.EW, pady=2)

    # Room Number field
    ttk.Label(patient_form_frame, text="Room Number:").grid(row=12, column=0, sticky=tk.W, pady=2)
    entry_room_number = ttk.Entry(patient_form_frame)
    entry_room_number.grid(row=12, column=1, sticky=tk.EW, pady=2)

    # Add Patient button
    add_patient_button = ttk.Button(patient_form_frame, text="Add Patient", command=add_patient)
    add_patient_button.grid(row=13, column=0, columnspan=2, pady=10)
    
    # Configure the grid
    patient_form_frame.columnconfigure(1, weight=1)


def View_Patients_Window():
    global employee_tree
    def update_treeview():
        # Clear the existing entries in the treeview
        for item in employee_tree.get_children():
            employee_tree.delete(item)

        # Fetch and insert data
        patients = Mapper.get_patients()
        for patient in patients:
            employee_tree.insert('', 'end', values=patient)

    # Frame for the View Patients section
    view_patients_frame = ttk.Frame(tab_view_patient)
    view_patients_frame.pack(fill='both', expand=True)

    # Treeview widget
    columns = ('Patient_ID', 'First_Name', 'Last_Name', 'Phone', 'Zip_Number', 'City', 'Street', 'Gender', 'Age', 'Disease', 'Birthdate', 'Room_Number')  # Adjust columns as per your database
    employee_tree = ttk.Treeview(view_patients_frame, columns=columns, show='headings')
    employee_tree.pack(fill='both', expand=True)

    # Define the headings
    for col in columns:
        employee_tree.heading(col, text=col.replace('_', ' '))
        employee_tree.column(col, width=70 , anchor=tk.CENTER)

    # Initial population of the treeview
    update_treeview()

def Add_Room_Window():
    def add_room():
        room_number = entry_room_number.get()
        ward_boy_id = entry_ward_boy_id.get()
        room_type = room_type_var.get()
        status = status_var.get()

        # Check if Ward Boy ID exists
        if not Mapper.does_ward_boy_exist(ward_boy_id):
            messagebox.showerror("Error", "Ward Boy ID does not exist.")
            return

        # Insert the data into the database
        success, message = Mapper.insert_room_into_db(room_number, ward_boy_id, room_type, status)
        if success:
            update_treeview(room_tree, Mapper.get_rooms)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    room_form_frame = ttk.Frame(tab_add_room)
    room_form_frame.pack(padx=10, pady=10, fill='x', expand=True)

    # 'Add Patient' label at the top
    add_patient_label = ttk.Label(room_form_frame, text="Add Room", font=('TkDefaultFont', 16))
    add_patient_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Room Number field
    ttk.Label(room_form_frame, text="Room Number:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_room_number = ttk.Entry(room_form_frame)
    entry_room_number.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # Ward Boy ID field
    ttk.Label(room_form_frame, text="Ward Boy ID:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_ward_boy_id = ttk.Entry(room_form_frame)
    entry_ward_boy_id.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Room Type field
    ttk.Label(room_form_frame, text="Room Type:").grid(row=3, column=0, sticky=tk.W, pady=2)
    room_type_var = tk.StringVar()
    room_type_combobox = ttk.Combobox(room_form_frame, textvariable=room_type_var, state='readonly', values=('Type1', 'Type2', 'Type3'))  # Adjust the values as needed
    room_type_combobox.grid(row=3, column=1, sticky=tk.EW, pady=2)

    # Status field
    ttk.Label(room_form_frame, text="Status:").grid(row=4, column=0, sticky=tk.W, pady=2)
    status_var = tk.StringVar()
    status_combobox = ttk.Combobox(room_form_frame, textvariable=status_var, state='readonly', values=('Available', 'Occupied', 'Maintenance'))  # Adjust the values as needed
    status_combobox.grid(row=4, column=1, sticky=tk.EW, pady=2)

    # Add Room button
    add_room_button = ttk.Button(room_form_frame, text="Add Room", command=add_room)
    add_room_button.grid(row=5, column=0, columnspan=2, pady=10)

    room_form_frame.columnconfigure(1, weight=1)

def View_Rooms_Window():
    global room_tree
    def update_treeview():
        for item in room_tree.get_children():
            room_tree.delete(item)

        rooms = Mapper.get_rooms()
        for room in rooms:
            room_tree.insert('', 'end', values=room)

    view_rooms_frame = ttk.Frame(tab_view_room)
    view_rooms_frame.pack(fill='both', expand=True)

    columns = ('Room_Number', 'Ward_Boy_ID', 'Room_Type', 'Status')  # Adjust as per your table columns
    room_tree = ttk.Treeview(view_rooms_frame, columns=columns, show='headings')
    room_tree.pack(fill='both', expand=True)

    for col in columns:
        room_tree.heading(col, text=col.replace('_', ' '))
        room_tree.column(col,width = 80 , anchor=tk.CENTER)

    update_treeview()


def Add_Appointment_Window():
    def add_appointment():
        appointment_id = entry_appointment_id.get()
        doctor_id = entry_doctor_id.get()
        patient_id = entry_patient_id.get()
        cost = entry_cost.get()
        date = entry_date.get()

        # Check if doctor and patient IDs exist
        if not Mapper.does_doctor_exist(doctor_id):
            messagebox.showerror("Error", "Doctor ID does not exist.")
            return
        if not Mapper.does_patient_exist(patient_id):
            messagebox.showerror("Error", "Patient ID does not exist.")
            return

        # Insert the data into the database
        success, message = Mapper.insert_appointment_into_db(appointment_id, doctor_id, patient_id, cost, date)
        if success:
            update_treeview(appointment_tree, Mapper.get_appointments)

            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    appointment_form_frame = ttk.Frame(tab_add_appointment)
    appointment_form_frame.pack(padx=10, pady=10, fill='x', expand=True)

    # 'Add Patient' label at the top
    add_patient_label = ttk.Label(appointment_form_frame, text="Add Appointment", font=('TkDefaultFont', 16))
    add_patient_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
# Appointment ID field
    ttk.Label(appointment_form_frame, text="Appointment ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_appointment_id = ttk.Entry(appointment_form_frame)
    entry_appointment_id.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # Doctor ID field
    ttk.Label(appointment_form_frame, text="Doctor ID:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_doctor_id = ttk.Entry(appointment_form_frame)
    entry_doctor_id.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Patient ID field
    ttk.Label(appointment_form_frame, text="Patient ID:").grid(row=3, column=0, sticky=tk.W, pady=2)
    entry_patient_id = ttk.Entry(appointment_form_frame)
    entry_patient_id.grid(row=3, column=1, sticky=tk.EW, pady=2)

    # Cost field
    ttk.Label(appointment_form_frame, text="Cost:").grid(row=4, column=0, sticky=tk.W, pady=2)
    entry_cost = ttk.Entry(appointment_form_frame)
    entry_cost.grid(row=4, column=1, sticky=tk.EW, pady=2)

    # Date field
    ttk.Label(appointment_form_frame, text="Date (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.W, pady=2)
    entry_date = ttk.Entry(appointment_form_frame)
    entry_date.grid(row=5, column=1, sticky=tk.EW, pady=2)

    # Add Appointment button
    add_appointment_button = ttk.Button(appointment_form_frame, text="Add Appointment", command=add_appointment)
    add_appointment_button.grid(row=6, column=0, columnspan=2, pady=10)

    appointment_form_frame.columnconfigure(1, weight=1)

    # Add Appointment button
    add_appointment_button = ttk.Button(appointment_form_frame, text="Add Appointment", command=add_appointment)
    add_appointment_button.grid(row=6, column=0, columnspan=2, pady=10)

    appointment_form_frame.columnconfigure(1, weight=1)

def View_Appointments_Window():
    global appointment_tree
    def update_treeview():
        for item in appointment_tree.get_children():
            appointment_tree.delete(item)

        appointments = Mapper.get_appointments()
        for appointment in appointments:
            appointment_tree.insert('', 'end', values=appointment)

    # Frame for the View Appointments section
    view_appointments_frame = ttk.Frame(tab_view_appointment)
    view_appointments_frame.pack(fill='both', expand=True)

    # Treeview widget
    columns = ('Appointment_ID', 'Doctor_ID', 'Patient_ID', 'Cost', 'Date')  # Adjust as per your table columns
    appointment_tree = ttk.Treeview(view_appointments_frame, columns=columns, show='headings')
    appointment_tree.pack(fill='both', expand=True)

    for col in columns:
        appointment_tree.heading(col, text=col.replace('_', ' '))
        appointment_tree.column(col,width=80, anchor=tk.CENTER)

    # Initial population of the treeview
    update_treeview()

def Add_Helping_Window():
    def add_helping():
        doctor_id = entry_doctor_id.get()
        nurse_id = entry_nurse_id.get()

        # Check if doctor and nurse IDs exist
        if not Mapper.does_doctor_exist(doctor_id):
            messagebox.showerror("Error", "Doctor ID does not exist.")
            return
        if not Mapper.does_nurse_exist(nurse_id):
            messagebox.showerror("Error", "Nurse ID does not exist.")
            return

        # Insert the data into the database
        success, message = Mapper.insert_helping_into_db(doctor_id, nurse_id)
        if success:
            update_treeview(helping_tree, Mapper.get_helpings)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    helping_form_frame = ttk.Frame(tab_add_helping)
    helping_form_frame.pack(padx=10, pady=10, fill='x', expand=True)


     # 'Add Patient' label at the top
    add_patient_label = ttk.Label(helping_form_frame, text="Add Helping", font=('TkDefaultFont', 16))
    add_patient_label.grid(row=0, column=0, columnspan=2, pady=(0, 60))

    # Doctor ID field
    ttk.Label(helping_form_frame, text="Doctor ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_doctor_id = ttk.Entry(helping_form_frame)
    entry_doctor_id.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # Nurse ID field
    ttk.Label(helping_form_frame, text="Nurse ID:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_nurse_id = ttk.Entry(helping_form_frame)
    entry_nurse_id.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Add Helping button
    add_helping_button = ttk.Button(helping_form_frame, text="Add Helping", command=add_helping)
    add_helping_button.grid(row=3, column=0, columnspan=2, pady=10)

    helping_form_frame.columnconfigure(1, weight=1)

def View_Helpings_Window():
    global helping_tree
    def update_treeview():
        for item in helping_tree.get_children():
            helping_tree.delete(item)

        helpings = Mapper.get_helpings()
        for helping in helpings:
            helping_tree.insert('', 'end', values=helping)

    # Frame for the View Helpings section
    view_helpings_frame = ttk.Frame(tab_view_helping)
    view_helpings_frame.pack(fill='both', expand=True)

    # Treeview widget
    columns = ('Doctor_ID', 'Nurse_ID')  # Adjust as per your table columns
    helping_tree = ttk.Treeview(view_helpings_frame, columns=columns, show='headings')
    helping_tree.pack(fill='both', expand=True)

    for col in columns:
        helping_tree.heading(col, text=col.replace('_', ' '))
        helping_tree.column(col, anchor=tk.CENTER)

    # Initial population of the treeview
    update_treeview()

def Add_Govers_Window():
    def add_gover():
        nurse_id = entry_nurse_id.get()
        room_number = entry_room_number.get()

        # Check if nurse and room exist
        if not Mapper.does_nurse_exist(nurse_id):
            messagebox.showerror("Error", "Nurse ID does not exist.")
            return

        if not Mapper.does_room_exist(room_number):
            messagebox.showerror("Error", "Room Number does not exist.")
            return

        # Insert the data into the database
        success, message = Mapper.insert_gover_into_db(nurse_id, room_number)
        if success:
            update_treeview(govers_tree, Mapper.get_govers)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    gover_form_frame = ttk.Frame(tab_add_govers)
    gover_form_frame.pack(padx=10, pady=10, fill='x', expand=True)

    # Nurse ID field
    ttk.Label(gover_form_frame, text="Nurse ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
    entry_nurse_id = ttk.Entry(gover_form_frame)
    entry_nurse_id.grid(row=1, column=1, sticky=tk.EW, pady=2)

    # Room Number field
    ttk.Label(gover_form_frame, text="Room Number:").grid(row=2, column=0, sticky=tk.W, pady=2)
    entry_room_number = ttk.Entry(gover_form_frame)
    entry_room_number.grid(row=2, column=1, sticky=tk.EW, pady=2)

    # Add Gover button
    add_gover_button = ttk.Button(gover_form_frame, text="Add Gover", command=add_gover)
    add_gover_button.grid(row=3, column=0, columnspan=2, pady=10)

    gover_form_frame.columnconfigure(1, weight=1)

def View_Govers_Window():
    global govers_tree
    def update_treeview():
        for item in govers_tree.get_children():
            govers_tree.delete(item)

        govers = Mapper.get_govers()
        for gover in govers:
            govers_tree.insert('', 'end', values=gover)

    # Frame for the View Govers section
    view_govers_frame = ttk.Frame(tab_view_govers)
    view_govers_frame.pack(fill='both', expand=True)

    # Treeview widget
    columns = ('Nurse_ID', 'Room_Number')  # Adjust as per your table columns
    govers_tree = ttk.Treeview(view_govers_frame, columns=columns, show='headings')
    govers_tree.pack(fill='both', expand=True)

    for col in columns:
        govers_tree.heading(col, text=col.replace('_', ' '))
        govers_tree.column(col, anchor=tk.CENTER)

    # Initial population of the treeview
    update_treeview()

def execute_query():
    global result_tree
    query = query_textbox.get("1.0", tk.END).strip()

    # Clear existing data in the treeview
    result_tree.delete(*result_tree.get_children())

    try:
        # Execute the query
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        # Update the treeview columns
        result_tree['columns'] = column_names
        for col in column_names:
            result_tree.heading(col, text=col)
            result_tree.column(col,width=70, anchor=tk.CENTER)

        # Insert data into treeview
        for row in rows:
            result_tree.insert('', tk.END, values=row)

        connection.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def Query_Window():
    global query_textbox, result_tree

    query_frame = ttk.Frame(tab_query)
    query_frame.pack(fill='both', expand=True)

    # Query input frame
    query_input_frame = ttk.Frame(query_frame)
    query_input_frame.pack(fill='x', padx=10, pady=10)

    query_textbox = tk.Text(query_input_frame, height=7)
    query_textbox.pack(side=tk.LEFT, fill='x', expand=True)

    execute_button = ttk.Button(query_input_frame, text="Execute Query", command=execute_query)
    execute_button.pack(side=tk.RIGHT, padx=10)

    # Result display frame
    result_display_frame = ttk.Frame(query_frame)
    result_display_frame.pack(fill='both', expand=True)

    result_tree = ttk.Treeview(result_display_frame, show='headings')
    result_tree.pack(fill='both', expand=True)

# Main application window (initially hidden)
main_window = tk.Tk()
main_window.title("Hospital Management System")
main_window.geometry('1050x430')
main_window.withdraw()  # Hide the main window

# Define a tab control
tab_control = ttk.Notebook(main_window)

# Create a tab for each table
tab_employee = ttk.Frame(tab_control)
tab_view_employee = ttk.Frame(tab_control)
tab_add_patient = ttk.Frame(tab_control)
tab_view_patient = ttk.Frame(tab_control)
tab_add_room = ttk.Frame(tab_control)
tab_view_room = ttk.Frame(tab_control)
tab_add_appointment = ttk.Frame(tab_control)
tab_view_appointment = ttk.Frame(tab_control)
tab_add_helping = ttk.Frame(tab_control)
tab_view_helping = ttk.Frame(tab_control)
tab_add_govers = ttk.Frame(tab_control)
tab_view_govers = ttk.Frame(tab_control)
tab_query = ttk.Frame(tab_control)




tab_control.add(tab_employee, text='Add Employee')
tab_control.add(tab_view_employee, text='View Employees')
tab_control.add(tab_add_patient, text='Add Patient')
tab_control.add(tab_view_patient, text='View Patients')
tab_control.add(tab_add_room, text='Add Room')
tab_control.add(tab_view_room, text='View Room')
tab_control.add(tab_add_appointment, text='Add Appointment')
tab_control.add(tab_view_appointment, text='View Appointment')
tab_control.add(tab_add_helping, text='Add Helping')
tab_control.add(tab_view_helping, text='View Helpings')
tab_control.add(tab_add_govers, text='Add Govers')
tab_control.add(tab_view_govers, text='View Govers')
tab_control.add(tab_query, text='Query')





# Pack to make visible
tab_control.pack(expand=1, fill='both')

Add_Employee_Window()
View_Employee_Window()
Add_Patient_Window()
View_Patients_Window()
Add_Room_Window()
View_Rooms_Window()
Add_Appointment_Window()
View_Appointments_Window()
Add_Helping_Window()
View_Helpings_Window()
Add_Govers_Window()
View_Govers_Window()
Query_Window()
login_window()


# Start the GUI event loop
main_window.mainloop()
