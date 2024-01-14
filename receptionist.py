from tkcalendar import Calendar
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from database import cursor, mysql
import smtplib

def show_receptionist_dashboard():
    def return_to_main_menu(window_to_close):
        window_to_close.destroy()
        receptionist_dashboard.deiconify()

    def admit_discharge_management(parent_window):
        '''Functionality for admitting and discharging patients'''
        receptionist_dashboard.withdraw()

        def back(window_to_close):
            window_to_close.destroy()
            admit_discharge_management(parent_window)

        def admit_patient():
            feature_window.withdraw()
            '''Functionality for admitting a patient'''

            def admit():
                name = name_entry.get()
                patient_id = patient_id_entry.get()
                doctor_id = doctor_id_entry.get()

                if not name and patient_id and doctor_id:
                    error_message = f"Empty values"
                    messagebox.showerror("Error", error_message)

                # Validate if the patient and doctor exists in the database
                query = f"SELECT name, id FROM patient WHERE id = {patient_id} AND name = {name};"
                cursor.execute(query)
                patient = cursor.fetchone()
                if not patient:
                    error_message = f"Patient ID: {patient[1]} Name: {patient[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return

                query = f"SELECT name, id FROM doctor WHERE id = {doctor_id};"
                cursor.execute(query)
                doctor = cursor.fetchone()
                if not doctor:
                    error_message = f"Doctor ID: {doctor[1]} Name: {doctor[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return

                # Insert the patient details into the database (for the 'admitted_patients' table)
                # Replace with your SQL INSERT statement
                query = f"INSERT INTO admitted (patient_id, doctor_id) VALUES ({patient_id}, {doctor_id});"
                cursor.execute(query)
                mysql.commit()

                messagebox.showinfo("Success",f"Patient '{name}' admitted successfully under supervision of '{doctor[0]}'.")
                patient_admit_window.destroy()

            patient_admit_window = tk.Toplevel()
            patient_admit_window.title("Admit Patient")
            patient_admit_window.geometry("300x200+500+250")

            # Create labels and entry fields for patient details
            name_label = tk.Label(patient_admit_window, text="Name:")
            name_label.pack()
            name_entry = tk.Entry(patient_admit_window)
            name_entry.pack()

            patient_id_label = tk.Label(patient_admit_window, text="Patient ID:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(patient_admit_window)
            patient_id_entry.pack()

            doctor_id_label = tk.Label(patient_admit_window, text="Doctor ID:")
            doctor_id_label.pack()
            doctor_id_entry = tk.Entry(patient_admit_window)
            doctor_id_entry.pack()

            admit_button = tk.Button(patient_admit_window, text="Admit", command=admit)
            admit_button.pack()

            back_button = tk.Button(patient_admit_window, text="Back", command=lambda: back(patient_admit_window))
            back_button.pack()

        def discharge_patient():
            feature_window.withdraw()

            # Functionality for discharging a patient
            def discharge():
                patient_id = patient_id_entry.get()

                if not patient_id:
                    error_message = f"Empty values"
                    messagebox.showerror("Error", error_message)
                    return

                # Check if the entered patient ID is valid and exists in the database
                query = f"SELECT id FROM patient WHERE id = {patient_id};"
                cursor.execute(query)
                patient = cursor.fetchone()
                if not patient:
                    error_message = f"Patient ID: {patient[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return
                query = f"SELECT admit_date FROM admitted WHERE patient_id = {patient_id};"
                cursor.execute(query)
                patient = cursor.fetchone()
                if patient[0] is None:
                    error_message = f"Patient ID: {patient_id} is not admitted in the hospital"
                    messagebox.showerror("Error", error_message)
                    return
                query = "UPDATE admitted SET discharged_date = CURRENT_TIMESTAMP WHERE patient_id = %s"
                cursor.execute(query, (patient_id,))
                mysql.commit()

                messagebox.showinfo("Success", "Patient discharged successfully.")
                patient_discharge_window.destroy()

            patient_discharge_window = tk.Toplevel()
            patient_discharge_window.title("Discharge Patient")
            patient_discharge_window.geometry("200x100+500+250")

            # Create an entry field to input patient ID for discharge
            patient_id_label = tk.Label(patient_discharge_window, text="Patient ID:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(patient_discharge_window)
            patient_id_entry.pack()

            discharge_button = tk.Button(patient_discharge_window, text="Discharge", command=discharge)
            discharge_button.pack()

            back_button = tk.Button(patient_discharge_window, text="Back",command=lambda: back(patient_discharge_window))
            back_button.pack()

        feature_window = tk.Toplevel()
        feature_window.title("Admit/Discharge Management")
        feature_window.geometry("100x100+500+250")

        admit_button = tk.Button(feature_window, text="Admit Patient", command=admit_patient)
        admit_button.pack()

        discharge_button = tk.Button(feature_window, text="Discharge Patient", command=discharge_patient)
        discharge_button.pack()

        return_button = tk.Button(feature_window, text="Back to Main Menu",command=lambda: return_to_main_menu(feature_window))
        return_button.pack()

    def appointment_scheduling(parent_window):
        '''Functionality for scheduling patient appointments with doctors'''
        receptionist_dashboard.withdraw()

        def back(window_to_close):
            window_to_close.destroy()
            appointment_scheduling(parent_window)

        def show_appointments():
            feature_window.withdraw()
            appointments_window = tk.Tk()
            appointments_window.title("Appointments")

            all_appointments = tk.Frame(appointments_window)
            all_appointments.pack()

            all_appointments_label = tk.Label(all_appointments, text="All Appointments")
            all_appointments_label.pack()

            tree = ttk.Treeview(all_appointments, show="headings")
            tree["columns"] = ("Patient ID", "Doctor ID", "Appointment Date", "Appointment Time")

            tree.heading("Patient ID", text="Patient ID")
            tree.heading("Doctor ID", text="Doctor ID")
            tree.heading("Appointment Date", text="Appointment Date")
            tree.heading("Appointment Time", text="Appointment Time")
            # Fetch appointments data from the appointments table
            cursor.execute("SELECT * FROM appointments")
            appointments_data = cursor.fetchall()
            for appointment in appointments_data:
                tree.insert("", tk.END, values=(appointment[1], appointment[2], appointment[3], appointment[4]))
            # Adjusting column widths
            for col in ("Patient ID", "Doctor ID", "Appointment Date", "Appointment Time"):
                tree.column(col, anchor="center")
            tree.pack()

            # appointments_window.mainloop()

            back_button = tk.Button(appointments_window, text="Back", command=lambda: back(appointments_window))
            back_button.pack()

        def schedule_appointment():
            feature_window.withdraw()
            '''Functionality for scheduling an appointment'''

            def confirm_appointment():
                patient_id = patient_id_entry.get()
                doctor_id = doctor_id_entry.get()
                appointment_date = appointment_date_entry.get()
                appointment_time = appointment_time_entry.get()

                # Check if the patient exists
                cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
                patient = cursor.fetchone()

                # Check if the doctor exists
                cursor.execute("SELECT * FROM doctor WHERE id = %s", (doctor_id,))
                doctor = cursor.fetchone()

                if not patient:
                    messagebox.showerror("Error", f"Patient '{patient_id}' does not exist.")
                    return
                elif not doctor:
                    messagebox.showerror("Error", f"Doctor '{doctor_id}' does not exist.")
                    return
                else:
                    # Check doctor's availability at the specified date and time
                    cursor.execute(
                        "SELECT * FROM appointments WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s",
                        (doctor_id, appointment_date, appointment_time))
                    existing_appointment = cursor.fetchone()

                    if existing_appointment:
                        messagebox.showerror("Error",
                                             f"Doctor '{doctor_id}' is not available at the specified date and time.")
                        return
                    else:
                        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)"
                        values = (patient_id, doctor_id, appointment_date, appointment_time)
                        cursor.execute(query, values)
                        mysql.commit()

                        send_notification(patient_id, appointment_date, appointment_time)
                        messagebox.showinfo("Success", "Appointment scheduled successfully.")
                        appointment_window.destroy()
                        appointment_scheduling(parent_window)

            def get_selected_date():
                def on_date_select():
                    selected_date = cal.get_date()
                    today = datetime.now().date()
                    selected_date = datetime.strptime(selected_date, "%m/%d/%Y").date()  # Updated date format

                    if selected_date < today:
                        messagebox.showwarning("Warning", "Please select a date from today onwards.")
                    else:
                        appointment_date_entry.delete(0, tk.END)
                        appointment_date_entry.insert(0, str(selected_date))  # Updated date format
                        top.destroy()

                top = tk.Toplevel(appointment_window)
                cal = Calendar(top, selectmode="day", date_pattern="m/d/Y")  # Updated date format
                cal.pack(padx=20, pady=20)

                select_button = ttk.Button(top, text="Select Date", command=on_date_select)
                select_button.pack(pady=10)

            available_time_slots = [
                    "09:00", "10:00", "11:00",
                    "13:00", "14:00", "15:00",
                    "16:00", "17:00", "18:00"
            ]
            def get_selected_time(selected_date):
                def on_time_select():
                    selected_time = time_combobox.get()
                    if selected_time in available_time_slots:
                        appointment_time_entry.insert(0, time_combobox.get())
                        available_time_slots.remove(selected_time)
                        time_combobox['values'] = available_time_slots
                        time_combobox.set((available_time_slots[0]) if available_time_slots else None)
                        top.destroy()
                        appointment_time_entry.config(state="readonly")
                    else:
                        messagebox.showwarning("Warning", "Please select an available time slot.")

                top = tk.Toplevel(appointment_window)
                top.title("Time Selection")

                time_label = ttk.Label(top, text="Select Time:")
                time_label.pack(pady=10)

                time_combobox = ttk.Combobox(top, values=available_time_slots, state="readonly")
                time_combobox.pack(pady=10)
                time_combobox.set(available_time_slots[0]) if available_time_slots else None

                select_button = ttk.Button(top, text="Select Time", command=on_time_select)
                select_button.pack(pady=10)

            appointment_window = tk.Toplevel()
            appointment_window.title("Schedule Appointment")
            appointment_window.geometry("200x250+500+250")

            # Create labels and entry fields for appointment details
            patient_id_label = tk.Label(appointment_window, text="Patient id:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(appointment_window)
            patient_id_entry.pack()

            doctor_id_label = tk.Label(appointment_window, text="Doctor id:")
            doctor_id_label.pack()
            doctor_id_entry = tk.Entry(appointment_window)
            doctor_id_entry.pack()

            # see a way to get date and time like using a calendar
            appointment_date_label = tk.Label(appointment_window, text="Appointment Date (YYYY-MM-DD):")
            appointment_date_label.pack()
            appointment_date_entry = tk.Entry(appointment_window)
            appointment_date_entry.pack()
            appointment_date_entry.bind("<Button-1>", lambda event: get_selected_date())

            appointment_time_label = tk.Label(appointment_window, text="Appointment Time (HH:MM 24hr Clock):")
            appointment_time_label.pack()
            appointment_time_entry = tk.Entry(appointment_window)
            appointment_time_entry.pack()
            appointment_time_entry.bind("<Button-1>", lambda event: get_selected_time(appointment_date_entry.get()))

            confirm_button = tk.Button(appointment_window, text="Confirm Appointment", command=confirm_appointment)
            confirm_button.pack()

            back_button = tk.Button(appointment_window, text="Back", command=lambda: back(appointment_window))
            back_button.pack()

        def send_notification(patient_id, appointment_date, appointment_time):
            # Fetch patient's email from the database
            cursor.execute("SELECT email FROM patient WHERE id = %s", (patient_id,))
            patient_email = cursor.fetchone()[0]

            # Email configuration
            sender_email = 'appointments.cityhospital@gmail.com'
            password = 'llqi cfwt smqu eodp'
            subject = 'Appointment Confirmation'
            cursor.execute("SELECT name FROM patient WHERE id = %s", (patient_id,))
            patient_name = cursor.fetchone()[0]
            body = f"Subject: {subject}\n\nDear {patient_name},\n\nYour appointment has been scheduled for {appointment_date} at {appointment_time}.\n\nRegards,\nHospital Management"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_email, password)
            s.sendmail(sender_email, patient_email, body)
            s.quit()

        feature_window = tk.Toplevel()
        feature_window.title("Appointment Scheduling")

        schedule_button = tk.Button(feature_window, text="Schedule Appointment", command=schedule_appointment)
        schedule_button.pack()

        show_appointments_button = tk.Button(feature_window, text="Show All Appointments", command=show_appointments)
        show_appointments_button.pack()

        return_button = tk.Button(feature_window, text="Back to Main Menu",command=lambda: return_to_main_menu(feature_window))
        return_button.pack()

    def patient_information(parent_window):
        ''' Functionality for updating patient details'''
        receptionist_dashboard.withdraw()

        def back(window_to_close):
            window_to_close.destroy()
            patient_information(parent_window)

        def add_patient():
            '''Functionality to add a new patient'''
            feature_window.withdraw()

            def insert_patient():
                name = name_entry.get()
                age = age_entry.get()
                sex = sex_entry.get()
                blood_group = blood_group_entry.get()
                email = email_entry.get()
                contact = contact_entry.get()
                address = address_entry.get()
                illness_injury = illness_injury_entry.get()
                status = status_entry.get()

                # Insert the patient details into the database
                insert_query = "INSERT INTO patient (name, age, sex, blood_group, email, contact, address, illness_injury, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (name, age, sex, blood_group, email, contact, address, illness_injury, status)

                cursor.execute(insert_query, values)
                mysql.commit()

                messagebox.showinfo("Success", "Patient added successfully.")
                # Clear entry fields after adding a patient
                name_entry.delete(0, tk.END)
                age_entry.delete(0, tk.END)
                sex_entry.delete(0, tk.END)
                blood_group_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                contact_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END)
                illness_injury_entry.delete(0, tk.END)
                status_entry.delete(0, tk.END)
                # Clear other entry fields
                add_patient_window.mainloop()

            add_patient_window = tk.Toplevel()
            add_patient_window.title("Add New Patient")
            add_patient_window.geometry("150x700+500+250")

            # Create labels and entry fields for patient details
            name_label = ttk.Label(add_patient_window, text="Name:")
            name_label.pack()
            name_entry = ttk.Entry(add_patient_window)
            name_entry.pack(expand=True)

            age_label = ttk.Label(add_patient_window, text="Age:")
            age_label.pack()
            age_entry = ttk.Entry(add_patient_window)
            age_entry.pack()

            # make dropdown with values Male, Female, Other
            sex_label = ttk.Label(add_patient_window, text="Sex:")
            sex_label.pack()
            sex_entry = ttk.Combobox(add_patient_window, state="readonly")
            sex_entry["values"] = ("Male", "Female", "Other")
            sex_entry.pack()

            # make dropdown with values A+, B+, O+, AB+, A-, B-, O-, AB-
            blood_group_label = tk.Label(add_patient_window, text="Blood Group:")
            blood_group_label.pack()
            blood_group_entry = ttk.Combobox(add_patient_window, state="readonly")
            blood_group_entry['values'] = ("A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-")
            blood_group_entry.pack()

            email_label = ttk.Label(add_patient_window, text="Email:")
            email_label.pack()
            email_entry = ttk.Entry(add_patient_window)
            email_entry.pack(expand=True)

            contact_label = ttk.Label(add_patient_window, text="Contact:")
            contact_label.pack()
            contact_entry = ttk.Entry(add_patient_window)
            contact_entry.pack()

            address_label = ttk.Label(add_patient_window, text="Address:")
            address_label.pack()
            address_entry = ttk.Entry(add_patient_window)
            address_entry.pack(expand=True)

            illness_injury_label = ttk.Label(add_patient_window, text="Illness/Injury:")
            illness_injury_label.pack()
            illness_injury_entry = ttk.Entry(add_patient_window)
            illness_injury_entry.pack(expand=True)

            # dropdown with values inpatient, outpatient
            status_label = tk.Label(add_patient_window, text="Status:")
            status_label.pack()
            status_entry = ttk.Combobox(add_patient_window, state="readonly")
            status_entry['values'] = ("inpatient", "outpatient")
            status_entry.pack()

            add_button = ttk.Button(add_patient_window, text="Add", command=insert_patient)
            add_button.pack()

            back_button = ttk.Button(add_patient_window, text="Back", command=lambda: back(add_patient_window))
            back_button.pack()

        def view_patients():
            '''Functionality to view patient records'''
            feature_window.withdraw()

            def insert_to_treeview(treeview, patients, columns):
                # Insert data into the Treeview widget
                for patient in patients:
                    treeview.insert('', 'end', values=patient)

            view_patients_window = tk.Toplevel()
            view_patients_window.title("View Patients")

            admitted_frame = tk.Frame(view_patients_window)
            admitted_frame.pack(padx=10, pady=10)
            admitted_label = tk.Label(admitted_frame, text="Admitted Patients")
            admitted_label.pack()

            admitted_columns = ("ID", "Name", "Age", "Sex", "Blood Group", "Admit Date", "Discharged Date")
            admitted_treeview = ttk.Treeview(admitted_frame, columns=admitted_columns, show="headings")
            for col in admitted_columns:
                admitted_treeview.heading(col, text=col)
            admitted_treeview.pack()

            all_patients_frame = tk.Frame(view_patients_window)
            all_patients_frame.pack(padx=10, pady=10)
            all_patients_label = tk.Label(all_patients_frame, text="All Hospital Patients")
            all_patients_label.pack()

            all_patients_columns = ("ID", "Name", "Age", "Sex", "Blood Group", "Status")
            all_patients_treeview = ttk.Treeview(all_patients_frame, columns=all_patients_columns, show="headings")
            for col in all_patients_columns:
                all_patients_treeview.heading(col, text=col)
            for col in admitted_columns:
                admitted_treeview.column(col, anchor="center")
            all_patients_treeview.pack()

            # Retrieve admitted patients
            admitted_query = "SELECT patient.id, patient.name, patient.age, patient.sex, patient.blood_group, " \
                             "admitted.admit_date, admitted.discharged_date " \
                             "FROM admitted " \
                             "INNER JOIN patient ON admitted.patient_id = patient.id"

            # Retrieve all patients
            all_patients_query = "SELECT id, name, age, sex, blood_group, status FROM patient"

            # Execute the queries
            cursor.execute(admitted_query)
            admitted_patients = cursor.fetchall()

            cursor.execute(all_patients_query)
            all_hospital_patients = cursor.fetchall()

            # Insert data into Treeview for admitted patients
            insert_to_treeview(admitted_treeview, admitted_patients, admitted_columns)

            # Insert data into Treeview for all hospital patients
            insert_to_treeview(all_patients_treeview, all_hospital_patients, all_patients_columns)

            # view_patients_window.mainloop()

            back_button = tk.Button(view_patients_window, text="Back", command=lambda: back(view_patients_window))
            back_button.pack()

        def update_patient():
            '''Functionality for updating patient information'''
            feature_window.withdraw()

            def save_changes():
                patient_id = patient_id_entry.get()
                address = address_entry.get()
                contact = contact_entry.get()
                email = email_entry.get()
                status = status_entry.get()
                illness_injury = illness_injury_entry.get()
                # Check if the entered patient ID is valid and exists in the database
                if not patient_id:
                    error_message = f"Empty values"
                    messagebox.showerror("Error", error_message)
                    return

                # Check if the entered patient ID is valid and exists in the database
                query = f"SELECT id FROM patient WHERE id = {patient_id};"
                cursor.execute(query)
                patient = cursor.fetchone()
                if not patient:
                    error_message = f"Patient ID: {patient[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return

                # Create a list to store fields that need to be updated
                update_fields = []

                # Check each field and add it to the list if it's not empty
                if address:
                    update_fields.append(f"address = '{address}'")
                if contact:
                    update_fields.append(f"contact = '{contact}'")
                if email:
                    update_fields.append(f"email = '{email}'")
                if status:
                    update_fields.append(f"status = '{status}'")
                if illness_injury:
                    update_fields.append(f"illness_injury = '{illness_injury}'")

                # Check if at least one field is being updated
                if update_fields:
                    # Prepare SET clause for SQL UPDATE query
                    set_clause = ", ".join(update_fields)

                    # Update staff details in the database based on staff_id
                    update_query = f"UPDATE staff SET {set_clause} WHERE id = {patient_id}"
                    cursor.execute(update_query)
                    mysql.commit()

                    messagebox.showinfo("Success", "Staff information updated successfully.")
                    update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter at least one field to update.")
                    return

                query = "UPDATE patient SET address = %s, contact = %s, email = %s, status = %s, illness_injury = %s WHERE id = %s"
                values = (address, contact, email, status, illness_injury, patient_id)
                cursor.execute(query, values)
                mysql.commit()

                messagebox.showinfo("Success", "Patient information updated successfully.")
                update_window.destroy()

            update_window = tk.Toplevel()
            update_window.title("Update Patient Information")
            update_window.geometry("150x600+500+250")

            # Create labels and entry fields for updating patient details
            patient_id_label = tk.Label(update_window, text="Patient ID:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(update_window)
            patient_id_entry.pack()

            email_label = tk.Label(update_window, text="Email:")
            email_label.pack()
            email_entry = tk.Entry(update_window)
            email_entry.pack()

            contact_label = tk.Label(update_window, text="Contact:")
            contact_label.pack()
            contact_entry = tk.Entry(update_window)
            contact_entry.pack()

            address_label = tk.Label(update_window, text="Address:")
            address_label.pack()
            address_entry = tk.Entry(update_window)
            address_entry.pack()

            illness_injury_label = tk.Label(update_window, text="Illness/Injury:")
            illness_injury_label.pack()
            illness_injury_entry = tk.Entry(update_window)
            illness_injury_entry.pack()

            # make dropdown with values -> inpatient and outpatient
            status_label = tk.Label(update_window, text="Status:")
            status_label.pack()
            status_entry = ttk.Combobox(update_window, state="readonly")
            status_entry['values'] = ("inpatient", "outpatient")
            status_entry.pack()

            save_button = tk.Button(update_window, text="Save Changes", command=save_changes)
            save_button.pack()

            back_button = tk.Button(update_window, text="Back", command=lambda: back(update_window))
            back_button.pack()

        feature_window = tk.Toplevel()
        feature_window.title("Patient Information")

        add_patient_button = tk.Button(feature_window, text="Add Patient", command=add_patient)
        add_patient_button.pack()

        view_patients_button = tk.Button(feature_window, text="View Patients", command=view_patients)
        view_patients_button.pack()

        update_button = tk.Button(feature_window, text="Update Patient Details", command=update_patient)
        update_button.pack()

        return_button = tk.Button(feature_window, text="Back to Main Menu",
                                  command=lambda: return_to_main_menu(feature_window))
        return_button.pack()

    receptionist_dashboard = tk.Tk()
    receptionist_dashboard.title("Receptionist Dashboard")
    receptionist_dashboard.geometry("300x100+500+250")

    main_menu = tk.Frame(receptionist_dashboard)
    main_menu.pack()

    admit_discharge_button = tk.Button(main_menu, text="Admit/Discharge Management",
                                       command=lambda: admit_discharge_management(main_menu))
    admit_discharge_button.pack()

    appointment_button = tk.Button(main_menu, text="Appointment Scheduling",
                                   command=lambda: appointment_scheduling(main_menu))
    appointment_button.pack()

    update_info_button = tk.Button(main_menu, text="Patient Information",
                                   command=lambda: patient_information(main_menu))
    update_info_button.pack()

    receptionist_dashboard.mainloop()
