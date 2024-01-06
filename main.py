import tkinter as tk
from receptionist import show_receptionist_dashboard
from admin import show_admin_dashboard

def validate_login_fields():
    '''Function to check if username and password fields are filled'''
    if username_entry.get() and password_entry.get():
        login_button.config(state="normal")
    else:
        login_button.config(state="disabled")

def authenticate():
    '''Function to handle login authentication'''
    print("in authenticate")
    username = username_entry.get()
    password = password_entry.get()

    if username == 'admin' and password == 'admin1234':
        root.destroy()
        show_admin_dashboard()
    elif username == 'dummy' and password == 'dummy1234':
        root.destroy()
        show_receptionist_dashboard()
    
    else:
        error_message = "Invalid username and/or password."
        show_error(error_message)
        # print("Invalid username and password")

def show_error(text:str):
    error_label.config(text=text)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Hospital Management System")

# Login Page
login_frame = tk.Frame(root)
login_frame.pack(padx=20, pady=20)

username_label = tk.Label(login_frame, text="Username:")
username_label.pack()

username_entry = tk.Entry(login_frame)
username_entry.pack()
username_entry.bind("<KeyRelease>", lambda event: validate_login_fields())  # Call validate function on key release

password_label = tk.Label(login_frame, text="Password:")
password_label.pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()
password_entry.bind("<KeyRelease>", lambda event: validate_login_fields())  # Call validate function on key release

error_label = tk.Label(login_frame, text="", fg="red")
error_label.pack()

login_button = tk.Button(login_frame, text="Login", command=authenticate, state="disabled")
login_button.pack()

# Admin Dashboard
admin_dashboard_frame = tk.Frame(root)
# Place admin dashboard components in this frame

# Receptionist Dashboard
receptionist_dashboard_frame = tk.Frame(root)
# Place receptionist dashboard components in this frame

root.mainloop()
