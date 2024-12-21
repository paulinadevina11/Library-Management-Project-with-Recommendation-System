import tkinter as tk
from tkinter import messagebox, StringVar, ttk, simpledialog
from BACK_END import *

def Logout(window_user):
    # Ask the user if they really want to log out
    answer = messagebox.askquestion("Logout", "Are you sure you want to log out?")
    if answer == "yes":
        window_user.destroy()  # Destroy the current user window
        root.deiconify()  # Bring the login window back to the front
        user_name.delete(0, tk.END)
        passw.delete(0, tk.END)



# Create
def NewWindow_create(window_user):
    window_user.withdraw()
    window = tk.Toplevel()
    window.geometry('1750x1500')
    window.state("zoomed")
    window.configure(bg="#951D1D")
    newlabel = tk.Label(window, text="Add book and its detail or a new member", font="Gothic 50 bold")
    newlabel.place(relwidth=1, relheight=0.1)


    button_create_book = tk.Button(window, text="Add New Book",width = int((lebar*20)/1366), command=lambda: create_window_book(window), fg="black", font="Gothic 24 bold",
                        bg="white")

    button_create_member = tk.Button(window, text="Add New Member", width = int((lebar*20)/1366), command=lambda: create_window_member(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_create_book.place(x=int((lebar*525)/1366), y=int((tinggi*170)/768))
    button_create_member.place(x=int((lebar*525)/1366), y=int((tinggi*270)/768))

    button = tk.Button(window, text="cancel", command=lambda: main_admin(global_data[0], global_data[1], window))
    button.place(x=int((lebar*1300)/1366), y=int((tinggi*650)/768))


def create_window_book(window_user):
    window_user.withdraw()
    def validate_fields(event=None):
        # Get the values from all fields
        fields = {
            "Book Name": book_name.get(),
            "Book Author": book_author.get(),
            "Book Year": book_year.get(),
            "Book Genre": book_genre.get(),
            "Stock": book_stock.get(),
            "Examplar Code": examplar_input.get()
        }
        # Check for missing fields
        missing = [key for key, value in fields.items() if not value]

        if missing:
            messagebox.showwarning("Warning", f"Please fill in the following fields: {', '.join(missing)}")
        else:
            book_title_entry = book_name.get()
            book_author_entry = book_author.get()
            book_year_entry = book_year.get()
            book_genre_entry = book_genre.get()
            book_stock_entry = int(book_stock.get())
            book_examplar_code_entry = int(examplar_input.get())
            result, error_code = create_entry_book(book_examplar_code_entry, book_title_entry, book_author_entry, book_year_entry, book_genre_entry, book_stock_entry)
            if not result:
                if error_code == 'examplar':
                    messagebox.showwarning("Warning", f"Examplar Code has been taken")
                    examplar_input.delete(0, tk.END)
                    return
                else:
                    messagebox.showwarning("Warning", "The title exists in the current database")
                    book_name.delete(0, tk.END)
                    return
            
            messagebox.showinfo("Success", "Book has been added")
            NewWindow_create(window)
            
    window = tk.Toplevel()
    window.geometry('1750x1500')
    window.state("zoomed")
    window.configure(bg="#951D1D")
    newlabel = tk.Label(window, text="Add new Book", font="Gothic 50 bold")
    newlabel.place(relwidth=1, relheight=0.1)

    # Book Name
    book_name_label = tk.Label(window, text="Insert Book Name", font="Gothic 14 bold")
    book_name_label.place(relx=0.3, rely=0.24)
    book_name = tk.Entry(window, font="Gothic 14 bold")
    book_name.place(relx=0.3, rely=0.28, relwidth=0.4)

    # Book Author
    book_author_label = tk.Label(window, text="Insert Book Author", font="Gothic 14 bold")
    book_author_label.place(relx=0.3, rely=0.34)
    book_author = tk.Entry(window, font="Gothic 14 bold")
    book_author.place(relx=0.3, rely=0.38, relwidth=0.4)

    # Book Year
    book_year_label = tk.Label(window, text="Insert Book Year", font="Gothic 14 bold")
    book_year_label.place(relx=0.3, rely=0.44)
    book_year = tk.Entry(window, font="Gothic 14 bold")
    book_year.place(relx=0.3, rely=0.48, relwidth=0.4)

    # Book Genre
    book_genre_label = tk.Label(window, text="Insert Book Genre", font="Gothic 14 bold")
    book_genre_label.place(relx=0.3, rely=0.54)
    book_genre = tk.Entry(window, font="Gothic 14 bold")
    book_genre.place(relx=0.3, rely=0.58, relwidth=0.4)

    # Stock
    status_label = tk.Label(window, text="Insert stock", font="Gothic 14 bold")
    status_label.place(relx=0.3, rely=0.64)
    book_stock = tk.Entry(window, font="Gothic 14 bold")
    book_stock.place(relx=0.3, rely=0.68, relwidth=0.4)

    # Examplar Code
    examplar_code_label = tk.Label(window, text="Insert Examplar Code", font="Gothic 14 bold")
    examplar_code_label.place(relx=0.3, rely=0.74)
    examplar_input = tk.Entry(window, font="Gothic 14 bold")
    examplar_input.place(relx=0.3, rely=0.78, relwidth=0.4)

    # Submit Button
    Button1 = tk.Button(window, text="Submit", command=validate_fields)
    Button1.place(relx=0.48, rely=0.85)

    window.bind("<Return>", validate_fields)

    # Exit Button
    button = tk.Button(window, text="Exit", command=lambda: NewWindow_create(window))
    button.place(relx=0.95, rely=0.85)


def create_window_member(window_user):
    window_user.withdraw()

    def validate_fields(event=None):
        fields = {
            "Member NIM": user_NIM.get(),
            "Member Name": username.get(),
            "Email": email.get(),
            "Password": password.get()
        }
        # Check missing fields
        missing = [key for key, value in fields.items() if not value]
        if missing:
            messagebox.showwarning("Warning", f"Please fill in the following fields: {', '.join(missing)}")
        else:
            NIM = user_NIM.get()
            name = username.get()
            email_input = email.get()
            password_input = password.get()
            mode = status_dropdown.get()
            result, error_code = create_entry_admin_user(NIM, name, email_input, password_input, mode)
            if not result:
                messagebox.showwarning("Warning", f"{error_code.title()} has been taken")
                return

            messagebox.showinfo("Success", "New user successfully added")
            NewWindow_create(window)

    window = tk.Toplevel()
    window.geometry('1750x1500')
    window.state("zoomed")
    window.configure(bg="#951D1D")

    # Title Label
    newlabel = tk.Label(window, text="Add new Member", font="Gothic 50 bold")
    newlabel.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    # NIM Entry
    nim_label = tk.Label(window, text="Insert NIM", font="Gothic 14 bold")
    nim_label.place(relx=0.3, rely=0.24)
    user_NIM = tk.Entry(window, font="Gothic 14 bold")
    user_NIM.place(relx=0.3, rely=0.28, relwidth=0.4)

    # Name Entry
    name_label = tk.Label(window, text="Insert Name", font="Gothic 14 bold")
    name_label.place(relx=0.3, rely=0.34)
    username = tk.Entry(window, font="Gothic 14 bold")
    username.place(relx=0.3, rely=0.38, relwidth=0.4)

    # Email Entry
    email_label = tk.Label(window, text="Insert Email", font="Gothic 14 bold")
    email_label.place(relx=0.3, rely=0.44)
    email = tk.Entry(window, font="Gothic 14 bold")
    email.place(relx=0.3, rely=0.48, relwidth=0.4)

    # Password Entry
    pass_label = tk.Label(window, text="Insert Password", font="Gothic 14 bold")
    pass_label.place(relx=0.3, rely=0.54)
    password = tk.Entry(window, font="Gothic 14 bold", show="*")
    password.place(relx=0.3, rely=0.58, relwidth=0.4)

    # Status Dropdown
    status_label = tk.Label(window, text="Select Status", font="Gothic 14 bold")
    status_label.place(relx=0.3, rely=0.64)
    status_var = tk.StringVar(value="user")  # Default value
    status_dropdown = ttk.Combobox(window, textvariable=status_var, font="Gothic 14 bold", state="readonly")
    status_dropdown['values'] = ("admin", "user")
    status_dropdown.place(relx=0.3, rely=0.68, relwidth=0.4)

    # Submit Button
    Button1 = tk.Button(window, text="Submit", font="Gothic 14 bold", bg="#ffffff", command=validate_fields)
    Button1.place(relx=0.48, rely=0.85)

    window.bind("<Return>", validate_fields)

    # Exit Button
    button = tk.Button(window, text="Exit", font="Gothic 14 bold", bg="#ffffff", command=lambda: NewWindow_create(window))
    button.place(relx=0.95, rely=0.85)



# Read
def create_window_admin_read(window_user):
    window_user.withdraw()
    window = tk.Toplevel()
    window.geometry('1750x1500')
    window.state("zoomed")
    window.configure(bg="#951D1D")
    newlabel = tk.Label(window, text="View books or users", font="Gothic 50 bold")
    newlabel.place(relwidth=1, relheight=0.1)


    button_create_book = tk.Button(window, text="See books",width = int((lebar*20)/1366), command=lambda: NewWindow_read_admin(window), fg="black", font="Gothic 24 bold",
                        bg="white")

    button_create_member = tk.Button(window, text="See users", width = int((lebar*20)/1366), command=lambda: NewWindow_userview_admin(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_create_book.place(x=int((lebar*525)/1366), y=int((tinggi*170)/768))
    button_create_member.place(x=int((lebar*525)/1366), y=int((tinggi*270)/768))

    button = tk.Button(window, text="cancel", command=lambda: main_admin(global_data[0], global_data[1], window))
    button.place(x=int((lebar*1300)/1366), y=int((tinggi*650)/768))


def NewWindow_read_admin(window_user):
    window_user.withdraw()
    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Books in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search Book in Library", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.15, anchor="center")

    search_bar = tk.Entry(window1, width=int((lebar*50)/1366), font="Gothic 14 bold")
    search_bar.place(x=int((lebar*300)/1366), y=int((tinggi*165)/768))

    # Filter Menu
    search_menuButton = StringVar(value="Book")
    menuList = ["Book", "Author"]
    option = tk.OptionMenu(window1, search_menuButton, *menuList)
    option.place(x=int((lebar*920)/1366), y=int((tinggi*165)/768))

    # Order by menu
    order_by_menubutton = StringVar(value="Order by")
    order_by_option = ["Book Title", "Book Author", "Stock", "Examplar code"]
    orderbyoption = tk.OptionMenu(window1, order_by_menubutton, *order_by_option)
    orderbyoption.place(x=int((lebar*1000)/1366), y=int((tinggi*165)/768))

    # Limit menu
    limit_menubutton = StringVar(value="Limit")
    limit_option = [str(i) for i in range(1,26)]
    limitoption = tk.OptionMenu(window1, limit_menubutton, *limit_option)
    limitoption.place(x=int((lebar*1100)/1366), y=int((tinggi*165)/768))

    # Sort menu
    sort_menubutton = StringVar(value="Sort")
    sort_option = ["Ascending", "Descending"]
    sortoption = tk.OptionMenu(window1, sort_menubutton, *sort_option)
    sortoption.place(x=int((lebar*1180)/1366), y=int((tinggi*165)/768))


    # Setting up Treeview for tabular display
    columns = ("title", "author", "examplar_code", "year", "category", "stock", "borrowed", "available")
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("title", text="Title")
    my_tree.heading("author", text="Author")
    my_tree.heading("examplar_code", text="Code")
    my_tree.heading("year", text="Year")
    my_tree.heading("category", text="Category")
    my_tree.heading("stock", text="Stock")
    my_tree.heading("borrowed", text="Borrowed")
    my_tree.heading("available", text="Available")
    
    # Set column widths for proper alignment
    my_tree.column("title", anchor="w", width=700)
    my_tree.column("author", anchor="w", width=100)
    my_tree.column("examplar_code", anchor="center", width=5)
    my_tree.column("year", anchor="center", width=5)
    my_tree.column("category", anchor="w", width=50)
    my_tree.column("stock", anchor="center", width=1)
    my_tree.column("borrowed", anchor="center", width=1)
    my_tree.column("available", anchor="center", width=1)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.35)
    select_all.place(relx=0.95, rely=0.45, anchor="center", relheight=0.35)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filter_option = search_menuButton.get()
        order_by_opt = order_by_menubutton.get()
        limit_by_opt = limit_menubutton.get()
        sort_by_opt = sort_menubutton.get()

        if sort_by_opt == "Ascending":
            sort_by_opt = 'ASC'
        elif sort_by_opt == "Descending":
            sort_by_opt = 'DESC'
        else:
            sort_by_opt = 'ASC'

        if order_by_opt == 'Order by':
            order_by_opt = None

        if limit_by_opt == 'Limit':
            limit_by_opt = None
        else:
            limit_by_opt = int(limit_by_opt)
            
        filtered_data = retrieve_books(search_text, order_by_opt, limit_by_opt, sort_by_opt, filter_option)

        populate_treeview(filtered_data)

    if global_data[1] == 'user':
        # Set up the second treeview for the recommendation system
        recommend_label = tk.Label(window1, text="Recommended Books", font="Gothic 16 bold")
        recommend_label.place(relx=0.5, rely=0.7, anchor="center")

        columns_2 = ("Examplar Code", "Book Title")
        my_tree_2 = ttk.Treeview(window1, columns=columns_2, show="headings", selectmode="browse")

        my_tree_2.heading("Examplar Code", text="Code")
        my_tree_2.heading("Book Title", text="Book Title")

        my_tree_2.column("Examplar Code", anchor='center', width=20)
        my_tree_2.column('Book Title', anchor='w', width=843)

        select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree_2.yview)
        my_tree_2.configure(yscrollcommand=select_all.set)

        my_tree_2.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.9, relheight=0.2)
        select_all.place(relx=0.95, rely=0.85, anchor="center", relheight=0.2)

        def populate_recommendation_treeview(data):
            my_tree_2.delete(*my_tree_2.get_children())
            if data == None:
                return
            for val in data:
                my_tree_2.insert("", "end", values=val)

        populate_recommendation_treeview(recommend_book(global_data[2]))


    # Bind Enter key to search
    search_bar.bind("<Return>", search_books_treeview)

    def return_to_main_menu():
        window1.destroy()
        window_user.deiconify()

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=return_to_main_menu)
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_books(""))


