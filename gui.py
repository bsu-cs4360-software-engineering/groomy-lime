import tkinter as tk
from user_manager import UserManager

# main window creation
home = tk.Tk()
home.geometry("1600x900")
home.title("Groomy") # title of the screen

# creates UserManager instance
user_manager = UserManager('users.db')

def create_sidebar():
    global home_btn # allows editing in show_home
    sidebar = tk.Frame(home, bg='#156082', width=225, bd=2, relief='solid')
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)

    # create sidebar buttons for each window
    home_btn = tk.Button(sidebar, text="HOME", font=('Arial', 15), fg='#FFFFFF', bg='#156082', bd=0, height=2, width=20, command=show_home)
    home_btn.pack(pady=250)


def show_home():
    clear_window()
    tk.Label(main_frame, text="Groomy", font=("Comic Sans MS", 30), bg="#FFFFFF", fg="#156082").pack(anchor="nw", padx=20, pady=5) # creates the label at the top left (this can probably be made into a function later)
    # later a function must be added to reset all buttons to their original background color to ensure that only one button is the highlight color at a time
    home_btn.config(bg='#1d81af')

    # username and password inputs
    create_login_form()

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

    # pressing enter in the password entry box attempts to login
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

# create the sidebar
create_sidebar()

# Main frame creation
main_frame = tk.Frame(home, bg="#fefefe", bd=2, relief='solid')
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


# show the home page at first
show_home()

# starts the loop
home.mainloop()
