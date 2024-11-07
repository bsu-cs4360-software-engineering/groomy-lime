import tkinter as tk
import tkinter.messagebox as messagebox
from user_manager import UserManager
from customer_service import CustomerService
from appointment_service import AppointmentService
import sqlite3

# SHARED database
conn = sqlite3.connect('app.db')
conn.row_factory = sqlite3.Row  # returns the rows as dictionaries
conn.execute('PRAGMA foreign_keys = ON')  # foreign keys supported
customer_service = CustomerService(conn)
appointment_service = AppointmentService(conn)

# main window creation
home = tk.Tk()
home.geometry("1600x900")
home.title("Groomy") # title of the screen

# creates the UserManager instance
user_manager = UserManager('users.db')

def create_sidebar():
    global home_btn, customers_btn, appointments_btn

    sidebar = tk.Frame(home, bg='#156082', width=225, bd=2, relief='solid')
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    # create sidebar buttons for each window
    home_btn = tk.Button(sidebar, text="HOME", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_home)
    home_btn.pack(pady=(100,10))

    customers_btn = tk.Button(sidebar, text="CUSTOMERS", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_customers)
    customers_btn.pack(pady=10)

    appointments_btn = tk.Button(sidebar, text="APPOINTMENTS", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_appointments)
    appointments_btn.pack(pady=10)

def show_home():
    clear_window()
    reset_sidebar_buttons()
    tk.Label(main_frame, text="Groomy", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5) # creates the label at the top left (this can probably be made into a function later)
    home_btn.config(bg='#1d81af')

    # username and password inputs
    create_login_form()


# Login functions
def create_login_form():

    # frame to put the username and password inputs at the center of the screen
    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True) # centers the items

    # username input/label

    username_label = tk.Label(form_frame, text="Username", fg='black', bg='#fefefe')  # Placeholder
    username_label.pack(anchor="w", padx=(10, 5), pady=(5, 0))

    global username_entry
    username_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    username_entry.pack(padx=(10, 5), pady=(0, 10))  # Space between label and entry

    # password input/label/enter to login

    password_label = tk.Label(form_frame, text="Password", fg='black', bg='#fefefe')  # Placeholder
    password_label.pack(anchor="w", padx=(10, 5))

    global password_entry
    password_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, show='*', highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')  # hide the user's password when they are typing
    password_entry.pack(padx=(10, 5), pady=(0, 10))  # Space between label and entry

    # pressing enter in the password entry box attempts to login (probably should change this to a button to be more consistent with the customers page)
    password_entry.bind("<Return>", lambda event: login())

    # Clickable label for creating an account
    create_account_label = tk.Label(form_frame, text="No account? Create one!", fg='blue', bg='#FFFFFF', cursor="hand2")
    create_account_label.pack(pady=(10, 0))
    create_account_label.bind("<Button-1>", show_create_account)  # clicking the create account text calls show_create_account