def NewWindow_userview_admin(window_user):
    window_user.withdraw()
    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Users in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search users in POS", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.15, anchor="center")

    search_bar = tk.Entry(window1, width=int((lebar*50)/1366), font="Gothic 14 bold")
    search_bar.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.4)

    # Setting up Treeview for tabular display
    columns = ('NIM', 'Name', 'Email', 'Password')
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("NIM", text="NIM")
    my_tree.heading("Name", text="Name")
    my_tree.heading("Email", text="Email")
    my_tree.heading("Password", text="Pasword")
    
    # Set column widths for proper alignment
    my_tree.column("NIM", anchor="w", width=250)
    my_tree.column("Name", anchor="w", width=250)
    my_tree.column("Email", anchor="center", width=250)
    my_tree.column("Password", anchor="center", width=250)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.6)
    select_all.place(relx=0.95, rely=0.6, anchor="center", relheight=0.6)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filtered_data = retrieve_user_by_filter(search_text)
        populate_treeview(filtered_data)

    # Bind Enter key to search
    search_bar.bind("<Return>", search_books_treeview)

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=lambda: create_window_admin_read(window1))
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_user_by_filter())




def NewWindow_read_user(window_user=None):
    if window_user:
        window_user.withdraw()
    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Borrow Books in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search Book in Library and borrow them", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.15, anchor="center")

    search_bar = tk.Entry(window1, width=int((lebar*50)/1366), font="Gothic 14 bold")
    search_bar.place(x=int((lebar*300)/1366), y=int((tinggi*165)/768))

    # Filter Menu
    search_menuButton = StringVar(value="Book")
    menuList = ["Book", "Author"]
    option = tk.OptionMenu(window1, search_menuButton, *menuList)
    option.place(x=int((lebar*920)/1366), y=int((tinggi*165)/768))

    # Order by menu
    order_by_menubutton = StringVar(value="Order by")
    order_by_option = ["Book Title", "Book Author", "Stock", "Examplar code"]
    orderbyoption = tk.OptionMenu(window1, order_by_menubutton, *order_by_option)
    orderbyoption.place(x=int((lebar*1000)/1366), y=int((tinggi*165)/768))

    # Limit menu
    limit_menubutton = StringVar(value="Limit")
    limit_option = [str(i) for i in range(1,26)]
    limitoption = tk.OptionMenu(window1, limit_menubutton, *limit_option)
    limitoption.place(x=int((lebar*1100)/1366), y=int((tinggi*165)/768))

    # Sort menu
    sort_menubutton = StringVar(value="Sort")
    sort_option = ["Ascending", "Descending"]
    sortoption = tk.OptionMenu(window1, sort_menubutton, *sort_option)
    sortoption.place(x=int((lebar*1180)/1366), y=int((tinggi*165)/768))

    # Setting up Treeview for tabular display
    columns = ("title", "author", "examplar_code", "year", "category", "stock", "borrowed", "available")
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("title", text="Title")
    my_tree.heading("author", text="Author")
    my_tree.heading("examplar_code", text="Code")
    my_tree.heading("year", text="Year")
    my_tree.heading("category", text="Category")
    my_tree.heading("stock", text="Stock")
    my_tree.heading("borrowed", text="Borrowed")
    my_tree.heading("available", text="Available")
    
    # Set column widths for proper alignment
    my_tree.column("title", anchor="w", width=700)
    my_tree.column("author", anchor="w", width=100)
    my_tree.column("examplar_code", anchor="center", width=5)
    my_tree.column("year", anchor="center", width=5)
    my_tree.column("category", anchor="w", width=50)
    my_tree.column("stock", anchor="center", width=1)
    my_tree.column("borrowed", anchor="center", width=1)
    my_tree.column("available", anchor="center", width=1)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.35)
    select_all.place(relx=0.95, rely=0.45, anchor="center", relheight=0.35)

    # Set up the second treeview for the recommendation system
    recommend_label = tk.Label(window1, text="Recommended Books", font="Gothic 16 bold")
    recommend_label.place(relx=0.5, rely=0.7, anchor="center")

    columns_2 = ("Examplar Code", "Book Title")
    my_tree_2 = ttk.Treeview(window1, columns=columns_2, show="headings", selectmode="browse")

    my_tree_2.heading("Examplar Code", text="Code")
    my_tree_2.heading("Book Title", text="Book Title")

    my_tree_2.column("Examplar Code", anchor='center', width=20)
    my_tree_2.column('Book Title', anchor='w', width=843)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree_2.yview)
    my_tree_2.configure(yscrollcommand=select_all.set)

    my_tree_2.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.9, relheight=0.2)
    select_all.place(relx=0.95, rely=0.85, anchor="center", relheight=0.2)

    def populate_recommendation_treeview(data):
        my_tree_2.delete(*my_tree_2.get_children())
        if data == None:
            return
        for val in data:
            my_tree_2.insert("", "end", values=val)


    def on_row_click_recommendation(event=None):
        selected_item = my_tree_2.focus()
        if selected_item:
            values = my_tree_2.item(selected_item, "values")
            title = values[1]
            result = retrieve_books(title)
            data = result[0]
            borrowing_book_user(selected_item, data)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filter_option = search_menuButton.get()
        order_by_opt = order_by_menubutton.get()
        limit_by_opt = limit_menubutton.get()
        sort_by_opt = sort_menubutton.get()

        if sort_by_opt == "Ascending":
            sort_by_opt = 'ASC'
        elif sort_by_opt == "Descending":
            sort_by_opt = 'DESC'
        else:
            sort_by_opt = 'ASC'

        if order_by_opt == 'Order by':
            order_by_opt = None

        if limit_by_opt == 'Limit':
            limit_by_opt = None
        else:
            limit_by_opt = int(limit_by_opt)
            
        filtered_data = retrieve_books(search_text, order_by_opt, limit_by_opt, sort_by_opt, filter_option)

        populate_treeview(filtered_data)

    # Row click handler
    def on_row_click(event=None):
        selected_item = my_tree.focus()  # Get the selected item
        if selected_item:
            values = my_tree.item(selected_item, "values")  # Get the row's values
            borrowing_book_user(selected_item, values)

    # Bind the search value to enter
    window1.bind("<Return>", search_books_treeview)
    # Bind Treeview row click to the handler
    my_tree.bind("<Double-1>", on_row_click)
    my_tree_2.bind("<Double-1>", on_row_click_recommendation)

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=lambda: main_user(global_data[0], global_data[1], window1))
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_books(""))
    populate_recommendation_treeview(recommend_book(global_data[2]))


