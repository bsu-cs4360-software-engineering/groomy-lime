import tkinter as tk
import tkinter.messagebox as messagebox
from user_manager import UserManager
from customer_service import CustomerService
from appointment_service import AppointmentService
import sqlite3
from datetime import datetime
from notes_service import NotesService
from services_service import ServicesService
from invoice_service import InvoiceService
from invoice_setup import setup_invoice_tables


logged_in = False
sidebar = None
customers_btn = None
appointments_btn = None
services_btn = None


# SHARED database
conn = sqlite3.connect('app.db')
conn.row_factory = sqlite3.Row  # returns the rows as dictionaries
conn.execute('PRAGMA foreign_keys = ON')  # foreign keys supported
customer_service = CustomerService(conn)
appointment_service = AppointmentService(conn)
notes_service = NotesService(conn)
services_service = ServicesService(conn)
invoice_service = InvoiceService(conn)
setup_invoice_tables(conn)

# main window creation
home = tk.Tk()
home.geometry("1600x900")
home.title("Groomy") # title of the screen

# creates the UserManager instance
user_manager = UserManager('users.db')

def create_sidebar():
    global home_btn, customers_btn, appointments_btn, services_btn, sidebar, logged_in, invoices_btn

    # removes the sidebar
    if sidebar:
        sidebar.destroy()

    # recreates the sidebar
    sidebar = tk.Frame(home, bg='#156082', width=225, bd=2, relief='solid')
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    # create sidebar buttons for each window
    home_btn = tk.Button(sidebar, text="HOME", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_home)
    home_btn.pack(pady=(100,10))

    # these are created only if the user is logged in
    if logged_in:
        customers_btn = tk.Button(sidebar, text="CUSTOMERS", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_customers)
        customers_btn.pack(pady=10)

        appointments_btn = tk.Button(sidebar, text="APPOINTMENTS", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_appointments)
        appointments_btn.pack(pady=10)

        services_btn = tk.Button(sidebar, text="SERVICES", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_services)
        services_btn.pack(pady=10)

        invoices_btn = tk.Button(sidebar, text="INVOICES", font=('Arial', 15), fg='#ffffff', bg='#156082', bd=0, height=2, width=20, command=show_invoices)
        invoices_btn.pack(pady=10)

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
        global logged_in
        logged_in = True
        create_sidebar()
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

def show_create_appointment_form():
    global customer_service
    clear_window()
    tk.Label(main_frame, text="New Appointment", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)
    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # appointment title
    tk.Label(form_frame, text="Title", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5),
                                                                      pady=(5, 0))
    title_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                           highlightbackground='#156082', highlightcolor='#1d81af')
    title_entry.pack(padx=(10, 5), pady=(0, 10))

    # appointment description
    tk.Label(form_frame, text="Description", fg='black', bg='#fefefe').pack(anchor="w",
                                                                            padx=(10, 5))
    description_entry = tk.Text(form_frame, font=('Arial', 12), bd=0, height=5,
                                highlightthickness=2, highlightbackground='#156082',
                                highlightcolor='#1d81af')
    description_entry.pack(padx=(10, 5), pady=(0, 10))

    # start of appointment
    tk.Label(form_frame, text="Start Time (YYYY-MM-DD HH:MM:SS)", fg='black',
             bg='#fefefe').pack(anchor="w", padx=(10, 5))
    start_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                                highlightthickness=2, highlightbackground='#156082',
                                highlightcolor='#1d81af')
    start_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # end of appointment
    tk.Label(form_frame, text="End Time (YYYY-MM-DD HH:MM:SS)", fg='black',
             bg='#fefefe').pack(anchor="w", padx=(10, 5))
    end_time_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                              highlightthickness=2, highlightbackground='#156082',
                              highlightcolor='#1d81af')
    end_time_entry.pack(padx=(10, 5), pady=(0, 10))

    # location
    tk.Label(form_frame, text="Location", fg='black', bg='#fefefe').pack(anchor="w",
                                                                         padx=(10, 5))
    location_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0, highlightthickness=2,
                              highlightbackground='#156082', highlightcolor='#1d81af')
    location_entry.pack(padx=(10, 5), pady=(0, 10))

    # select customer
    tk.Label(form_frame, text="Customer", fg='black', bg='#fefefe').pack(anchor="w",
                                                                         padx=(10, 5))

    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()

    if customer_options:
        selected_customer.set(customer_options[0])  # Set default value
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.pack(padx=(10, 5), pady=(0, 10))
    else:
        # no customers to choose from
        tk.Label(form_frame, text="No Customers Available", fg='red',
                 bg='#FFFFFF').pack()
        return

    # save button
    save_label = tk.Label(form_frame, text="Save Appointment", fg='blue', bg='#FFFFFF',
                          cursor="hand2", font=('Arial', 14, 'underline'))
    save_label.pack(pady=10)
    save_label.bind("<Button-1>", lambda event: save_appointment(
        selected_customer.get(),
        title_entry.get(),
        description_entry.get("1.0", tk.END),
        start_time_entry.get(),
        end_time_entry.get(),
        location_entry.get()
    ))


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
    global customer_service
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
    global customer_service
    customer_service.create_customer(first_name, last_name, email, phone_number, address)
    show_customers()

