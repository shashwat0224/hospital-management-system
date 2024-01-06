import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage
from database import cursor, mysql

'''
 in add_patients and update patients need to use combobox for sex,bloodgroup,etc.
'''

'''
 have to change
'''
def show_admin_dashboard():
    def return_to_main_menu(window_to_close):
        window_to_close.destroy()
        admin_dashboard.deiconify()

    def manage_staff(parent_window):
        admin_dashboard.withdraw()
        def back(window_to_close):
                window_to_close.destroy()
                manage_staff(parent_window)
        def add_staff():
            staff_management_window.withdraw()
            def add_to_database():
                # Function to add staff details to the database
                name = name_entry.get()
                job_title = job_title_entry.get()
                contact = contact_entry.get()
                address = address_entry.get()
                email = email_entry.get()
                # Check if required fields are not empty before inserting into the database
                if name and job_title and email and  contact and address:
                    # Insert staff details into the database
                    query = "INSERT INTO staff (name, job_title, contact, address, email) VALUES (%s, %s, %s, %s, %s)"
                    values = (name, job_title, contact, address, email)
                    cursor.execute(query, values)
                    mysql.commit()

                    messagebox.showinfo("Success", "Staff added successfully.")
                    staff_add_window.destroy()
                    back(manage_staff)

                else:
                    messagebox.showerror("Error", "Please fill in all required fields.")
                    return

            # Create a new window for adding staff
            staff_add_window = tk.Toplevel()
            staff_add_window.title("Add Staff")

            # Labels and Entry fields for staff details
            name_label = tk.Label(staff_add_window, text="Name:")
            name_label.pack()
            name_entry = tk.Entry(staff_add_window)
            name_entry.pack()

            job_title_label = tk.Label(staff_add_window, text="Job Title:")
            job_title_label.pack()
            job_title_entry = tk.Entry(staff_add_window)
            job_title_entry.pack()

            email_label = tk.Label(staff_add_window, text="Email:")
            email_label.pack()
            email_entry = tk.Entry(staff_add_window)
            email_entry.pack()

            contact_label = tk.Label(staff_add_window, text="Contact:")
            contact_label.pack()
            contact_entry = tk.Entry(staff_add_window)
            contact_entry.pack()

            address_label = tk.Label(staff_add_window, text="Address:")
            address_label.pack()
            address_entry = tk.Entry(staff_add_window)
            address_entry.pack()

            # Button to add staff details to the database
            add_button = tk.Button(staff_add_window, text="Add", command=add_to_database)
            add_button.pack()

            back_button = tk.Button(staff_add_window, text="Back", command=lambda: back(staff_add_window))
            back_button.pack()

            staff_add_window.mainloop()

        def update_staff():
            staff_management_window.withdraw()
            def update_in_database():
                # Function to update staff details in the database
                staff_id = staff_id_entry.get()

                query = f"SELECT name, id FROM staff WHERE id = {staff_id};"
                cursor.execute(query)
                staff = cursor.fetchone()
                if not staff:
                    error_message = f"Staff ID: {staff[1]} Name: {staff[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return

                # Retrieve updated information from entry fields
                new_job_title = new_job_title_entry.get()
                new_email = new_email_entry.get()
                new_contact = new_contact_entry.get()
                new_address = new_address_entry.get()

                # Create a list to store fields that need to be updated
                update_fields = []

                # Check each field and add it to the list if it's not empty
                if new_job_title:
                    update_fields.append(f"job_title = '{new_job_title}'")
                if new_email:
                    update_fields.append(f"email = '{new_email}'")
                if new_contact:
                    update_fields.append(f"contact = '{new_contact}'")
                if new_address:
                    update_fields.append(f"address = '{new_address}'")

                # Check if at least one field is being updated
                if update_fields:
                    # Prepare SET clause for SQL UPDATE query
                    set_clause = ", ".join(update_fields)

                    # Update staff details in the database based on staff_id
                    update_query = f"UPDATE staff SET {set_clause} WHERE id = {staff_id}"
                    cursor.execute(update_query)
                    mysql.commit()

                    messagebox.showinfo("Success", "Staff information updated successfully.")
                    staff_update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter at least one field to update.")
                    return

            # Create a window for updating staff information
            staff_update_window = tk.Toplevel()
            staff_update_window.title("Update Staff Information")

            # Labels and Entry fields for staff details to update
            staff_id_label = tk.Label(staff_update_window, text="Staff ID:")
            staff_id_label.pack()
            staff_id_entry = tk.Entry(staff_update_window)
            staff_id_entry.pack()

            # Entry fields for updated information
            new_job_title_label = tk.Label(staff_update_window, text="New Job Title:")
            new_job_title_label.pack()
            new_job_title_entry = tk.Entry(staff_update_window)
            new_job_title_entry.pack()

            new_email_label = tk.Label(staff_update_window, text="New Email:")
            new_email_label.pack()
            new_email_entry = tk.Entry(staff_update_window)
            new_email_entry.pack()

            new_contact_label = tk.Label(staff_update_window, text="New Contact:")
            new_contact_label.pack()
            new_contact_entry = tk.Entry(staff_update_window)
            new_contact_entry.pack()

            new_address_label = tk.Label(staff_update_window, text="New Address:")
            new_address_label.pack()
            new_address_entry = tk.Entry(staff_update_window)
            new_address_entry.pack()

            # Button to update staff details in the database
            update_button = tk.Button(staff_update_window, text="Update", command=update_in_database)
            update_button.pack()

            back_button = tk.Button(staff_update_window, text="Back", command=lambda: back(staff_update_window))
            back_button.pack()

            staff_update_window.mainloop()

        def delete_staff():
            staff_management_window.withdraw()
            def delete_from_database():
                # Function to delete staff member from the database
                staff_id = staff_id_entry.get()

                query = f"SELECT name, id FROM staff WHERE id = {staff_id};"
                cursor.execute(query)
                staff = cursor.fetchone()
                if not staff:
                    error_message = f"Staff ID: {staff[1]} Name: {staff[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return

                # Check if staff ID is not empty before deleting from the database
                if staff_id:
                    # Delete staff member from the database based on staff_id
                    delete_query = "DELETE FROM staff_details WHERE ID = %s"
                    cursor.execute(delete_query, (staff_id,))
                    mysql.commit()

                    messagebox.showinfo("Success", "Staff member deleted successfully.")
                    staff_delete_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter staff ID.")
                    return

            # Create a window for deleting a staff member
            staff_delete_window = tk.Toplevel()
            staff_delete_window.title("Delete Staff Member")

            # Label and Entry field for staff ID to delete
            staff_id_label = tk.Label(staff_delete_window, text="Staff ID:")
            staff_id_label.pack()
            staff_id_entry = tk.Entry(staff_delete_window)
            staff_id_entry.pack()

            # Button to delete staff member from the database
            delete_button = tk.Button(staff_delete_window, text="Delete", command=delete_from_database)
            delete_button.pack()

            back_button = tk.Button(staff_delete_window, text="Back", command=lambda: back(staff_delete_window))
            back_button.pack()

            staff_delete_window.mainloop()

        # Create the main window for managing staff
        staff_management_window = tk.Tk()
        staff_management_window.title("Staff Management")

        add_staff_button = tk.Button(staff_management_window, text="Add Staff", command=add_staff)
        add_staff_button.pack()

        update_staff_button = tk.Button(staff_management_window, text="Update Staff Information", command=update_staff)
        update_staff_button.pack()

        delete_staff_button = tk.Button(staff_management_window, text="Delete Staff", command=delete_staff)
        delete_staff_button.pack()

        return_button = tk.Button(staff_management_window, text="Back to Main Menu", command=lambda: return_to_main_menu(staff_management_window))
        return_button.pack()

        staff_management_window.mainloop()

    def manage_patient_records(parent_window):
        admin_dashboard.withdraw()
        def back(window_to_close):
            window_to_close.destroy()
            manage_patient_records(parent_window)
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

            # Create labels and entry fields for patient details
            name_label = tk.Label(add_patient_window, text="Name:")
            name_label.pack()
            name_entry = tk.Entry(add_patient_window)
            name_entry.pack(expand=True)

            age_label = tk.Label(add_patient_window, text="Age:")
            age_label.pack()
            age_entry = tk.Entry(add_patient_window)
            age_entry.pack()

            #make dropdown with values Male, Female, Other
            sex_label = tk.Label(add_patient_window, text="Sex:")
            sex_label.pack()
            sex_entry = tk.Combobox(add_patient_window)
            sex_entry["values"] = ("Male", "Female", "Other")
            sex_entry.pack()

             # Create labels and entry fields for patient details
            name_label = ttk.Label(add_patient_window, text="Name:")
            name_label.pack()
            name_entry = ttk.Entry(add_patient_window)
            name_entry.pack(expand=True)

            age_label = ttk.Label(add_patient_window, text="Age:")
            age_label.pack()
            age_entry = ttk.Entry(add_patient_window)
            age_entry.pack()

            #make dropdown with values Male, Female, Other
            sex_label = ttk.Label(add_patient_window, text="Sex:")
            sex_label.pack()
            sex_entry = ttk.Combobox(add_patient_window)
            sex_entry["values"] = ("Male", "Female", "Other")
            sex_entry.pack()

            # make dropdown with values A+, B+, O+, AB+, A-, B-, O-, AB-
            blood_group_label = tk.Label(add_patient_window, text="Blood Group:")
            blood_group_label.pack()
            blood_group_entry = ttk.Combobox(add_patient_window)
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
            status_entry = ttk.Combobox(add_patient_window)
            status_entry['values'] = ("inpatient", "outpatient")
            status_entry.pack()

            add_button = tk.Button(add_patient_window, text="Add", command=insert_patient)
            add_button.pack()

            back_button = tk.Button(add_patient_window, text="Back", command=lambda: back(add_patient_window))
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
                if not patient_id : 
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
                
                query = "UPDATE patient SET address = %s, contact = %s, email = %s, status = %s, illness_injury = %s WHERE id = %s"
                values = (address, contact, email, status, illness_injury, patient_id) 
                cursor.execute(query, values)
                mysql.commit()

                messagebox.showinfo("Success", "Patient information updated successfully.")
                update_window.destroy()

            update_window = tk.Toplevel()
            update_window.title("Update Patient Information")

            # Create labels and entry fields for updating patient details
            patient_id_label = tk.Label(update_window, text="Patient ID:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(update_window)
            patient_id_entry.pack()

            email_label = tk.Label(update_window, text="Email:")
            email_label.pack()
            email_entry = tk.Entry(update_window)
            email_entry.pack(expand=True)

            contact_label = tk.Label(update_window, text="Contact:")
            contact_label.pack()
            contact_entry = tk.Entry(update_window)
            contact_entry.pack()

            address_label = tk.Label(update_window, text="Address:")
            address_label.pack()
            address_entry = tk.Entry(update_window)
            address_entry.pack(expand=True)

            illness_injury_label = tk.Label(update_window, text="Illness/Injury:")
            illness_injury_label.pack()
            illness_injury_entry = tk.Entry(update_window)
            illness_injury_entry.pack(expand=True)

            # make dropdown with values -> inpatient and outpatient
            status_label = tk.Label(update_window, text="Status:")
            status_label.pack()
            status_entry = tk.Entry(update_window)
            status_entry.pack()

            save_button = tk.Button(update_window, text="Save Changes", command=save_changes)
            save_button.pack()

            back_button = tk.Button(update_window, text="Back", command=lambda: back(update_window))
            back_button.pack()

        def delete_patient():
            '''Functionality to delete a patient'''
            feature_window.withdraw()
            def delete_from_db():
                patient_id = patient_id_entry.get()
                delete_query = "DELETE FROM patient WHERE ID = %s"
                cursor.execute(delete_query, (patient_id,))
                mysql.commit()

                messagebox.showinfo("Success", "Patient deleted successfully.")
                delete_patient_window.destroy()

            delete_patient_window = tk.Toplevel()
            delete_patient_window.title("Delete Patient")

            # Entry field for patient ID to be deleted
            patient_id_label = tk.Label(delete_patient_window, text="Patient ID:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(delete_patient_window)
            patient_id_entry.pack()

            delete_button = tk.Button(delete_patient_window, text="Delete", command=delete_from_db)
            delete_button.pack()

            back_button = tk.Button(delete_patient_window, text="Back", command=lambda: back(delete_patient_window))
            back_button.pack()

        feature_window = tk.Toplevel()
        feature_window.title("Patient Information")

        add_patient_button = tk.Button(feature_window, text="Add Patient", command=add_patient)
        add_patient_button.pack()

        view_patients_button = tk.Button(feature_window, text="View Patients", command=view_patients)
        view_patients_button.pack()

        update_button = tk.Button(feature_window, text="Update Patient Details", command=update_patient)
        update_button.pack()

        delete_patient_button = tk.Button(feature_window, text="Delete Patient", command=delete_patient)
        delete_patient_button.pack()

        return_button = tk.Button(feature_window, text="Back to Main Menu", command=lambda: return_to_main_menu(feature_window))
        return_button.pack()

        feature_window.mainloop()

    def analytics_reports():
        admin_dashboard.withdraw()
        # Fetch data from the database (For example: Number of patients in different age groups)
        cursor.execute("SELECT Age, COUNT(*) FROM patient GROUP BY Age")
        data = cursor.fetchall()

        ages = [row[0] for row in data]
        patient_count = [row[1] for row in data]

        # Create a bar chart for age distribution
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(ages, patient_count, color='skyblue')
        plt.xlabel('Age')
        plt.ylabel('Number of Patients')
        plt.title('Distribution of Patients by Age Group')
        plt.grid(True)

        # Fetch data for gender distribution
        cursor.execute("SELECT Sex, COUNT(*) FROM patient GROUP BY Sex")
        gender_data = cursor.fetchall()

        genders = [row[0] for row in gender_data]
        gender_count = [row[1] for row in gender_data]

        # Create a pie chart for gender distribution
        plt.subplot(1, 2, 2)
        plt.pie(gender_count, labels=genders, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Gender Distribution of Admitted Patients')

        plt.tight_layout()
        plt.show()

    def view_update_doctor_info(parent_window):
        admin_dashboard.withdraw()
        def back(window_to_close):
            window_to_close.destroy()
            view_update_doctor_info(parent_window)
        def view_doctor_information():
            doctor_info_window.withdraw()
            cursor.execute("SELECT * FROM doctor")
            doctor_data = cursor.fetchall()

            view_window = tk.Toplevel()
            view_window.title("View Doctor Information")

            # Create a Treeview widget to display doctor information in a table
            tree = ttk.Treeview(view_window, columns=("ID", "Name", "Specialization", "Fees", "Contact", "Address", "Email"))
            tree.heading("#0", text="Index")
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Specialization", text="Specialization")
            tree.heading("Fees", text="Fees")
            tree.heading("Contact", text="Contact")
            tree.heading("Address", text="Address")
            tree.heading("Email", text="Email")

            tree.column("#0", width=50)
            tree.column("ID", width=50)
            tree.column("Name", width=100)
            tree.column("Specialization", width=150)
            tree.column("Fees", width=100)
            tree.column("Contact", width=100)
            tree.column("Address", width=200)
            tree.column("Email", width=150)

            tree.pack(expand=True, fill=tk.BOTH)

            # Insert doctor details into the Treeview
            for index, doctor in enumerate(doctor_data, start=1):
                tree.insert("", "end", text=str(index), values=doctor)

            back_button = tk.Button(view_window, text="Back", command=lambda: back(view_window))
            back_button.pack()

            view_window.mainloop()

        def update_doctor_information():
            doctor_info_window.withdraw()
            def save_changes():
                # Functionality for updating doctor information in the database
                doctor_id = doctor_id_entry.get()
                # Check if the entered doctor ID is valid and exists in the database
                if not doctor_id : 
                    error_message = f"Empty values"
                    messagebox.showerror("Error", error_message)
                    return

                # Check if the entered patient ID is valid and exists in the database
                query = f"SELECT id FROM doctor WHERE id = {doctor_id};"
                cursor.execute(query)
                doctor = cursor.fetchone()
                if not doctor:
                    error_message = f"doctor ID: {doctor[0]} is not found in the database"
                    messagebox.showerror("Error", error_message)
                    return
                # Retrieve updated information from entry fields
                new_specialization = new_specialization_entry.get()
                new_contact = new_contact_entry.get()
                new_address = new_address_entry.get()

                # Create a list to store fields that need to be updated
                update_fields = []

                # Check each field and add it to the list if it's not empty
                if new_specialization:
                    update_fields.append(f"Specialization = '{new_specialization}'")
                if new_contact:
                    update_fields.append(f"Contact = '{new_contact}'")
                if new_address:
                    update_fields.append(f"Address = '{new_address}'")

                # Check if at least one field is being updated
                if update_fields:
                    # Prepare SET clause for SQL UPDATE query
                    set_clause = ", ".join(update_fields)

                    # Update doctor details in the database based on doctor_id
                    update_query = f"UPDATE doctor SET {set_clause} WHERE id = {doctor_id}"
                    cursor.execute(update_query)
                    mysql.commit()

                    messagebox.showinfo("Success", "Doctor information updated successfully.")
                    doctor_update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter at least one field to update.")
                    return

            # Create a window for updating doctor information
            doctor_update_window = tk.Toplevel()
            doctor_update_window.title("Update Doctor Information")

            # Labels and Entry fields for doctor details to update
            doctor_id_label = tk.Label(doctor_update_window, text="Doctor ID:")
            doctor_id_label.pack()
            doctor_id_entry = tk.Entry(doctor_update_window)
            doctor_id_entry.pack()

            # Entry fields for updated information
            new_specialization_label = tk.Label(doctor_update_window, text="New Specialization:")
            new_specialization_label.pack()
            new_specialization_entry = tk.Entry(doctor_update_window)
            new_specialization_entry.pack()

            new_contact_label = tk.Label(doctor_update_window, text="New Contact:")
            new_contact_label.pack()
            new_contact_entry = tk.Entry(doctor_update_window)
            new_contact_entry.pack()

            new_address_label = tk.Label(doctor_update_window, text="New Address:")
            new_address_label.pack()
            new_address_entry = tk.Entry(doctor_update_window)
            new_address_entry.pack()

            # Button to update doctor details in the database
            update_button = tk.Button(doctor_update_window, text="Update", command=save_changes)
            update_button.pack()

            back_button = tk.Button(doctor_update_window, text="Back", command=lambda: back(doctor_update_window))
            back_button.pack()

            doctor_update_window.mainloop()

        # Create the main window for viewing and updating doctor information
        doctor_info_window = tk.Toplevel()
        doctor_info_window.title("View/Update Doctor Information")

        view_info_button = tk.Button(doctor_info_window, text="View Doctor Information", command=view_doctor_information)
        view_info_button.pack()

        update_info_button = tk.Button(doctor_info_window, text="Update Doctor Information", command=update_doctor_information)
        update_info_button.pack()

        return_button = tk.Button(doctor_info_window, text="Back to Main Menu", command=lambda: return_to_main_menu(doctor_info_window))
        return_button.pack()

        doctor_info_window.mainloop()

    def appointment_scheduling_notifications(parent_window):
        admin_dashboard.withdraw()
        def back(window_to_close):
            window_to_close.destroy()
            appointment_scheduling_notifications(parent_window)
        def schedule_appointment():
            appointment_schedule_window.withdraw()
            def check_schedule():
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
                    cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s",
                                (doctor_id, appointment_date, appointment_time))
                    existing_appointment = cursor.fetchone()

                    if existing_appointment:
                        messagebox.showerror("Error", f"Doctor '{doctor_id}' is not available at the specified date and time.")
                        return
                    else:
                        # Schedule the appointment
                        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s)"
                        values = (patient_id, doctor_id, appointment_date, appointment_time)
                        cursor.execute(query, values)
                        mysql.commit()

                        messagebox.showinfo("Success", "Appointment scheduled successfully.")
                        send_notification(patient_id, appointment_date, appointment_time)
                        schedule_window.destroy()

            schedule_window = tk.Toplevel()
            schedule_window.title("Schedule Appointment")

            # Labels and entry fields for scheduling appointment
            patient_id_label = tk.Label(schedule_window, text="Patient Id:")
            patient_id_label.pack()
            patient_id_entry = tk.Entry(schedule_window)
            patient_id_entry.pack()

            doctor_id_label = tk.Label(schedule_window, text="Doctor Id:")
            doctor_id_label.pack()
            doctor_id_entry = tk.Entry(schedule_window)
            doctor_id_entry.pack()

            appointment_date_label = tk.Label(schedule_window, text="Appointment Date (YYYY-MM-DD):")
            appointment_date_label.pack()
            appointment_date_entry = tk.Entry(schedule_window)
            appointment_date_entry.pack()

            appointment_time_label = tk.Label(schedule_window, text="Appointment Time (HH:MM AM/PM):")
            appointment_time_label.pack()
            appointment_time_entry = tk.Entry(schedule_window)
            appointment_time_entry.pack()

            schedule_button = tk.Button(schedule_window, text="Schedule", command=check_schedule)
            schedule_button.pack()

            back_button = tk.Button(schedule_window, text="Back", command=lambda: back(schedule_window))
            back_button.pack()

            schedule_window.mainloop()

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
            s.starttls() #Puts connection to smtp server in Tls mode
            s.login(sender_email, password)
            s.sendmail(sender_email, patient_email, body)
            s.quit()
        
        appointment_schedule_window = tk.Toplevel()
        appointment_schedule_window.title("Appointment Scheduling and Notifications")

        schedule_appointment_button = tk.Button(appointment_schedule_window, text="Schedule Appointment", command=schedule_appointment)
        schedule_appointment_button.pack()

        return_button = tk.Button(appointment_schedule_window, text="Back to Main Menu", command=lambda: return_to_main_menu(appointment_schedule_window))
        return_button.pack()

        appointment_schedule_window.mainloop()

    admin_dashboard = tk.Tk()
    admin_dashboard.title("Admin Dashboard")

    main_menu = tk.Frame(admin_dashboard)
    main_menu.pack()
    staff_management_button = tk.Button(main_menu, text="Manage Staff", command=lambda: manage_staff(main_menu))
    staff_management_button.pack()

    manage_records_button = tk.Button(main_menu, text="Manage Patient Records", command=lambda: manage_patient_records(main_menu))
    manage_records_button.pack()

    analytics_reports_button = tk.Button(main_menu, text="Analytics/Reports", command=analytics_reports)
    analytics_reports_button.pack()

    view_update_doctor_info_button = tk.Button(main_menu, text="View/Update Doctor Information", command=lambda: view_update_doctor_info(main_menu))
    view_update_doctor_info_button.pack()

    appointment_scheduling_button = tk.Button(main_menu, text="Appointment Scheduling/Notifications", command=lambda: appointment_scheduling_notifications(main_menu))
    appointment_scheduling_button.pack()

    admin_dashboard.mainloop()