def borrowing_book_user(selected_item, book_value=None):
    if book_value:
        book_title, book_stock, book_borrowed, book_available = book_value[0], int(book_value[5]), int(book_value[6]), int(book_value[7])
    else:
        messagebox.showwarning("Warning", f"There is no book value")
        return NewWindow_read_user()
    
    if book_available == 0:
        messagebox.showinfo("Sorry", "The book you want to borrow is unavailable")
        return NewWindow_read_user()
    
    result = messagebox.askyesno("Confirmation", f"Please confirm your request to borrow {book_title}")
    if result:
        new_book_borrowed = book_borrowed + 1
        new_book_available = book_available - 1
        update_entry(book_title, book_stock, new_book_available, new_book_borrowed)
        messagebox.showinfo("Success", f"Your request to borrow {book_title} is complete")
        return NewWindow_read_user()
    else:
        return NewWindow_read_user()




def NewWindow_historyview_user(window_user):
    window_user.withdraw()

    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="User History in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label
    search_label = tk.Label(window1, text="This is your book history", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.15, anchor="center")

    # Setting up Treeview for tabular display
    columns = ('Examplar Code', 'Book Title', 'Book Author')
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("Examplar Code", text="Examplar Code")
    my_tree.heading("Book Title", text="Book Title")
    my_tree.heading("Book Author", text="Book Author")
    
    # Set column widths for proper alignment
    my_tree.column("Examplar Code", anchor="w", width=100)
    my_tree.column("Book Title", anchor="w", width=1400)
    my_tree.column("Book Author", anchor="center", width=200)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.6)
    select_all.place(relx=0.95, rely=0.6, anchor="center", relheight=0.6)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

     # Back button to return to the main menu
    def return_to_main_menu():
        window1.destroy()
        window_user.deiconify()

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=return_to_main_menu)
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_user_history_by_filter(global_data[2]))