def login():
    email = username_entry.get()
    password = password_entry.get()
    if user_manager.check_password(email,password):
        clear_window()
        tk.Label(main_frame, text="Welcome!", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(expand=True) # centers the welcome message for now if login successful
    else: # resets the entry boxes if login fails
        show_home()



# Customer Functions
def show_create_account(event=None): # sets up the create account page with the entry boxes and labels
    clear_window()
    tk.Label(main_frame, text="Create Account", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # frame to put the account information entry boxes at the center of the screen
    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)  # centers the items

    # first name label and entry
    first_name_label = tk.Label(form_frame, text="First Name", fg='black', bg='#fefefe')
    first_name_label.pack(anchor="w", padx=(10, 5), pady=(5, 0))

    global first_name_entry
    first_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    first_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # last name label and entry
    last_name_label = tk.Label(form_frame, text="Last Name", fg='black', bg='#fefefe')
    last_name_label.pack(anchor="w", padx=(10, 5))

    global last_name_entry
    last_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    last_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # email/username label and entry
    email_label = tk.Label(form_frame, text="Email Address", fg='black', bg='#fefefe')
    email_label.pack(anchor="w", padx=(10, 5))

    global email_entry
    email_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    email_entry.pack(padx=(10, 5), pady=(0, 10))

    # password label and entry
    create_password_label = tk.Label(form_frame, text="Password", fg='black', bg='#fefefe')
    create_password_label.pack(anchor="w", padx=(10, 5))

    global create_password_entry
    create_password_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, show='*', highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    create_password_entry.pack(padx=(10, 5), pady=(0, 10))

    # pressing enter on the password line creates the account
    create_password_entry.bind("<Return>", lambda event: save_and_go_home())

def show_create_customer_form():
    clear_window()
    tk.Label(main_frame, text="Create New Customer", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # first name label and entry
    tk.Label(form_frame, text="First Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5), pady=(5, 0))
    first_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    first_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # last name label and entry
    tk.Label(form_frame, text="Last Name", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    last_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    last_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # email address label and entry
    tk.Label(form_frame, text="Email Address", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    email_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    email_entry.pack(padx=(10, 5), pady=(0, 10))

    # phone number label and entry
    tk.Label(form_frame, text="Phone Number", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    phone_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    phone_entry.pack(padx=(10, 5), pady=(0, 10))

    # address label and entry
    tk.Label(form_frame, text="Address", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    address_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    address_entry.pack(padx=(10, 5), pady=(0, 10))

    # save button
    save_btn = tk.Button(form_frame, text="Save", command=lambda: save_customer(
        first_name_entry.get(),
        last_name_entry.get(),
        email_entry.get(),
        phone_entry.get(),
        address_entry.get()))
    save_btn.pack(pady=10)

def edit_customer(customer):
    clear_window()
    tk.Label(main_frame, text="Edit Customer", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # frame to center the items
    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # first name label and entry
    tk.Label(form_frame, text="First Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5), pady=(5, 0))
    first_name_entry = tk.Entry(
        form_frame, font=('Arial', 12), bd=0,
        highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af'
    )
    first_name_entry.insert(0, customer.first_name)
    first_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # last name label and entry
    tk.Label(form_frame, text="Last Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    last_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    last_name_entry.insert(0, customer.last_name)
    last_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # email address label and entry
    tk.Label(form_frame, text="Email Address", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    email_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    email_entry.insert(0, customer.email)
    email_entry.pack(padx=(10, 5), pady=(0, 10))

    # phone number label and entry
    tk.Label(form_frame, text="Phone Number", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    phone_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    phone_entry.insert(0, customer.phone_number)
    phone_entry.pack(padx=(10, 5), pady=(0, 10))

    # address label and entry
    tk.Label(form_frame, text="Address", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    address_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    address_entry.insert(0, customer.address)
    address_entry.pack(padx=(10, 5), pady=(0, 10))

    # clickable label for updating the customer
    update_label = tk.Label(form_frame, text="Update Customer", fg='blue', bg='#FFFFFF', cursor="hand2",font=('Arial', 14, 'underline'))
    update_label.pack(pady=10)
    update_label.bind("<Button-1>", lambda event: update_customer(
        customer.id,
        first_name_entry.get(),
        last_name_entry.get(),
        email_entry.get(),
        phone_entry.get(),
        address_entry.get()
    ))

def show_customers():
    clear_window()
    reset_sidebar_buttons()
    customers_btn.config(bg='#1d81af')

    # header label
    tk.Label(main_frame, text="Customers", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # create new customer frame
    link_frame = tk.Frame(main_frame, bg="#FFFFFF")
    link_frame.pack(pady=(0, 20))

    # label to click and create a new customer
    create_customer_label = tk.Label(link_frame, text="Create New Customer", fg='blue', bg='#FFFFFF', cursor="hand2",font=('Arial', 14, 'underline'))
    create_customer_label.pack()
    create_customer_label.bind("<Button-1>", lambda event: show_create_customer_form())

    # frame to hold list of customers
    list_frame = tk.Frame(main_frame, bg="#FFFFFF")
    list_frame.pack(fill=tk.BOTH, expand=True)

    # each grid column expands the same amount
    for i in range(4):
        list_frame.columnconfigure(i, weight=1, uniform='column')

    # retrieves customers from the customers.db
    customer_service = CustomerService()
    customers = customer_service.get_all_customers()

    # customer page header labels
    headers = ["Full Name", "Email Address", "Phone Number", "Actions"]
    for idx, header in enumerate(headers):
        tk.Label(list_frame, text=header, font=('Arial', 16, 'bold'), bg="#FFFFFF").grid(row=0, column=idx, padx=10, pady=10, sticky='ew')

    # adds to customer list
    for idx, customer in enumerate(customers, start=1):
        full_name = f"{customer.first_name} {customer.last_name}"
        tk.Label(list_frame, text=full_name, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(row=idx, column=0, padx=10, pady=10, sticky='ew')
        tk.Label(list_frame, text=customer.email, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(row=idx, column=1, padx=10, pady=10, sticky='ew')
        tk.Label(list_frame, text=customer.phone_number, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(row=idx, column=2, padx=10, pady=10, sticky='ew')

        # view, edit, and delete buttons
        actions_frame = tk.Frame(list_frame, bg="#FFFFFF")
        actions_frame.grid(row=idx, column=3, padx=10, pady=10, sticky='ew')

        view_btn = tk.Button(actions_frame, text="View", font=('Arial', 12),
                             command=lambda c=customer: view_customer(c))
        view_btn.pack(side=tk.LEFT, padx=5, expand=True)

        edit_btn = tk.Button(actions_frame, text="Edit", font=('Arial', 12),
                             command=lambda c=customer: edit_customer(c))
        edit_btn.pack(side=tk.LEFT, padx=5, expand=True)

        delete_btn = tk.Button(actions_frame, text="Delete", font=('Arial', 12),
                               command=lambda c=customer: delete_customer(c))
        delete_btn.pack(side=tk.LEFT, padx=5, expand=True)

def save_customer(first_name, last_name, email, phone_number, address):
    customer_service = CustomerService()
    customer_service.create_customer(first_name, last_name, email, phone_number, address)
    show_customers()

def view_customer(customer):
    clear_window()
    tk.Label(main_frame, text="Customer Details", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg="#FFFFFF")
    details_frame.pack(expand=True, padx=20, pady=20)

    # display customer details with larger fonts
    fields = [
        ('First Name', customer.first_name),
        ('Last Name', customer.last_name),
        ('Email Address', customer.email),
        ('Phone Number', customer.phone_number),
        ('Address', customer.address)
    ]

    for label_text, value in fields:
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe', font=('Arial', 16, 'bold')).pack(anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe', font=('Arial', 14)).pack(anchor="w", pady=(0, 10))

    # back button
    back_btn = tk.Button(details_frame, text="Back", font=('Arial', 12), command=show_customers)
    back_btn.pack(pady=20)

def update_customer(customer_id, first_name, last_name, email, phone_number, address):
    customer_service = CustomerService()
    try:
        customer_service.update_customer(
            customer_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address
        )
        messagebox.showinfo("Success", "Customer updated successfully!")
        show_customers()
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))

def delete_customer(customer):
    result = tk.messagebox.askquestion("Delete Customer", f"Are you sure you want to delete {customer.first_name} {customer.last_name}?", icon='warning')
    if result == 'yes':
        customer_service = CustomerService()
        customer_service.soft_delete_customer(customer.id)
        show_customers()

def show_appointments():
    clear_window()
    reset_sidebar_buttons()
    appointments_btn.config(bg='#1d81af')

    tk.Label(main_frame, text="Appointments", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # button to add a new appointment
    add_new_label = tk.Label(main_frame, text="Add New Appointment", fg='blue', bg='#FFFFFF', cursor="hand2",
                             font=('Arial', 14, 'underline'))
    add_new_label.pack(pady=(0, 20))
    add_new_label.bind("<Button-1>", lambda event: show_create_appointment_form())

    # frame to hold the appointment list
    list_frame = tk.Frame(main_frame, bg="#FFFFFF")
    list_frame.pack(fill=tk.BOTH, expand=True)

    # configures grid columns
    for i in range(5):
        list_frame.columnconfigure(i, weight=1, uniform='column')

    # gets appointments
    appointment_service = AppointmentService()
    appointments = appointment_service.get_upcoming_appointments()

    # appointment page headers
    headers = ["Title", "Start Time", "End Time", "Location", "Actions"]
    for idx, header in enumerate(headers):
        tk.Label(list_frame, text=header, font=('Arial', 16, 'bold'), bg="#FFFFFF").grid(row=0, column=idx, padx=10, pady=10, sticky='ew')

    for idx, appointment in enumerate(appointments, start=1):
        # appointment title
        title_label = tk.Label(list_frame, text=appointment.title, font=('Arial', 14), fg='blue', bg="#FFFFFF", cursor="hand2")
        title_label.grid(row=idx, column=0, padx=10, pady=10, sticky='ew')
        title_label.bind("<Button-1>", lambda event, appt=appointment: view_appointment(appt))

        # start time
        tk.Label(list_frame, text=appointment.start_time.strftime('%Y-%m-%d %H:%M'), font=('Arial', 14), bg="#FFFFFF").grid(row=idx, column=1, padx=10, pady=10, sticky='ew')

        # end time
        tk.Label(list_frame, text=appointment.end_time.strftime('%Y-%m-%d %H:%M'), font=('Arial', 14), bg="#FFFFFF").grid(row=idx, column=2, padx=10, pady=10, sticky='ew')

        # location
        tk.Label(list_frame, text=appointment.location, font=('Arial', 14), bg="#FFFFFF").grid(row=idx, column=3, padx=10, pady=10, sticky='ew')

        # actions/buttons for appointments
        actions_frame = tk.Frame(list_frame, bg="#FFFFFF")
        actions_frame.grid(row=idx, column=4, padx=10, pady=10, sticky='ew')

        view_btn = tk.Button(actions_frame, text="View", font=('Arial', 12), command=lambda appt=appointment: view_appointment(appt))
        view_btn.pack(side=tk.LEFT, padx=5, expand=True)

        edit_btn = tk.Button(actions_frame, text="Edit", font=('Arial', 12), command=lambda appt=appointment: edit_appointment(appt))
        edit_btn.pack(side=tk.LEFT, padx=5, expand=True)

        delete_btn = tk.Button(actions_frame, text="Delete", font=('Arial', 12), command=lambda appt=appointment: delete_appointment(appt))
        delete_btn.pack(side=tk.LEFT, padx=5, expand=True)

def show_create_appointment_form():
    clear_window()
    tk.Label(main_frame, text="New Appointment", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)
    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # appointment title
    tk.Label(form_frame, text="Title", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5), pady=(5, 0))
    title_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    title_entry.pack(padx=(10, 5), pady=(0, 10))

    # appointment description
    tk.Label(form_frame, text="Description", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    description_entry = tk.Text(form_frame, font=('Arial', 12), bd=0, height=5, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    description_entry.pack(padx=(10, 5), pady=(0, 10))

    # start of appointment
    tk.Label(form_frame, text="Start Time (YYYY-MM-DD HH:MM:SS)", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    start_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    start_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # end of appointment
    tk.Label(form_frame, text="End Time (YYYY-MM-DD HH:MM:SS)", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    end_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    end_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # location
    tk.Label(form_frame, text="Location", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    location_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    location_entry.pack(padx=(10, 5), pady=(0, 10))

    # select customer
    tk.Label(form_frame, text="Customer", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))

    customer_service = CustomerService()
    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()

    if customer_options:
        selected_customer.set(customer_options[0])  # Set default value
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
    else:
        # no customers to choose from
        customer_options = ['No Customers Available']
        selected_customer.set(customer_options[0])
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.config(state='disabled')  # removes the dropdown menu

    customer_dropdown.pack(padx=(10, 5), pady=(0, 10))

    # save button/clickable label
    save_label = tk.Label(form_frame, text="Save Appointment", fg='blue', bg='#FFFFFF', cursor="hand2", font=('Arial', 14, 'underline'))
    save_label.pack(pady=10)
    save_label.bind("<Button-1>", lambda event: save_appointment(
        selected_customer.get(),
        title_entry.get(),
        description_entry.get("1.0", tk.END),
        start_time_entry.get(),
        end_time_entry.get(),
        location_entry.get()
    ))

def save_appointment(selected_customer, title, description, start_time, end_time, location):
    if not selected_customer:
        messagebox.showerror("Error", "Please select a customer.")
        return

    customer_id = int(selected_customer.split(":")[0])  # Extract customer ID

    appointment_service = AppointmentService()
    try:
        appointment_service.create_appointment(
            customer_id=customer_id,
            title=title,
            description=description.strip(),
            start_time=start_time,
            end_time=end_time,
            location=location
        )
        messagebox.showinfo("Success", "Appointment created successfully!")
        show_appointments()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_appointment(appointment):
    clear_window()
    tk.Label(main_frame, text="Appointment Details", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg="#FFFFFF")
    details_frame.pack(expand=True, padx=20, pady=20)

    # appointment's details
    fields = [
        ('Title', appointment.title),
        ('Description', appointment.description),
        ('Start Time', appointment.start_time.strftime('%Y-%m-%d %H:%M')),
        ('End Time', appointment.end_time.strftime('%Y-%m-%d %H:%M')),
        ('Location', appointment.location)
    ]

    for label_text, value in fields:
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe', font=('Arial', 16, 'bold')).pack(anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe', font=('Arial', 14)).pack(anchor="w", pady=(0, 10))

    # customer details
    customer_service = CustomerService()
    customer = customer_service.get_customer_by_id(appointment.customer_id)
    tk.Label(details_frame, text="Customer:", fg='black', bg='#fefefe', font=('Arial', 16, 'bold')).pack(anchor="w", pady=(20, 0))
    customer_fields = [
        ('Name', f"{customer.first_name} {customer.last_name}"),
        ('Phone', customer.phone_number),
        ('Email', customer.email),
        ('Address', customer.address)
    ]

    for label_text, value in customer_fields:
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe', font=('Arial', 14, 'bold')).pack(anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe', font=('Arial', 12)).pack(anchor="w", pady=(0, 10))

    # back button
    back_btn = tk.Button(details_frame, text="Back", font=('Arial', 12), command=show_appointments)
    back_btn.pack(pady=20)


def edit_appointment(appointment):
    clear_window()
    tk.Label(main_frame, text="Edit Appointment", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # appointment title
    tk.Label(form_frame, text="Title", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5), pady=(5, 0))
    title_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                           highlightbackground='#156082', highlightcolor='#1d81af')
    title_entry.insert(0, appointment.title)
    title_entry.pack(padx=(10, 5), pady=(0, 10))

    # appointment description
    tk.Label(form_frame, text="Description", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    description_entry = tk.Text(form_frame, font=('Arial', 12), bd=0, height=5, highlightthickness=2,
                                highlightbackground='#156082', highlightcolor='#1d81af')
    description_entry.insert("1.0", appointment.description)
    description_entry.pack(padx=(10, 5), pady=(0, 10))

    # starting time
    tk.Label(form_frame, text="Start Time (YYYY-MM-DD HH:MM:SS)", fg='black', bg='#fefefe').pack(anchor="w",
                                                                                                 padx=(10, 5))
    start_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                                highlightbackground='#156082', highlightcolor='#1d81af')
    start_time_entry.insert(0, appointment.start_time.strftime('%Y-%m-%d %H:%M:%S'))
    start_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # ending time
    tk.Label(form_frame, text="End Time (YYYY-MM-DD HH:MM:SS)", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    end_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                              highlightbackground='#156082', highlightcolor='#1d81af')
    end_time_entry.insert(0, appointment.end_time.strftime('%Y-%m-%d %H:%M:%S'))
    end_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # location
    tk.Label(form_frame, text="Location", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    location_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                              highlightbackground='#156082', highlightcolor='#1d81af')
    location_entry.insert(0, appointment.location)
    location_entry.pack(padx=(10, 5), pady=(0, 10))

    # select customer
    tk.Label(form_frame, text="Customer", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    customer_service = CustomerService()
    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()

    if customer_options:
        # customer index
        current_customer_option = f"{appointment.customer_id}: {customer_service.get_customer_by_id(appointment.customer_id).first_name} {customer_service.get_customer_by_id(appointment.customer_id).last_name}"
        selected_customer.set(current_customer_option)
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.pack(padx=(10, 5), pady=(0, 10))
    else:
        # there are no customers
        tk.Label(form_frame, text="No customers available. Please add a customer first.", fg='red', bg='#FFFFFF').pack()
        return

    # save button/label to click
    save_label = tk.Label(form_frame, text="Update Appointment", fg='blue', bg='#FFFFFF', cursor="hand2",
                          font=('Arial', 14, 'underline'))
    save_label.pack(pady=10)
    save_label.bind("<Button-1>", lambda event: update_appointment(
        appointment.id,
        selected_customer.get(),
        title_entry.get(),
        description_entry.get("1.0", tk.END),
        start_time_entry.get(),
        end_time_entry.get(),
        location_entry.get()
    ))

def update_appointment(appointment_id, selected_customer, title, description, start_time, end_time, location):
    if not selected_customer:
        messagebox.showerror("Error", "Please select a customer.")
        return

    customer_id = int(selected_customer.split(":")[0])  # gets the customer id

    appointment_service = AppointmentService()
    try:
        appointment_service.update_appointment(
            appointment_id,
            customer_id=customer_id,
            title=title,
            description=description.strip(),
            start_time=start_time,
            end_time=end_time,
            location=location
        )
        messagebox.showinfo("Success", "Appointment updated successfully!")
        show_appointments()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_appointment(appointment):
    result = messagebox.askquestion("Delete Appointment", f"Are you sure you want to delete '{appointment.title}'?", icon='warning')
    if result == 'yes':
        appointment_service = AppointmentService()
        appointment_service.soft_delete_appointment(appointment.id)
        messagebox.showinfo("Deleted", "Appointment deleted successfully.")
        show_appointments()

# General functions
def reset_sidebar_buttons():
    # UPDATE EACH TIME ANOTHER PAGE IS ADDED!!!!!!!!!
    home_btn.config(bg='#156082')
    customers_btn.config(bg='#156082')
    appointments_btn.config(bg='#156082')

def save_and_go_home():
    # retrieves the information entered in each of the entry boxes
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = create_password_entry.get()

    if first_name and last_name and email and password:
        user_manager.create_user(first_name, last_name, email, password)
        show_home() #returns home after creating the new user

def clear_window(): # clears window
    for widget in main_frame.winfo_children():
        widget.destroy()

# makes default page
create_sidebar()
main_frame = tk.Frame(home, bg="#fefefe", bd=2, relief='solid')
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
show_home()
home.mainloop()