def view_customer(customer):
    clear_window()
    tk.Label(main_frame, text="Customer Details", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg="#FFFFFF")
    details_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # customer details
    fields = [
        ('First Name', customer.first_name),
        ('Last Name', customer.last_name),
        ('Email Address', customer.email),
        ('Phone Number', customer.phone_number),
        ('Address', customer.address)
    ]

    for label_text, value in fields:
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe',
                 font=('Arial', 16, 'bold')).pack(anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe',
                 font=('Arial', 14)).pack(anchor="w", pady=(0, 10))

    # notes section
    tk.Label(details_frame, text="Notes:", fg='black', bg='#fefefe',
             font=('Arial', 16, 'bold')).pack(anchor="w", pady=(20, 0))

    notes = notes_service.get_notes_for_customer(customer.id)

    # add new note button
    add_note_btn = tk.Button(details_frame, text="Add New Note",
                             command=lambda: add_note_to_customer(customer))
    add_note_btn.pack(anchor="w", pady=(10, 10))

    if notes:
        for note in notes:
            note_frame = tk.Frame(details_frame, bg="#fefefe", bd=1, relief=tk.RIDGE)
            note_frame.pack(fill=tk.X, pady=(0, 10))

            title_label = tk.Label(note_frame, text=note.title, fg='blue', bg='#fefefe',
                                   cursor="hand2", font=('Arial', 14, 'underline'))
            title_label.pack(anchor="w", padx=10, pady=5)
            title_label.bind("<Button-1>", lambda event, n=note: view_note_popup(n))

            snippet = (note.content[:100] + '...') if len(note.content) > 100 else note.content
            tk.Label(note_frame, text=snippet, fg='black', bg='#fefefe',
                     font=('Arial', 12)).pack(anchor="w", padx=10)

            date_label = tk.Label(note_frame, text=note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  fg='gray', bg='#fefefe', font=('Arial', 10))
            date_label.pack(anchor="e", padx=10, pady=5)

            # note actions
            actions_frame = tk.Frame(note_frame, bg="#fefefe")
            actions_frame.pack(anchor="e", padx=10, pady=5)

            edit_btn = tk.Button(actions_frame, text="Edit",
                                 command=lambda n=note: edit_note_for_customer(customer, n))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(actions_frame, text="Delete",
                                   command=lambda n=note: delete_note_for_customer(customer, n))
            delete_btn.pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(details_frame, text="No notes available.", fg='gray', bg='#fefefe',
                 font=('Arial', 12)).pack(anchor="w", pady=(10, 0))

    # back button
    back_btn = tk.Button(details_frame, text="Back", font=('Arial', 12), command=show_customers)
    back_btn.pack(pady=20)

def update_customer(customer_id, first_name, last_name, email, phone_number, address):
    global customer_service
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
    global customer_service
    result = tk.messagebox.askquestion("Delete Customer", f"Are you sure you want to delete {customer.first_name} {customer.last_name}?", icon='warning')
    if result == 'yes':
        customer_service.soft_delete_customer(customer.id)
        show_customers()

def add_note_to_customer(customer):
    def save_note():
        title = title_entry.get()
        content = content_text.get("1.0", tk.END).strip()
        if title and content:
            notes_service.create_note_for_customer(customer.id, title, content)
            note_window.destroy()
            view_customer(customer)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Add Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Save", command=save_note)
    save_btn.pack(pady=10)

def edit_note_for_customer(customer, note):
    def update_note():
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        if new_title and new_content:
            notes_service.update_note(note.id, new_title, new_content)
            note_window.destroy()
            view_customer(customer)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Edit Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.insert(0, note.title)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.insert(tk.END, note.content)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Update", command=update_note)
    save_btn.pack(pady=10)

def delete_note_for_customer(customer, note):
    result = messagebox.askquestion("Delete Note",
                                    f"Are you sure you want to delete '{note.title}'?",
                                    icon='warning')
    if result == 'yes':
        notes_service.delete_note_for_customer(customer.id, note.id)
        view_customer(customer)

def view_note_popup(note):
    note_window = tk.Toplevel(home)
    note_window.title(note.title)
    note_window.geometry("400x300")

    tk.Label(note_window, text=note.title, font=('Arial', 16, 'bold')).pack(pady=(10, 0))
    tk.Label(note_window, text=note.created_at.strftime('%Y-%m-%d %H:%M:%S'), fg='gray',
             font=('Arial', 10)).pack()

    content_text = tk.Text(note_window, width=50, height=10)
    content_text.insert(tk.END, note.content)
    content_text.configure(state='disabled')
    content_text.pack(pady=10)