def NewWindow_returning_user(window_user=None):
    if window_user:
        window_user.withdraw()

    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Return Books in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search Book in Library and return them", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.15, anchor="center")

    search_bar = tk.Entry(window1, width=int((lebar*50)/1366), font="Gothic 14 bold")
    search_bar.place(x=int((lebar*300)/1366), y=int((tinggi*165)/768))

    # Filter Menu
    search_menuButton = StringVar(value="Book")
    menuList = ["Book", "Author"]
    option = tk.OptionMenu(window1, search_menuButton, *menuList)
    option.place(x=int((lebar*920)/1366), y=int((tinggi*165)/768))

    # Order by menu
    order_by_menubutton = StringVar(value="Order by")
    order_by_option = ["Book Title", "Book Author", "Stock", "Examplar code"]
    orderbyoption = tk.OptionMenu(window1, order_by_menubutton, *order_by_option)
    orderbyoption.place(x=int((lebar*1000)/1366), y=int((tinggi*165)/768))

    # Limit menu
    limit_menubutton = StringVar(value="Limit")
    limit_option = [str(i) for i in range(1,26)]
    limitoption = tk.OptionMenu(window1, limit_menubutton, *limit_option)
    limitoption.place(x=int((lebar*1100)/1366), y=int((tinggi*165)/768))

    # Sort menu
    sort_menubutton = StringVar(value="Sort")
    sort_option = ["Ascending", "Descending"]
    sortoption = tk.OptionMenu(window1, sort_menubutton, *sort_option)
    sortoption.place(x=int((lebar*1180)/1366), y=int((tinggi*165)/768))


    # Setting up Treeview for tabular display
    columns = ("title", "author", "examplar_code", "year", "category", "stock", "borrowed", "available")
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("title", text="Title")
    my_tree.heading("author", text="Author")
    my_tree.heading("examplar_code", text="Code")
    my_tree.heading("year", text="Year")
    my_tree.heading("category", text="Category")
    my_tree.heading("stock", text="Stock")
    my_tree.heading("borrowed", text="Borrowed")
    my_tree.heading("available", text="Available")
    
    # Set column widths for proper alignment
    my_tree.column("title", anchor="w", width=700)
    my_tree.column("author", anchor="w", width=100)
    my_tree.column("examplar_code", anchor="center", width=5)
    my_tree.column("year", anchor="center", width=5)
    my_tree.column("category", anchor="w", width=50)
    my_tree.column("stock", anchor="center", width=1)
    my_tree.column("borrowed", anchor="center", width=1)
    my_tree.column("available", anchor="center", width=1)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.35)
    select_all.place(relx=0.95, rely=0.45, anchor="center", relheight=0.35)

    # Set up the second treeview for the recommendation system
    recommend_label = tk.Label(window1, text="Recommended Books", font="Gothic 16 bold")
    recommend_label.place(relx=0.5, rely=0.7, anchor="center")

    columns_2 = ("Examplar Code", "Book Title")
    my_tree_2 = ttk.Treeview(window1, columns=columns_2, show="headings", selectmode="browse")

    my_tree_2.heading("Examplar Code", text="Code")
    my_tree_2.heading("Book Title", text="Book Title")

    my_tree_2.column("Examplar Code", anchor='center', width=20)
    my_tree_2.column('Book Title', anchor='w', width=843)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree_2.yview)
    my_tree_2.configure(yscrollcommand=select_all.set)

    my_tree_2.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.9, relheight=0.2)
    select_all.place(relx=0.95, rely=0.85, anchor="center", relheight=0.2)

    def populate_recommendation_treeview(data):
        my_tree_2.delete(*my_tree_2.get_children())
        if data == None:
            return
        for val in data:
            my_tree_2.insert("", "end", values=val)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filter_option = search_menuButton.get()
        order_by_opt = order_by_menubutton.get()
        limit_by_opt = limit_menubutton.get()
        sort_by_opt = sort_menubutton.get()

        if sort_by_opt == "Ascending":
            sort_by_opt = 'ASC'
        elif sort_by_opt == "Descending":
            sort_by_opt = 'DESC'
        else:
            sort_by_opt = 'ASC'

        if order_by_opt == 'Order by':
            order_by_opt = None

        if limit_by_opt == 'Limit':
            limit_by_opt = None
        else:
            limit_by_opt = int(limit_by_opt)
            
        filtered_data = retrieve_books(search_text, order_by_opt, limit_by_opt, sort_by_opt, filter_option)

        populate_treeview(filtered_data)

    # Row click handler
    def on_row_click(event=None):
        selected_item = my_tree.focus()  # Get the selected item
        if selected_item:
            window1.withdraw()
            values = my_tree.item(selected_item, "values")  # Get the row's values
            if values:
                # Extract relevant details for the selected book
                book_title = values[0]
                book_author = values[1]
                examplar_code = values[2]

                # Prompt user for rating using a simple input dialog
                rating = simpledialog.askinteger(
                "Rate Book",
                f"Rate the book '{book_title}' by {book_author} (1-5):",
                minvalue=1,
                maxvalue=5
                )

                if rating:
                    return_book(global_data[2], examplar_code, rating)
                
                return NewWindow_returning_user()
            

   # Bind the search value to enter
    window1.bind("<Return>", search_books_treeview)
    # Bind Treeview row click to the handler
    my_tree.bind("<Double-1>", on_row_click)

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=lambda: main_user(global_data[0], global_data[1], window1))
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_books(""))
    populate_recommendation_treeview(recommend_book(global_data[2]))



