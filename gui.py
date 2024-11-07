import tkinter as tk
import tkinter.messagebox as messagebox
from user_manager import UserManager
from customer_service import CustomerService

# main window creation
home = tk.Tk()
home.geometry("1600x900")
home.title("Groomy") # title of the screen

# creates the UserManager instance
user_manager = UserManager('users.db')

def create_sidebar():
    global home_btn, customers_btn

    sidebar = tk.Frame(home, bg='#156082', width=225, bd=2, relief='solid')
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    # create sidebar buttons for each window
    home_btn = tk.Button(sidebar, text="HOME", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_home)
    home_btn.pack(pady=(100,10))

    customers_btn = tk.Button(sidebar, text="CUSTOMERS", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_customers)
    customers_btn.pack(pady=10)

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
    tk.Label(main_frame, text="Create New Customer", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

    form_frame = tk.Frame(main_frame, bg="#FFFFFF")
    form_frame.pack(expand=True)

    # first name label and entry
    tk.Label(form_frame, text="First Name", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5), pady=(5, 0))
    first_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                                highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    first_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # last name label and entry
    tk.Label(form_frame, text="Last Name", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    last_name_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                               highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    last_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # email address label and entry
    tk.Label(form_frame, text="Email Address", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    email_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                           highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    email_entry.pack(padx=(10, 5), pady=(0, 10))

    # phone number label and entry
    tk.Label(form_frame, text="Phone Number", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    phone_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                           highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
    phone_entry.pack(padx=(10, 5), pady=(0, 10))

    # address label and entry
    tk.Label(form_frame, text="Address", fg='black', bg='#fefefe').pack(anchor="w", padx=(10, 5))
    address_entry = tk.Entry(form_frame, font=('Arial', 12), bd=0,
                             highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af')
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
    tk.Label(main_frame, text="Edit Customer", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

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
    last_name_entry = tk.Entry(
        form_frame, font=('Arial', 12), bd=0,
        highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af'
    )
    last_name_entry.insert(0, customer.last_name)
    last_name_entry.pack(padx=(10, 5), pady=(0, 10))

    # email address label and entry
    tk.Label(form_frame, text="Email Address", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    email_entry = tk.Entry(
        form_frame, font=('Arial', 12), bd=0,
        highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af'
    )
    email_entry.insert(0, customer.email)
    email_entry.pack(padx=(10, 5), pady=(0, 10))

    # phone number label and entry
    tk.Label(form_frame, text="Phone Number", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    phone_entry = tk.Entry(
        form_frame, font=('Arial', 12), bd=0,
        highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af'
    )
    phone_entry.insert(0, customer.phone_number)
    phone_entry.pack(padx=(10, 5), pady=(0, 10))

    # address label and entry
    tk.Label(form_frame, text="Address", fg='black', bg='#fefefe').pack(
        anchor="w", padx=(10, 5))
    address_entry = tk.Entry(
        form_frame, font=('Arial', 12), bd=0,
        highlightthickness=2, highlightbackground='#156082', highlightcolor='#1d81af'
    )
    address_entry.insert(0, customer.address)
    address_entry.pack(padx=(10, 5), pady=(0, 10))

    # clickable label for updating the customer
    update_label = tk.Label(
        form_frame, text="Update Customer", fg='blue', bg='#FFFFFF', cursor="hand2",
        font=('Arial', 14, 'underline')
    )
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
    tk.Label(main_frame, text="Customers", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

    # create new customer frame
    link_frame = tk.Frame(main_frame, bg="#FFFFFF")
    link_frame.pack(pady=(0, 20))

    # label to click and create a new customer
    create_customer_label = tk.Label(link_frame, text="Create New Customer", fg='blue', bg='#FFFFFF', cursor="hand2",
                                     font=('Arial', 14, 'underline'))
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
        tk.Label(list_frame, text=header, font=('Arial', 16, 'bold'), bg="#FFFFFF").grid(
            row=0, column=idx, padx=10, pady=10, sticky='ew')

    # adds to customer list
    for idx, customer in enumerate(customers, start=1):
        full_name = f"{customer.first_name} {customer.last_name}"
        tk.Label(list_frame, text=full_name, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(
            row=idx, column=0, padx=10, pady=10, sticky='ew')
        tk.Label(list_frame, text=customer.email, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(
            row=idx, column=1, padx=10, pady=10, sticky='ew')
        tk.Label(list_frame, text=customer.phone_number, font=('Arial', 14), bg="#FFFFFF", anchor='center').grid(
            row=idx, column=2, padx=10, pady=10, sticky='ew')

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
    tk.Label(main_frame, text="Customer Details", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(
        anchor="nw", padx=20, pady=5)

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
        tk.Label(details_frame, text=label_text + ":", fg='black', bg='#fefefe', font=('Arial', 16, 'bold')).pack(
            anchor="w", pady=(10, 0))
        tk.Label(details_frame, text=value, fg='black', bg='#fefefe', font=('Arial', 14)).pack(
            anchor="w", pady=(0, 10))

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


# General functions
def reset_sidebar_buttons():
    home_btn.config(bg='#156082')
    customers_btn.config(bg='#156082')

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