def show_appointments():
    global appointment_service
    clear_window()
    reset_sidebar_buttons()
    appointments_btn.config(bg='#1d81af')

    tk.Label(main_frame, text="Appointments", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # button to add a new appointment
    add_new_label = tk.Label(main_frame, text="Add New Appointment", fg='blue', bg='#FFFFFF',
                             cursor="hand2", font=('Arial', 14, 'underline'))
    add_new_label.pack(pady=(0, 20))
    add_new_label.bind("<Button-1>", lambda event: show_create_appointment_form())

    # frame to hold the appointment list
    list_frame = tk.Frame(main_frame, bg="#FFFFFF")
    list_frame.pack(fill=tk.BOTH, expand=True)

    # configures grid columns
    for i in range(5):
        list_frame.columnconfigure(i, weight=1, uniform='column')

    # gets appointments
    appointments = appointment_service.get_upcoming_appointments()

    # appointment page headers
    headers = ["Title", "Start Time", "End Time", "Location", "Actions"]
    for idx, header in enumerate(headers):
        tk.Label(list_frame, text=header, font=('Arial', 16, 'bold'), bg="#FFFFFF").grid(
            row=0, column=idx, padx=10, pady=10, sticky='ew')

    for idx, appointment in enumerate(appointments, start=1):
        # appointment title
        title_label = tk.Label(list_frame, text=appointment.title, font=('Arial', 14),
                               fg='blue', bg="#FFFFFF", cursor="hand2")
        title_label.grid(row=idx, column=0, padx=10, pady=10, sticky='ew')
        title_label.bind("<Button-1>", lambda event, appt=appointment: view_appointment(appt))

        # start time
        tk.Label(list_frame, text=appointment.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                 font=('Arial', 14), bg="#FFFFFF").grid(row=idx, column=1, padx=10,
                                                        pady=10, sticky='ew')

        # end time
        tk.Label(list_frame, text=appointment.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                 font=('Arial', 14), bg="#FFFFFF").grid(row=idx, column=2, padx=10,
                                                        pady=10, sticky='ew')

        # location
        tk.Label(list_frame, text=appointment.location, font=('Arial', 14),
                 bg="#FFFFFF").grid(row=idx, column=3, padx=10, pady=10, sticky='ew')

        # actions/buttons for appointments
        actions_frame = tk.Frame(list_frame, bg="#FFFFFF")
        actions_frame.grid(row=idx, column=4, padx=10, pady=10, sticky='ew')

        view_btn = tk.Button(actions_frame, text="View", font=('Arial', 12),
                             command=lambda appt=appointment: view_appointment(appt))
        view_btn.pack(side=tk.LEFT, padx=5, expand=True)

        edit_btn = tk.Button(actions_frame, text="Edit", font=('Arial', 12),
                             command=lambda appt=appointment: edit_appointment(appt))
        edit_btn.pack(side=tk.LEFT, padx=5, expand=True)

        delete_btn = tk.Button(actions_frame, text="Delete", font=('Arial', 12),
                               command=lambda appt=appointment: delete_appointment(appt))
        delete_btn.pack(side=tk.LEFT, padx=5, expand=True)


def view_appointment(appointment):
    clear_window()
    tk.Label(main_frame, text="Appointment Details", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg="#FFFFFF")
    details_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # configure grid columns in details_frame
    details_frame.columnconfigure(0, weight=1, uniform='column')
    details_frame.columnconfigure(1, weight=1, uniform='column')

    # appointment details frame
    appointment_frame = tk.Frame(details_frame, bg="#FFFFFF")
    appointment_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

    # customer details frame
    customer_frame = tk.Frame(details_frame, bg="#FFFFFF")
    customer_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

    # appointment details
    tk.Label(appointment_frame, text="Appointment Details", fg='black', bg='#fefefe',
             font=('Arial', 18, 'bold')).pack(anchor="w", pady=(0, 10))

    appointment_fields = [
        ('Title', appointment.title),
        ('Description', appointment.description),
        ('Start Time', appointment.start_time.strftime('%Y-%m-%d %H:%M:%S')),
        ('End Time', appointment.end_time.strftime('%Y-%m-%d %H:%M:%S')),
        ('Location', appointment.location)
    ]

    for label_text, value in appointment_fields:
        tk.Label(appointment_frame, text=label_text + ":", fg='black', bg='#fefefe',
                 font=('Arial', 14, 'bold')).pack(anchor="w", pady=(5, 0))
        tk.Label(appointment_frame, text=value, fg='black', bg='#fefefe',
                 font=('Arial', 12), wraplength=400, justify=tk.LEFT).pack(anchor="w", pady=(0, 10))

    # Customer details
    customer = customer_service.get_customer_by_id(appointment.customer_id)
    tk.Label(customer_frame, text="Customer Details", fg='black', bg='#fefefe',
             font=('Arial', 18, 'bold')).pack(anchor="w", pady=(0, 10))

    customer_fields = [
        ('Name', f"{customer.first_name} {customer.last_name}"),
        ('Phone', customer.phone_number),
        ('Email', customer.email),
        ('Address', customer.address)
    ]

    for label_text, value in customer_fields:
        tk.Label(customer_frame, text=label_text + ":", fg='black', bg='#fefefe',
                 font=('Arial', 14, 'bold')).pack(anchor="w", pady=(5, 0))
        tk.Label(customer_frame, text=value, fg='black', bg='#fefefe',
                 font=('Arial', 12), wraplength=400, justify=tk.LEFT).pack(anchor="w", pady=(0, 10))

    # Notes section
    tk.Label(main_frame, text="Notes:", fg='black', bg='#fefefe',
             font=('Arial', 16, 'bold')).pack(anchor="w", padx=20, pady=(10, 0))

    notes = notes_service.get_notes_for_appointment(appointment.id)

    # Add new note button
    add_note_btn = tk.Button(main_frame, text="Add New Note",
                             command=lambda: add_note_to_appointment(appointment))
    add_note_btn.pack(anchor="w", padx=20, pady=(10, 10))

    if notes:
        for note in notes:
            note_frame = tk.Frame(main_frame, bg="#fefefe", bd=1, relief=tk.RIDGE)
            note_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

            title_label = tk.Label(note_frame, text=note.title, fg='blue', bg='#fefefe',
                                   cursor="hand2", font=('Arial', 14, 'underline'))
            title_label.pack(anchor="w", padx=10, pady=5)
            title_label.bind("<Button-1>", lambda event, n=note: view_note_popup(n))

            snippet = (note.content[:100] + '...') if len(note.content) > 100 else note.content
            tk.Label(note_frame, text=snippet, fg='black', bg='#fefefe',
                     font=('Arial', 12), wraplength=800, justify=tk.LEFT).pack(anchor="w", padx=10)

            date_label = tk.Label(note_frame, text=note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  fg='gray', bg='#fefefe', font=('Arial', 10))
            date_label.pack(anchor="e", padx=10, pady=5)

            # Note actions
            actions_frame = tk.Frame(note_frame, bg="#fefefe")
            actions_frame.pack(anchor="e", padx=10, pady=5)

            edit_btn = tk.Button(actions_frame, text="Edit",
                                 command=lambda n=note: edit_note_for_appointment(appointment, n))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(actions_frame, text="Delete",
                                   command=lambda n=note: delete_note_for_appointment(appointment, n))


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
    tk.Label(form_frame, text="End Time (YYYY-MM-DD HH:MM:SS)", fg='black', bg='#fefefe').pack(anchor="w",
                                                                                                padx=(10, 5))
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
    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()

    if customer_options:
        # set the current customer as the default
        current_customer_option = f"{appointment.customer_id}: {customer_service.get_customer_by_id(appointment.customer_id).first_name} {customer_service.get_customer_by_id(appointment.customer_id).last_name}"
        selected_customer.set(current_customer_option)
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.pack(padx=(10, 5), pady=(0, 10))
    else:
        tk.Label(form_frame, text="No customers available. Please add a customer first.", fg='red',
                 bg='#FFFFFF').pack()
        return

    # save button
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

def add_note_to_appointment(appointment):
    def save_note():
        title = title_entry.get()
        content = content_text.get("1.0", tk.END).strip()
        if title and content:
            notes_service.create_note_for_appointment(appointment.id, title, content)
            note_window.destroy()
            view_appointment(appointment)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Add Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Save", command=save_note)
    save_btn.pack(pady=10)

def edit_note_for_appointment(appointment, note):
    def update_note():
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        if new_title and new_content:
            notes_service.update_note(note.id, new_title, new_content)
            note_window.destroy()
            view_appointment(appointment)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Edit Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.insert(0, note.title)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.insert(tk.END, note.content)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Update", command=update_note)
    save_btn.pack(pady=10)

def delete_note_for_appointment(appointment, note):
    result = messagebox.askquestion("Delete Note",
                                    f"Are you sure you want to delete '{note.title}'?",
                                    icon='warning')
    if result == 'yes':
        notes_service.delete_note_for_appointment(appointment.id, note.id)
        view_appointment(appointment)

def update_appointment(appointment_id, selected_customer, title, description, start_time, end_time, location):
    global appointment_service
    if not selected_customer:
        messagebox.showerror("Error", "Please select a customer.")
        return

    customer_id = int(selected_customer.split(":")[0])  # Gets the customer ID

    try:
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        if end_time_obj <= start_time_obj:
            messagebox.showerror("Error", "End time must be after start time.")
            return

        # converts back to strings
        start_time_formatted = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        end_time_formatted = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

        appointment_service.update_appointment(
            appointment_id,
            customer_id=customer_id,
            title=title,
            description=description.strip(),
            start_time=start_time_formatted,
            end_time=end_time_formatted,
            location=location
        )
        messagebox.showinfo("Success", "Appointment updated successfully!")
        show_appointments()
    except ValueError as ve:
        messagebox.showerror("Error", f"Invalid date/time format: {ve}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_appointment(selected_customer, title, description, start_time, end_time, location):
    global appointment_service
    if not selected_customer:
        messagebox.showerror("Error", "Please select a customer.")
        return

    customer_id = int(selected_customer.split(":")[0])  # extract customer ID

    try:
        # ensures start and end time make sense
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        if end_time_obj <= start_time_obj:
            messagebox.showerror("Error", "End time must be after start time.")
            return

        # converts date and time back to the correct format
        start_time_formatted = start_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        end_time_formatted = end_time_obj.strftime('%Y-%m-%d %H:%M:%S')

        appointment_service.create_appointment(
            customer_id=customer_id,
            title=title,
            description=description.strip(),
            start_time=start_time_formatted,
            end_time=end_time_formatted,
            location=location
        )
        messagebox.showinfo("Success", "Appointment created successfully!")
        show_appointments()
    except ValueError as ve:
        messagebox.showerror("Error", f"Invalid date/time format: {ve}")
    except Exception as e:
        print(f"Error creating appointment: {e}")
        messagebox.showerror("Error", str(e))

def delete_appointment(appointment):
    global appointment_service
    result = messagebox.askquestion("Delete Appointment", f"Are you sure you want to delete '{appointment.title}'?", icon='warning')
    if result == 'yes':
        appointment_service.soft_delete_appointment(appointment.id)
        messagebox.showinfo("Deleted", "Appointment deleted successfully.")
        show_appointments()

# services
def show_services():
    clear_window()
    reset_sidebar_buttons()
    services_btn.config(bg='#1d81af')

    # add header label to main_frame
    tk.Label(main_frame, text="Services", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

    # clickable label to add a new service
    add_new_service_label = tk.Label(main_frame, text="Add New Service", fg='blue', bg='#FFFFFF',
                                     cursor="hand2", font=('Arial', 14, 'underline'))
    add_new_service_label.pack(pady=(0, 20))
    add_new_service_label.bind("<Button-1>", lambda event: show_create_service_form())

    # frame to hold the list of services
    list_frame = tk.Frame(main_frame, bg="#FFFFFF")
    list_frame.pack(fill=tk.BOTH, expand=True)

    # configure grid columns
    for i in range(4):
        list_frame.columnconfigure(i, weight=1, uniform='column')

    # get services
    services = services_service.get_all_services()

    # services page headers
    headers = ["Name", "Description", "Price", "Actions"]
    for idx, header in enumerate(headers):
        tk.Label(list_frame, text=header, font=('Arial', 16, 'bold'), bg="#FFFFFF").grid(
            row=0, column=idx, padx=10, pady=10, sticky='ew')

    # lists services
    for idx, service in enumerate(services, start=1):
        # name
        name_label = tk.Label(list_frame, text=service.name, font=('Arial', 14), fg='blue', bg="#FFFFFF", cursor="hand2")
        name_label.grid(row=idx, column=0, padx=10, pady=10, sticky='ew')
        name_label.bind("<Button-1>", lambda event, svc=service: view_service(svc))

        # description (max 100 characters)
        description = (service.description[:100] + '...') if len(service.description) > 100 else service.description
        tk.Label(list_frame, text=description, font=('Arial', 14), bg="#FFFFFF", anchor='w').grid(
            row=idx, column=1, padx=10, pady=10, sticky='ew')

        # price
        tk.Label(list_frame, text=f"${service.price:.2f}", font=('Arial', 14), bg="#FFFFFF").grid(
            row=idx, column=2, padx=10, pady=10, sticky='ew')

        # actions
        actions_frame = tk.Frame(list_frame, bg="#FFFFFF")
        actions_frame.grid(row=idx, column=3, padx=10, pady=10, sticky='ew')

        view_btn = tk.Button(actions_frame, text="View", font=('Arial', 12),
                             command=lambda svc=service: view_service(svc))
        view_btn.pack(side=tk.LEFT, padx=5, expand=True)

        edit_btn = tk.Button(actions_frame, text="Edit", font=('Arial', 12),
                             command=lambda svc=service: edit_service(svc))
        edit_btn.pack(side=tk.LEFT, padx=5, expand=True)

        delete_btn = tk.Button(actions_frame, text="Delete", font=('Arial', 12),
                               command=lambda svc=service: delete_service(svc))
        delete_btn.pack(side=tk.LEFT, padx=5, expand=True)


def show_create_service_form():
    clear_window()

    # add header label to main_frame
    tk.Label(main_frame, text="New Service", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # create a container frame to center the form
    container_frame = tk.Frame(main_frame, bg="#FFFFFF")
    container_frame.pack(expand=True)

    # create form_frame inside container_frame
    form_frame = tk.Frame(container_frame, bg="#FFFFFF")
    form_frame.pack()

    # name
    tk.Label(form_frame, text="Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5), pady=(5, 0))
    name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                          highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    name_entry.pack(padx=(10, 5), pady=(0, 10))

    # description
    tk.Label(form_frame, text="Description", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    description_entry = tk.Text(form_frame, font=('Arial', 12), bd=0, height=5,
                                highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    description_entry.pack(padx=(10, 5), pady=(0, 10))

    # price
    tk.Label(form_frame, text="Price", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    price_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                           highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    price_entry.pack(padx=(10, 5), pady=(0, 10))

    # save button
    save_btn = tk.Button(form_frame, text="Save", command=lambda: save_service(
        name_entry.get(),
        description_entry.get("1.0", tk.END).strip(),
        price_entry.get()
    ))
    save_btn.pack(pady=10)



# general functions
def reset_sidebar_buttons():
    home_btn.config(bg='#156082')
    if logged_in:
        customers_btn.config(bg='#156082')
        appointments_btn.config(bg='#156082')
        services_btn.config(bg='#156082')
        invoices_btn.config(bg='#156082')

def save_and_go_home():
    # retrieves the information entered in each of the entry boxes
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    password = create_password_entry.get()

    if first_name and last_name and email and password:
        user_manager.create_user(first_name, last_name, email, password)
        show_home()  # returns home after creating the new user

def clear_window():  # clears window
    for widget in main_frame.winfo_children():
        widget.destroy()

def save_service(name, description, price):
    try:
        price = float(price)
        services_service.create_service(name, description, price)
        messagebox.showinfo("Success", "Service created successfully!")
        show_services()
    except ValueError:
        messagebox.showerror("Error", "Invalid price. Please enter a valid number.")

def view_service(service):
    clear_window()
    # Clear main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Add header label
    tk.Label(main_frame, text="Service Details", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg="#FFFFFF")
    details_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Service details
    fields = [
        ('Name', service.name),
        ('Description', service.description),
        ('Price', f"${service.price:.2f}")
    ]

    for label_text, value in fields:
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe',
                 font=('Arial', 16, 'bold')).pack(anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe',
                 font=('Arial', 14), wraplength=800, justify=tk.LEFT).pack(anchor="w", pady=(0, 10))

    # Notes section
    tk.Label(details_frame, text="Notes:", fg='black', bg='#fefefe',
             font=('Arial', 16, 'bold')).pack(anchor="w", pady=(20, 0))

    notes = notes_service.get_notes_for_service(service.id)

    # Add new note button
    add_note_btn = tk.Button(details_frame, text="Add New Note",
                             command=lambda: add_note_to_service(service))
    add_note_btn.pack(anchor="w", pady=(10, 10))

    if notes:
        for note in notes:
            note_frame = tk.Frame(details_frame, bg="#fefefe", bd=1, relief=tk.RIDGE)
            note_frame.pack(fill=tk.X, pady=(0, 10))

            title_label = tk.Label(note_frame, text=note.title, fg='blue', bg='#fefefe',
                                   cursor="hand2", font=('Arial', 14, 'underline'))
            title_label.pack(anchor="w", padx=10, pady=5)
            title_label.bind("<Button-1>", lambda event, n=note: view_note_popup(n))

            snippet = (note.content[:100] + '...') if len(note.content) > 100 else note.content
            tk.Label(note_frame, text=snippet, fg='black', bg='#fefefe',
                     font=('Arial', 12)).pack(anchor="w", padx=10)

            date_label = tk.Label(note_frame, text=note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                  fg='gray', bg='#fefefe', font=('Arial', 10))
            date_label.pack(anchor="e", padx=10, pady=5)

            # Note actions
            actions_frame = tk.Frame(note_frame, bg="#fefefe")
            actions_frame.pack(anchor="e", padx=10, pady=5)

            edit_btn = tk.Button(actions_frame, text="Edit",
                                 command=lambda n=note: edit_note_for_service(service, n))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(actions_frame, text="Delete",
                                   command=lambda n=note: delete_note_for_service(service, n))
            delete_btn.pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(details_frame, text="No notes available.", fg='gray', bg='#fefefe',
                 font=('Arial', 12)).pack(anchor="w", pady=(10, 0))

    # Back button
    back_btn = tk.Button(details_frame, text="Back", font=('Arial', 12), command=show_services)
    back_btn.pack(pady=20)

def edit_service(service):
    clear_window()

    # Add header label to main_frame
    tk.Label(main_frame, text="Edit Service", font=("Comic Sans MS", 30), bg="#FFFFFF",
             fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # Create a container frame to center the form vertically
    container_frame = tk.Frame(main_frame, bg="#FFFFFF")
    container_frame.pack(expand=True)

    # Create form_frame inside container_frame
    form_frame = tk.Frame(container_frame, bg="#FFFFFF")
    form_frame.pack()

    # Name
    tk.Label(form_frame, text="Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5), pady=(5, 0))
    name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                          highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    name_entry.insert(0, service.name)
    name_entry.pack(padx=(10, 5), pady=(0, 10))

    # Description
    tk.Label(form_frame, text="Description", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    description_entry = tk.Text(form_frame, font=('Arial', 12), bd=0, height=5,
                                highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    description_entry.insert("1.0", service.description)
    description_entry.pack(padx=(10, 5), pady=(0, 10))

    # Price
    tk.Label(form_frame, text="Price", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    price_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                           highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    price_entry.insert(0, f"{service.price:.2f}")
    price_entry.pack(padx=(10, 5), pady=(0, 10))

    # Update button
    update_btn = tk.Button(form_frame, text="Update", command=lambda: update_service(
        service.id,
        name_entry.get(),
        description_entry.get("1.0", tk.END).strip(),
        price_entry.get()
    ))
    update_btn.pack(pady=10)

def update_service(service_id, name, description, price):
    try:
        price = float(price)
        services_service.update_service(service_id, name, description, price)
        messagebox.showinfo("Success", "Service updated successfully!")
        show_services()
    except ValueError:
        messagebox.showerror("Error", "Invalid price. Please enter a valid number.")

def delete_service(service):
    result = messagebox.askquestion("Delete Service", f"Are you sure you want to delete '{service.name}'?", icon='warning')
    if result == 'yes':
        services_service.soft_delete_service(service.id)
        messagebox.showinfo("Deleted", "Service deleted successfully.")
        show_services()

def add_note_to_service(service):
    def save_note():
        title = title_entry.get()
        content = content_text.get("1.0", tk.END).strip()
        if title and content:
            note = notes_service.create_note_only(title, content)
            services_service.add_note_to_service(service.id, note.id)
            note_window.destroy()
            view_service(service)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Add Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Save", command=save_note)
    save_btn.pack(pady=10)

def edit_note_for_service(service, note):
    def update_note():
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        if new_title and new_content:
            notes_service.update_note(note.id, new_title, new_content)
            note_window.destroy()
            view_service(service)
        else:
            messagebox.showerror("Error", "Please enter both title and content.")

    note_window = tk.Toplevel(home)
    note_window.title("Edit Note")
    note_window.geometry("400x300")

    tk.Label(note_window, text="Title").pack(pady=(10, 0))
    title_entry = tk.Entry(note_window, width=50)
    title_entry.insert(0, note.title)
    title_entry.pack(pady=(0, 10))

    tk.Label(note_window, text="Content").pack()
    content_text = tk.Text(note_window, width=50, height=10)
    content_text.insert(tk.END, note.content)
    content_text.pack()

    save_btn = tk.Button(note_window, text="Update", command=update_note)
    save_btn.pack(pady=10)

def delete_note_for_service(service, note):
    result = messagebox.askquestion("Delete Note",
                                    f"Are you sure you want to delete '{note.title}'?",
                                    icon='warning')
    if result == 'yes':
        services_service.delete_note_for_service(service.id, note.id)
        view_service(service)

# invoices
def show_invoices():
    clear_window()
    reset_sidebar_buttons()
    invoices_btn.config(bg='#1d81af')

    # add header label
    tk.Label(main_frame, text="Invoices", font=("Comic Sans MS", 30), bg="#ffffff", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # frame for filter and new invoice
    top_frame = tk.Frame(main_frame, bg="#ffffff")
    top_frame.pack(anchor="nw", padx=20, pady=10)

    # filter for unpaid or all
    filter_var = tk.StringVar(value="unpaid")

    def refresh_invoices():
        show_invoice_list(filter_var.get())

    # radio buttons for filter
    tk.Radiobutton(top_frame, text="Unpaid Only", variable=filter_var, value="unpaid", command=refresh_invoices, bg="#ffffff").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(top_frame, text="All", variable=filter_var, value="all", command=refresh_invoices, bg="#ffffff").pack(side=tk.LEFT, padx=5)

    # new invoice clickable label
    new_invoice_label = tk.Label(top_frame, text="New Invoice", fg='blue', bg='#ffffff', cursor="hand2", font=('Arial', 14, 'underline'))
    new_invoice_label.pack(side=tk.LEFT, padx=20)
    new_invoice_label.bind("<Button-1>", lambda e: show_create_invoice_form())

    # create a frame for the invoice list
    list_frame = tk.Frame(main_frame, bg="#ffffff")
    list_frame.pack(fill=tk.BOTH, expand=True)

    def show_invoice_list(filter_type):
        # clear list_frame first
        for w in list_frame.winfo_children():
            w.destroy()

        invoices = invoice_service.get_invoices(show_only_unpaid=(filter_type=="unpaid"))

        # headers
        headers = ["Invoice #", "Date", "Client", "Total", "Paid?", "Actions"]
        for idx, header in enumerate(headers):
            tk.Label(list_frame, text=header, font=('Arial',16,'bold'), bg='#ffffff').grid(row=0, column=idx, padx=10, pady=10, sticky='ew')

        # populate
        for i, inv in enumerate(invoices, start=1):
            invoice_number = inv.id
            invoice_date = inv.created_date
            client_name = inv.get_customer_full_name()
            total_str = f"${inv.total:.2f}"
            paid_str = "Yes" if inv.is_paid() else "No"

            # clickable invoice number to view
            inv_label = tk.Label(list_frame, text=str(invoice_number), fg='blue', bg='#ffffff', cursor="hand2", font=('Arial',14,'underline'))
            inv_label.grid(row=i, column=0, padx=10, pady=10, sticky='ew')
            inv_label.bind("<Button-1>", lambda e, inv_obj=inv: view_invoice(inv_obj))

            tk.Label(list_frame, text=invoice_date, font=('Arial',14), bg='#ffffff').grid(row=i, column=1, padx=10, pady=10, sticky='ew')
            tk.Label(list_frame, text=client_name, font=('Arial',14), bg='#ffffff').grid(row=i, column=2, padx=10, pady=10, sticky='ew')
            tk.Label(list_frame, text=total_str, font=('Arial',14), bg='#ffffff').grid(row=i, column=3, padx=10, pady=10, sticky='ew')
            tk.Label(list_frame, text=paid_str, font=('Arial',14), bg='#ffffff').grid(row=i, column=4, padx=10, pady=10, sticky='ew')

            # actions: view, edit, delete
            actions_frame = tk.Frame(list_frame, bg='#ffffff')
            actions_frame.grid(row=i, column=5, padx=10, pady=10, sticky='ew')

            view_btn = tk.Button(actions_frame, text="View", font=('Arial',12), command=lambda inv_obj=inv: view_invoice(inv_obj))
            view_btn.pack(side=tk.LEFT, padx=5, expand=True)

            edit_btn = tk.Button(actions_frame, text="Edit", font=('Arial',12), command=lambda inv_obj=inv: edit_invoice(inv_obj))
            edit_btn.pack(side=tk.LEFT, padx=5, expand=True)

            delete_btn = tk.Button(actions_frame, text="Delete", font=('Arial',12), command=lambda inv_obj=inv: delete_invoice(inv_obj))
            delete_btn.pack(side=tk.LEFT, padx=5, expand=True)

    # show initial list
    show_invoice_list("unpaid")


def show_create_invoice_form():
    clear_window()
    # header
    tk.Label(main_frame, text="New Invoice", font=("Comic Sans MS",30), bg="#ffffff", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    # form frame
    form_frame = tk.Frame(main_frame, bg="#ffffff")
    form_frame.pack(expand=True)

    # select customer
    tk.Label(form_frame, text="Customer", fg='black', bg='#fefefe').pack(anchor="w", padx=(10,5), pady=(5,0))
    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()
    if customer_options:
        selected_customer.set(customer_options[0])
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.pack(padx=(10,5), pady=(0,10))
    else:
        tk.Label(form_frame, text="No Customers Available", fg='red', bg='#ffffff').pack()
        return

    # invoice date and due date
    tk.Label(form_frame, text="Due Date (YYYY-MM-DD)", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5))
    due_date_entry = tk.Entry(form_frame, font=('Arial',12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    due_date_entry.pack(padx=(10,5), pady=(0,10))

    # services
    # get services to add line items
    all_services = services_service.get_all_services()
    service_options = [f"{svc.id}: {svc.name} ${svc.price:.2f}" for svc in all_services]
    service_frame = tk.Frame(form_frame, bg="#ffffff")
    service_frame.pack(pady=10, fill=tk.X)

    tk.Label(service_frame, text="Line Items (select service and date):", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5))

    line_items = []  # will store tuples of (service_var, date_entry)
    def add_line_item():
        lf = tk.Frame(service_frame, bg="#ffffff")
        lf.pack(anchor='w', fill=tk.X, pady=5)

        service_var = tk.StringVar()
        if service_options:
            service_var.set(service_options[0])
            service_dropdown = tk.OptionMenu(lf, service_var, *service_options)
            service_dropdown.pack(side=tk.LEFT, padx=(10,5))
        else:
            tk.Label(lf, text="No Services Available", fg='red', bg='#ffffff').pack(side=tk.LEFT, padx=(10,5))

        date_entry = tk.Entry(lf, font=('Arial',12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
        date_entry.pack(side=tk.LEFT, padx=(10,5))
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        line_items.append((service_var, date_entry))

    add_line_item_btn = tk.Button(service_frame, text="Add Line Item", command=add_line_item)
    add_line_item_btn.pack(anchor='w', padx=(10,5), pady=(5,0))

    # notes
    tk.Label(form_frame, text="Notes", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5), pady=(20,0))
    notes_text = tk.Text(form_frame, font=('Arial',12), bd=0, height=5, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    notes_text.pack(padx=(10,5), pady=(0,10))

    def save_invoice():
        customer_id = int(selected_customer.get().split(":")[0])
        due_date = due_date_entry.get().strip()
        notes_content = notes_text.get("1.0", tk.END).strip()

        # parse line items
        parsed_line_items = []
        for (svc_var, date_e) in line_items:
            svc_str = svc_var.get()
            if not svc_str:
                continue
            svc_id = int(svc_str.split(":")[0])
            svc_date = date_e.get().strip()
            parsed_line_items.append({"service_id": svc_id, "service_date": svc_date})

        if not parsed_line_items:
            messagebox.showerror("Error", "At least one line item is required.")
            return

        try:
            invoice = invoice_service.create_invoice(customer_id, due_date, parsed_line_items, notes_content)
            messagebox.showinfo("Success", f"Invoice #{invoice.id} created successfully!")
            show_invoices()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    save_btn = tk.Button(form_frame, text="Save Invoice", command=save_invoice)
    save_btn.pack(pady=10)


def view_invoice(invoice):
    clear_window()
    # similar layout to view_customer, view_appointment
    tk.Label(main_frame, text=f"Invoice #{invoice.id}", font=("Comic Sans MS",30), bg="#ffffff", fg="#156082").pack(anchor='nw', padx=20, pady=5)

    details_frame = tk.Frame(main_frame, bg='#ffffff')
    details_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)

    # invoice info
    tk.Label(details_frame, text="Invoice Info:", fg='black', bg='#fefefe', font=('Arial',16,'bold')).pack(anchor='w', pady=(10,0))
    tk.Label(details_frame, text=f"Date: {invoice.created_date}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))
    tk.Label(details_frame, text=f"Due Date: {invoice.due_date}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))
    tk.Label(details_frame, text=f"Paid: {'Yes' if invoice.is_paid() else 'No'}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))

    # customer info
    tk.Label(details_frame, text="Customer Info:", fg='black', bg='#fefefe', font=('Arial',16,'bold')).pack(anchor='w', pady=(20,0))
    tk.Label(details_frame, text=f"Name: {invoice.get_customer_full_name()}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))
    tk.Label(details_frame, text=f"Email: {invoice.customer_email}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))
    tk.Label(details_frame, text=f"Phone: {invoice.customer_phone}", fg='black', bg='#fefefe', font=('Arial',14)).pack(anchor='w', pady=(0,10))
    tk.Label(details_frame, text=f"Address: {invoice.customer_address}", fg='black', bg='#fefefe', font=('Arial',14), wraplength=800, justify=tk.LEFT).pack(anchor='w', pady=(0,10))

    # line items
    tk.Label(details_frame, text="Line Items:", fg='black', bg='#fefefe', font=('Arial',16,'bold')).pack(anchor='w', pady=(20,0))
    line_items_frame = tk.Frame(details_frame, bg='#ffffff')
    line_items_frame.pack(anchor='w', fill=tk.X)

    headers = ["Date", "Service", "Qty", "Price", "Line Total"]
    for idx, h in enumerate(headers):
        tk.Label(line_items_frame, text=h, font=('Arial',14,'bold'), bg='#fefefe').grid(row=0, column=idx, padx=10, pady=10, sticky='ew')

    for i, li in enumerate(invoice.line_items, start=1):
        tk.Label(line_items_frame, text=li.service_date, font=('Arial',14), bg='#fefefe').grid(row=i, column=0, padx=10, pady=5, sticky='ew')
        tk.Label(line_items_frame, text=li.service_name, font=('Arial',14), bg='#fefefe').grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        tk.Label(line_items_frame, text=str(li.quantity), font=('Arial',14), bg='#fefefe').grid(row=i, column=2, padx=10, pady=5, sticky='ew')
        tk.Label(line_items_frame, text=f"${li.service_price:.2f}", font=('Arial',14), bg='#fefefe').grid(row=i, column=3, padx=10, pady=5, sticky='ew')
        tk.Label(line_items_frame, text=f"${li.get_line_total():.2f}", font=('Arial',14), bg='#fefefe').grid(row=i, column=4, padx=10, pady=5, sticky='ew')

    tk.Label(details_frame, text=f"Total: ${invoice.total:.2f}", fg='black', bg='#fefefe', font=('Arial',16,'bold')).pack(anchor='e', pady=(20,0))

    # notes section
    tk.Label(details_frame, text="Notes:", fg='black', bg='#fefefe', font=('Arial',16,'bold')).pack(anchor='w', pady=(20,0))

    add_note_btn = tk.Button(details_frame, text="Add New Note", command=lambda: add_note_to_invoice(invoice))
    add_note_btn.pack(anchor='w', pady=(10,10))

    if invoice.notes:
        for note in invoice.notes:
            note_frame = tk.Frame(details_frame, bg="#fefefe", bd=1, relief=tk.RIDGE)
            note_frame.pack(fill=tk.X, pady=(0,10))

            title_label = tk.Label(note_frame, text=note.title, fg='blue', bg='#fefefe', cursor="hand2", font=('Arial',14,'underline'))
            title_label.pack(anchor='w', padx=10, pady=5)
            title_label.bind("<Button-1>", lambda e, n=note: view_note_popup(n))

            snippet = (note.content[:100] + '...') if len(note.content) > 100 else note.content
            tk.Label(note_frame, text=snippet, fg='black', bg='#fefefe', font=('Arial',12)).pack(anchor='w', padx=10)

            date_label = tk.Label(note_frame, text=note.created_at.strftime('%Y-%m-%d %H:%M:%S'), fg='gray', bg='#fefefe', font=('Arial',10))
            date_label.pack(anchor='e', padx=10, pady=5)

            actions_frame = tk.Frame(note_frame, bg='#fefefe')
            actions_frame.pack(anchor='e', padx=10, pady=5)

            edit_btn = tk.Button(actions_frame, text="Edit", command=lambda n=note: edit_note_for_invoice(invoice, n))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = tk.Button(actions_frame, text="Delete", command=lambda n=note: delete_note_for_invoice(invoice, n))
            delete_btn.pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(details_frame, text="No notes available.", fg='gray', bg='#fefefe', font=('Arial',12)).pack(anchor='w', pady=(10,0))

    # back, edit, delete buttons at bottom
    bottom_frame = tk.Frame(main_frame, bg='#ffffff')
    bottom_frame.pack(anchor='e', padx=20, pady=20)

    back_btn = tk.Button(bottom_frame, text="Back", font=('Arial',12), command=show_invoices)
    back_btn.pack(side=tk.LEFT, padx=10)

    edit_btn = tk.Button(bottom_frame, text="Edit", font=('Arial',12), command=lambda: edit_invoice(invoice))
    edit_btn.pack(side=tk.LEFT, padx=10)

    delete_btn = tk.Button(bottom_frame, text="Delete", font=('Arial',12), command=lambda: delete_invoice(invoice))
    delete_btn.pack(side=tk.LEFT, padx=10)

    if not invoice.is_paid():
        pay_btn = tk.Button(bottom_frame, text="Pay", font=('Arial',12), command=lambda: mark_invoice_as_paid(invoice))
        pay_btn.pack(side=tk.LEFT, padx=10)

def mark_invoice_as_paid(invoice):
    invoice_service.mark_invoice_paid(invoice.id)
    messagebox.showinfo("Success", f"Invoice #{invoice.id} marked as paid.")
    # display invoice again
    updated_invoice = invoice_service.get_invoice_by_id(invoice.id)
    view_invoice(updated_invoice)

def delete_invoice(invoice):
    result = messagebox.askquestion("Delete Invoice", f"Are you sure you want to delete Invoice #{invoice.id}?", icon='warning')
    if result == 'yes':
        invoice_service.soft_delete_invoice(invoice.id)
        messagebox.showinfo("Deleted", f"Invoice #{invoice.id} deleted successfully.")
        show_invoices()

def edit_invoice(invoice):
    clear_window()
    tk.Label(main_frame, text=f"Edit Invoice #{invoice.id}", font=("Comic Sans MS",30), bg="#ffffff", fg="#156082").pack(anchor="nw", padx=20, pady=5)

    form_frame = tk.Frame(main_frame, bg="#ffffff")
    form_frame.pack(expand=True)

    # customer
    tk.Label(form_frame, text="Customer", fg='black', bg='#fefefe').pack(anchor="w", padx=(10,5), pady=(5,0))
    customers = customer_service.get_all_customers()
    customer_options = [f"{c.id}: {c.first_name} {c.last_name}" for c in customers]
    selected_customer = tk.StringVar()
    if customer_options:
        # set to current invoice's customer
        current_customer_option = f"{invoice.customer_id}: {invoice.customer_first_name} {invoice.customer_last_name}"
        # if current_customer_option not in list, just append it
        if current_customer_option not in customer_options:
            customer_options.insert(0, current_customer_option)
        selected_customer.set(current_customer_option)
        customer_dropdown = tk.OptionMenu(form_frame, selected_customer, *customer_options)
        customer_dropdown.pack(padx=(10,5), pady=(0,10))
    else:
        tk.Label(form_frame, text="No Customers Available", fg='red', bg='#ffffff').pack()
        return

    # due date
    tk.Label(form_frame, text="Due Date (YYYY-MM-DD)", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5))
    due_date_entry = tk.Entry(form_frame, font=('Arial',12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    due_date_entry.pack(padx=(10,5), pady=(0,10))
    due_date_entry.insert(0, invoice.due_date)

    # line items
    all_services = services_service.get_all_services()
    service_options = [f"{svc.id}: {svc.name} ${svc.price:.2f}" for svc in all_services]

    service_frame = tk.Frame(form_frame, bg="#ffffff")
    service_frame.pack(pady=10, fill=tk.X)

    tk.Label(service_frame, text="Line Items (select service and date):", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5))

    line_items = []  # (service_var, date_entry)

    def add_line_item_prefilled(service_id=None, service_date_str=None):
        # if no service_id given, default to first in list if available
        lf = tk.Frame(service_frame, bg="#ffffff")
        lf.pack(anchor='w', fill=tk.X, pady=5)

        service_var = tk.StringVar()
        if service_options:
            # find the matching service_id in service_options
            default_option = service_options[0]
            if service_id:
                for opt in service_options:
                    if opt.startswith(f"{service_id}:"):
                        default_option = opt
                        break
            service_var.set(default_option)
            service_dropdown = tk.OptionMenu(lf, service_var, *service_options)
            service_dropdown.pack(side=tk.LEFT, padx=(10,5))
        else:
            tk.Label(lf, text="No Services Available", fg='red', bg='#ffffff').pack(side=tk.LEFT, padx=(10,5))

        date_entry = tk.Entry(lf, font=('Arial',12), bd=0, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
        date_entry.pack(side=tk.LEFT, padx=(10,5))
        if service_date_str:
            date_entry.insert(0, service_date_str)
        else:
            date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        line_items.append((service_var, date_entry))

    # prefill line items from invoice
    for li in invoice.line_items:
        add_line_item_prefilled(service_id=li.service_id, service_date_str=li.service_date)

    # button to add more line items if needed
    def add_line_item():
        add_line_item_prefilled()

    add_line_item_btn = tk.Button(service_frame, text="Add Line Item", command=add_line_item)
    add_line_item_btn.pack(anchor='w', padx=(10,5), pady=(5,0))

    # notes
    tk.Label(form_frame, text="Notes", fg='black', bg='#fefefe').pack(anchor='w', padx=(10,5), pady=(20,0))
    notes_text = tk.Text(form_frame, font=('Arial',12), bd=0, height=5, highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    notes_text.pack(padx=(10,5), pady=(0,10))

    # if there's at least one note, just load the content of the first note
    if invoice.notes:
        # assuming first note is main note
        notes_text.insert("1.0", invoice.notes[0].content)

    def save_edited_invoice():
        cid = int(selected_customer.get().split(":")[0])
        due_date = due_date_entry.get().strip()
        notes_content = notes_text.get("1.0", tk.END).strip()

        parsed_line_items = []
        for (svc_var, date_e) in line_items:
            svc_str = svc_var.get()
            if not svc_str:
                continue
            svc_id = int(svc_str.split(":")[0])
            svc_date = date_e.get().strip()
            parsed_line_items.append({"service_id": svc_id, "service_date": svc_date})

        if not parsed_line_items:
            messagebox.showerror("Error", "At least one line item is required.")
            return

        try:
            updated_invoice = invoice_service.update_invoice(invoice.id, cid, due_date, parsed_line_items, notes_content)
            messagebox.showinfo("Success", f"Invoice #{updated_invoice.id} updated successfully!")
            show_invoices()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    save_btn = tk.Button(form_frame, text="Update Invoice", command=save_edited_invoice)
    save_btn.pack(pady=10)

# makes default page
create_sidebar()
main_frame = tk.Frame(home, bg="#fefefe", bd=2, relief='solid')
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
show_home()
home.mainloop()