# Update
def NewWindow_update(window_user):
    window_user.withdraw()
    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Update Books in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search Book in Library and Update Them", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.1, anchor="center")

    search_bar = tk.Entry(window1, font="Gothic 14 bold")
    search_bar.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.4)

    # Filter Menu
    search_menuButton = tk.StringVar(value="Book")
    menuList = ["Book", "Author"]
    option = tk.OptionMenu(window1, search_menuButton, *menuList)
    option.place(relx=0.8, rely=0.2, anchor="center")

    # Order by menu
    order_by_menubutton = StringVar(value="Order by")
    order_by_option = ["Book Title", "Book Author", "Stock", "Examplar code"]
    orderbyoption = tk.OptionMenu(window1, order_by_menubutton, *order_by_option)
    orderbyoption.place(x=int((lebar*1000)/1366), y=int((tinggi*165)/768))

    # Limit menu
    limit_menubutton = StringVar(value="Limit")
    limit_option = [str(i) for i in range(1,26)]
    limitoption = tk.OptionMenu(window1, limit_menubutton, *limit_option)
    limitoption.place(x=int((lebar*1100)/1366), y=int((tinggi*165)/768))

    # Sort menu
    sort_menubutton = StringVar(value="Sort")
    sort_option = ["Ascending", "Descending"]
    sortoption = tk.OptionMenu(window1, sort_menubutton, *sort_option)
    sortoption.place(x=int((lebar*1180)/1366), y=int((tinggi*165)/768))

    # Setting up Treeview for tabular display
    columns = ("title", "author", "examplar_code", "year", "category", "stock", "borrowed", "available")
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("title", text="Title")
    my_tree.heading("author", text="Author")
    my_tree.heading("examplar_code", text="Code")
    my_tree.heading("year", text="Year")
    my_tree.heading("category", text="Category")
    my_tree.heading("stock", text="Stock")
    my_tree.heading("borrowed", text="Borrowed")
    my_tree.heading("available", text="Available")
    
    # Set column widths for proper alignment
    my_tree.column("title", anchor="w", width=700)
    my_tree.column("author", anchor="w", width=100)
    my_tree.column("examplar_code", anchor="center", width=5)
    my_tree.column("year", anchor="center", width=5)
    my_tree.column("category", anchor="w", width=50)
    my_tree.column("stock", anchor="center", width=1)
    my_tree.column("borrowed", anchor="center", width=1)
    my_tree.column("available", anchor="center", width=1)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.6)
    select_all.place(relx=0.95, rely=0.6, anchor="center", relheight=0.6)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filter_option = search_menuButton.get()
        order_by_opt = order_by_menubutton.get()
        limit_by_opt = limit_menubutton.get()
        sort_by_opt = sort_menubutton.get()

        if sort_by_opt == "Ascending":
            sort_by_opt = 'ASC'
        elif sort_by_opt == "Descending":
            sort_by_opt = 'DESC'
        else:
            sort_by_opt = 'ASC'

        if order_by_opt == 'Order by':
            order_by_opt = None

        if limit_by_opt == 'Limit':
            limit_by_opt = None
        else:
            limit_by_opt = int(limit_by_opt)
            
        filtered_data = retrieve_books(search_text, order_by_opt, limit_by_opt, sort_by_opt, filter_option)

        populate_treeview(filtered_data)

    # Row click handler
    def on_row_click(event=None):
        selected_item = my_tree.focus()  # Get the selected item
        if selected_item:
            values = my_tree.item(selected_item, "values")  # Get the row's values
            update_book(window1, selected_item, values)

    # Bind the search value to enter
    window1.bind("<Return>", search_books_treeview)
    # Bind Treeview row click to the handler
    my_tree.bind("<Double-1>", on_row_click)

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=lambda: main_admin(global_data[0], global_data[1], window1))
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_books(""))


def update_book(window_user, selected_item, book_values=None):
    window_user.withdraw()
    def validate_fields(events=None):
        fields = {
            "stock available": stock_available_entry.get(),
            'stock borrowed': stock_borrowed_entry.get(),
            'stock total': stock_total_entry.get()
        }
        missing = [key for key, values in fields.items() if not values]
        if missing:
            messagebox.showwarning("Warning", f"Please fill in the following fields: {', '.join(missing)}")
        
        stock_available = int(stock_available_entry.get())
        stock_borrowed = int(stock_borrowed_entry.get())
        stock_total = int(stock_total_entry.get())

        if stock_total != stock_available + stock_borrowed:
            messagebox.showwarning("Warning", f"Stock count does not add up")
        else:
            update_entry(book_values[0], stock_total, stock_available, stock_borrowed)
            messagebox.showinfo("Success", f"Book has been updated")
            NewWindow_update(window)    

    window = tk.Toplevel()
    window.geometry('1750x1500')
    window.state("zoomed")
    window.configure(bg="#951D1D")
    newlabel = tk.Label(window, text="Update Book Stock", font="Gothic 50 bold")
    newlabel.place(relwidth=1, relheight=0.2)

    # Create Entry fields for stock-related information
    stock_available_label = tk.Label(window, text="Stock Available", font="Gothic 14 bold")
    stock_available_label.place(relx=0.3, rely=0.34)
    stock_available_entry = tk.Entry(window, font="Gothic 14 bold")
    stock_available_entry.place(relx=0.3, rely=0.38, relwidth=0.4)

    stock_borrowed_label = tk.Label(window, text="Stock Borrowed", font="Gothic 14 bold")
    stock_borrowed_label.place(relx=0.3, rely=0.54)
    stock_borrowed_entry = tk.Entry(window, font="Gothic 14 bold")
    stock_borrowed_entry.place(relx=0.3, rely=0.58, relwidth=0.4)

    stock_total_label = tk.Label(window, text="Total Stock", font="Gothic 14 bold")
    stock_total_label.place(relx=0.3, rely=0.74)
    stock_total_entry = tk.Entry(window, font="Gothic 14 bold")
    stock_total_entry.place(relx=0.3, rely=0.78, relwidth=0.4)

    # If book_values are passed, pre-fill the fields with the selected book's values
    if book_values:
        stock_available_entry.insert(0, book_values[7])  # stock available (column 6)
        stock_borrowed_entry.insert(0, book_values[6])  # borrowed (column 7)
        stock_total_entry.insert(0, book_values[5])     # stock (column 5)

    # Button to submit the updated data
    submit_button = tk.Button(window, text="Submit", font="Gothic 14 bold", command=validate_fields)
    submit_button.place(relx=0.48, rely=0.85)

    window.bind("<Return>", validate_fields)

    # Button to cancel and close the window
    cancel_button = tk.Button(window, text="Cancel", font="Gothic 14 bold", command=lambda: NewWindow_update(window_user))
    cancel_button.place(relx=0.95, rely=0.85)



# Delete
def NewWindow_delete(window_user=None):
    if window_user:
        window_user.withdraw()

    window1 = tk.Toplevel()
    window1.geometry('1750x1500')
    window1.state("zoomed")
    window1.configure(bg="#951D1D")

    newlabel = tk.Label(window1, text="Delete Books in Library POS", font="Gothic 50 bold")
    newlabel.place(relx=0.5, rely=0.05, anchor="center")

    # Search Label and Bar
    search_label = tk.Label(window1, text="Search Book in Library and delete them", font="Gothic 16 bold")
    search_label.place(relx=0.5, rely=0.1, anchor="center")

    search_bar = tk.Entry(window1, font="Gothic 14 bold")
    search_bar.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.4)

    # Filter Menu
    search_menuButton = tk.StringVar(value="Book")
    menuList = ["Book", "Author"]
    option = tk.OptionMenu(window1, search_menuButton, *menuList)
    option.place(relx=0.8, rely=0.2, anchor="center")

    # Order by menu
    order_by_menubutton = StringVar(value="Order by")
    order_by_option = ["Book Title", "Book Author", "Stock", "Examplar code"]
    orderbyoption = tk.OptionMenu(window1, order_by_menubutton, *order_by_option)
    orderbyoption.place(x=int((lebar*1000)/1366), y=int((tinggi*165)/768))

    # Limit menu
    limit_menubutton = StringVar(value="Limit")
    limit_option = [str(i) for i in range(1,26)]
    limitoption = tk.OptionMenu(window1, limit_menubutton, *limit_option)
    limitoption.place(x=int((lebar*1100)/1366), y=int((tinggi*165)/768))

    # Sort menu
    sort_menubutton = StringVar(value="Sort")
    sort_option = ["Ascending", "Descending"]
    sortoption = tk.OptionMenu(window1, sort_menubutton, *sort_option)
    sortoption.place(x=int((lebar*1180)/1366), y=int((tinggi*165)/768))

    # Setting up Treeview for tabular display
    columns = ("title", "author", "examplar_code", "year", "category", "stock", "borrowed", "available")
    my_tree = ttk.Treeview(window1, columns=columns, show="headings", selectmode="browse")

    my_tree.heading("title", text="Title")
    my_tree.heading("author", text="Author")
    my_tree.heading("examplar_code", text="Code")
    my_tree.heading("year", text="Year")
    my_tree.heading("category", text="Category")
    my_tree.heading("stock", text="Stock")
    my_tree.heading("borrowed", text="Borrowed")
    my_tree.heading("available", text="Available")
    
    # Set column widths for proper alignment
    my_tree.column("title", anchor="w", width=700)
    my_tree.column("author", anchor="w", width=100)
    my_tree.column("examplar_code", anchor="center", width=5)
    my_tree.column("year", anchor="center", width=5)
    my_tree.column("category", anchor="w", width=50)
    my_tree.column("stock", anchor="center", width=1)
    my_tree.column("borrowed", anchor="center", width=1)
    my_tree.column("available", anchor="center", width=1)

    select_all = tk.Scrollbar(window1, orient="vertical", command=my_tree.yview)
    my_tree.configure(yscrollcommand=select_all.set)
    
    # Pack Treeview and scrollbar
    my_tree.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9, relheight=0.6)
    select_all.place(relx=0.95, rely=0.6, anchor="center", relheight=0.6)

    # Populate Treeview
    def populate_treeview(data):
        my_tree.delete(*my_tree.get_children())  # Clear existing entries
        if data == None:
            return
        for book_val in data:
            my_tree.insert("", "end", values=book_val)

    # Search functionality
    def search_books_treeview(event=None):
        search_text = search_bar.get()
        filter_option = search_menuButton.get()
        order_by_opt = order_by_menubutton.get()
        limit_by_opt = limit_menubutton.get()
        sort_by_opt = sort_menubutton.get()

        if sort_by_opt == "Ascending":
            sort_by_opt = 'ASC'
        elif sort_by_opt == "Descending":
            sort_by_opt = 'DESC'
        else:
            sort_by_opt = 'ASC'

        if order_by_opt == 'Order by':
            order_by_opt = None
        
        if limit_by_opt == 'Limit':
            limit_by_opt = None
        else:
            limit_by_opt = int(limit_by_opt)
            
        filtered_data = retrieve_books(search_text, order_by_opt, limit_by_opt, sort_by_opt, filter_option)

        populate_treeview(filtered_data)

    # Row click handler
    def on_row_click(event=None):
        selected_item = my_tree.focus()  # Get the selected item
        if selected_item:
            values = my_tree.item(selected_item, "values")  # Get the row's values
            delete_validation(selected_item, values)

    # Bind the search value to enter
    window1.bind("<Return>", search_books_treeview)
    # Bind Treeview row click to the handler
    my_tree.bind("<Double-1>", on_row_click)

    back_button = tk.Button(window1, text="Back", font="Gothic 14 bold", command=lambda: main_admin(global_data[0], global_data[1], window1))
    back_button.place(relx=0.97, rely=0.98, anchor="center")

    # Initial population with all data
    populate_treeview(retrieve_books(""))


def delete_validation(selected_item, book_values=None):
    book_title = book_values[0]
    result = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {book_title}? ")
    if result:
        result, error_code = delete_entry(book_title)
        if not result:
            messagebox.showwarning("Warning", f"{error_code} does not exist")
            return NewWindow_delete()

    return NewWindow_delete()



# Class driver
def main_admin(credentials: tuple[str, str], status, window_user=None):
    if window_user:
        window_user.withdraw()

    user, status = credentials[0], status
    window = tk.Toplevel()
    window.geometry("1750x1500")
    window.state("zoomed")
    window.configure(bg="#951D1D")
    my_label = tk.Label(window, text="Library POS",font="Gothic 50 bold")
    my_label.place(relwidth=1, relheight=0.1)
    label_welcome = tk.Label(window, text=f"welcome {user} as {status}", font="Gothic 20 bold")
    label_welcome.place(x=int((lebar*100)/1366), y=int((tinggi*75)/768))


    button_create = tk.Button(window, text="Create",width = int((lebar*20)/1366), command=lambda: NewWindow_create(window), fg="black", font="Gothic 24 bold",
                        bg="white")

    button_read = tk.Button(window, text=" Read ", width = int((lebar*20)/1366), command=lambda: create_window_admin_read(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_update = tk.Button(window, text="Update",width = int((lebar*20)/1366),command=lambda: NewWindow_update(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_delete = tk.Button(window, text="Delete",width = int((lebar*20)/1366),command=lambda: NewWindow_delete(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")
    
    button_logout = tk.Button(window, text="Logout",width = int((lebar*20)/1366), command=lambda: Logout(window), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_create.place(x=int((lebar*525)/1366), y=int((tinggi*170)/768))
    button_read.place(x=int((lebar*525)/1366), y=int((tinggi*270)/768))
    button_update.place(x=int((lebar*525)/1366), y=int((tinggi*370)/768))
    button_delete.place(x=int((lebar*525)/1366), y=int((tinggi*470)/768))
    button_logout.place(x=int((lebar*525)/1366), y=int((tinggi*570)/768))


def main_user(credentials: tuple[str, str], status, window_user=None):
    if window_user:
        window_user.withdraw()

    user, status = credentials[0], status
    window_user = tk.Toplevel()
    window_user.geometry("1750x1500")
    window_user.state("zoomed")
    window_user.configure(bg="#951D1D")
    my_label = tk.Label(window_user, text="Library POS",font="Gothic 50 bold")
    my_label.place(relwidth=1, relheight=0.1)
    label_welcome = tk.Label(window_user, text=f"welcome {user} as {status}", font="Gothic 20 bold")
    label_welcome.place(relx=0.5, rely=0.15, anchor="center")

    button_read = tk.Button(window_user, text="See Books", width = int((lebar*20)/1366), command=lambda: NewWindow_read_admin(window_user), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")
    
    button_borrow = tk.Button(window_user, text="Borrow Books", width = int((lebar*20)/1366), command=lambda: NewWindow_read_user(window_user), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")
    
    button_return = tk.Button(window_user, text="Return Book", width = int((lebar*20)/1366), command=lambda: NewWindow_returning_user(window_user), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_view_history = tk.Button(window_user, text="View history", width = int((lebar*20)/1366), command=lambda: NewWindow_historyview_user(window_user), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")
    
    button_logout = tk.Button(window_user, text="Logout",width = int((lebar*20)/1366),command=lambda: Logout(window_user), fg="black", font="Gothic 24 bold",
                        bg="white", relief="groove")

    button_read.place(x=int((lebar*525)/1366), y=int((tinggi*170)/768))
    button_borrow.place(x=int((lebar*525)/1366), y=int((tinggi*270)/768))
    button_return.place(x=int((lebar*525)/1366), y=int((tinggi*370)/768))
    button_view_history.place(x=int((lebar*525)/1366), y=int((tinggi*470)/768))
    button_logout.place(x=int((lebar*525)/1366), y=int((tinggi*570)/768))


def showuser(event=None):
    global global_data
    user = user_name.get()
    password = passw.get()
    result = login(user, password)
    if not result:
        messagebox.showerror("Error", "Invalid credentials. Please check your username or password")
        user_name.delete(0, tk.END)
        passw.delete(0, tk.END)
    
    else:
        global_data = (result[0], result[1], result[2])
        if result[1] == "user":
            root.withdraw()
            main_user(result[0], result[1])

        elif result[1] == "admin":
            root.withdraw()
            main_admin(result[0], result[1])

        else:
            raise Exception(f"User status not found")


# Main Root
if __name__ == "__main__":
    global_data = None # (Name, Password), admin/ user, nim
    root = tk.Tk()
    root.title("Library POS")
    root.geometry("1750x1500")
    root.configure(bg="#951D1D")

    lebar = root.winfo_screenwidth()
    tinggi = root.winfo_screenheight()

    newlabel = tk.Label(root, text="LOGIN SITE", font="Gothic 50 bold")
    newlabel.place(relwidth=1, relheight=0.2)

    Username_label = tk.Label(root, text="Username", font="Gothic 20 bold")
    Username_label.place(relx=0.3, rely=0.3, anchor="center")

    user_name = tk.Entry(root, width=int((lebar*50)/1366), font="Gothic 14 bold")
    user_name.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.3)

    Username_label = tk.Label(root, text="Password", font="Gothic 20 bold")
    Username_label.place(relx=0.3, rely=0.4, anchor="center")

    passw = tk.Entry(root, width=int((lebar*50)/1366), font="Gothic 14 bold", show="*")
    passw.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.3)
        
    Button1 = tk.Button(root, text="Submit", command=showuser)
    Button1.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.2)

    root.bind("<Return>", showuser)

    button = tk.Button(root, text="exit", command=root.quit)
    button.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.2)

    root.mainloop()