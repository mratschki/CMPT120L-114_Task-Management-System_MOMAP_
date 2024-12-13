import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
import calendar
from datetime import datetime
from tkcalendar import Calendar

print("Current working dir:", os.getcwd())
os.chdir('/Users/marissa/Desktop/CMPT 120L')
from tkinter import filedialog

'''''''''''''''''''''''''''
TEAM MOMAP - Task Management System 
Desc: A task management system with kinter GUI, and caesar cipher for password encryption



'''''''''''''''''''''''''''

encryptionShift = 16  # number of characters shifted


# CAESAR CIPHER FUNCTION #
def encrypt(text, shift=encryptionShift):
    return ''.join(chr((ord(char) - 32 + shift) % 95 + 32) for char in
                   text)  # ensures that characters stay within the bounds of ASCII 32 - 126 during encryption


def decrypt(text, shift=encryptionShift):
    return ''.join(chr((ord(char) - 32 - shift) % 95 + 32) for char in text)


users = {
    "admin": {"password": encrypt("adminpass"), "tasks": []}}  # encrypts "admin123", sets user and password for admin

class UserManagementPage(tk.Frame):
    def __init__(self, parent):
            super().__init__(parent)
            tk.Label(self, text="User Management", font=("Georgia", 24)).pack(pady=20)
            tk.Button(self, text="Delete My Account", font=("Georgia", 12), command=self.delete_my_account).pack(pady=10)
            tk.Button(self, text="Change Admin Credentials", font=("Georgia", 12), command=self.change_admin_credentials).pack(pady=10)
            tk.Button(self, text="Back", font= ("Georgia", 12), command=lambda: parent.show_page(TaskPage)).pack(pady=10)

    def delete_my_account(self):
        username = self.master.current_user
        if username == "admin":
            messagebox.showerror("Error", "Admin account cannot be deleted.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete your account '{username}'?")
        if confirm:
            del users[username]
            self.master.save_users()
            messagebox.showinfo("Success", "Your account has been deleted.")
            self.master.current_user = None
            self.master.show_page(WelcomePage)
        # Method implementation

    def delete_user(self):
        if self.master.current_user != "admin":
            messagebox.showerror("Error", "Only the admin can delete other users.")
            return

        username = tk.simpledialog.askstring("Delete User", "Enter the username to delete:")
        if not username:
            return

        if username == "admin":
            messagebox.showerror("Error", "Cannot delete the admin account.")
        elif username in users:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{username}'?")
            if confirm:
                del users[username]
                self.master.save_users()
                messagebox.showinfo("Success", f"User '{username}' has been deleted.")
        else:
            messagebox.showerror("Error", f"User '{username}' does not exist.")
        # Method implementation

    def change_admin_credentials(self):
        # Method implementation
        if self.master.current_user != "admin":
            messagebox.showerror("Error", "Only the admin can change credentials.")
            return

        new_username = tk.simpledialog.askstring("Change Admin Username", "Enter new admin username:")
        if not new_username:
            return

        new_password = tk.simpledialog.askstring("Change Admin Password", "Enter new admin password:", show="*")
        if not new_password:
            return

        del users["admin"]  # Remove old admin credentials
        users[new_username] = {"password": encrypt(new_password), "tasks": []}
        self.master.current_user = new_username
        self.master.save_users()
        messagebox.showinfo("Success", "Admin credentials have been updated.")

    def logout_and_go_to_welcome(self):
        self.master.current_user = None  # Clear the logged-in user
        messagebox.showinfo("Logout", "You have been logged out.")
        self.master.show_page(WelcomePage)  # Redirect to the WelcomePage

class TaskManagementSystem(tk.Tk):  # root
    def __init__(self):
        super().__init__()
        self.title("Task Management System")  # self = instance of the class
        self.geometry("650x500")
        self.Pages = {}
        self.current_user = None
        self.load_users()


        for Page in (WelcomePage, AdminLoginPage, UserLoginPage, TaskPage,
                     CalendarPage, UserManagementPage):  # iterates over a tuple of classes representing the different pages
            page = Page(self)
            self.Pages[Page] = page  # stores pages in dictionary called Pages
            page.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure([0], weight=1)  # centers menu
        self.grid_columnconfigure([0], weight=1)  # centers menu

        self.show_page(WelcomePage)
        self.load_task()  #

    def show_page(self, page_class):
        page = self.Pages[page_class]
        page.tkraise()

    def load_users(self):   #  loads users stored in the text file
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    username, password = line.strip().split("|")
                    if username not in users:
                        users[username] = {"password": password, "tasks": []}
            print(f"Loaded users: {users}")
        except FileNotFoundError:
            print("No user file found.")

    def save_users(self):
        try:
            with open("users.txt", "w") as file:
                for username, data in users.items():
                    file.write(f"{username}|{data['password']}\n")
            print("Users saved successfully.")
        except Exception as e:
            print(f"Error saving users: {e}")

    def load_task(self):
        print("Loading tasks...")
        try:
            with open("tms_tasks.txt", "r") as file:
                for line in file:
                    user, title, time, duration, description = line.strip().split("|")
                    if user not in users:
                        users[user] = {"password": "", "tasks": []}
                    users[user]["tasks"].append({
                        "title": title.strip(),  # strips invisible characters
                        "time": time.strip(),
                        "duration": duration.strip(),
                        "description": description.strip()
                    })
            print(f"Users from task list: {users}")
        except FileNotFoundError:
            pass
        print("No tasks found")

    def save_task(self):  ###
        print("Saving tasks to tms_tasks.txt")
        try:
            with open("tms_tasks.txt", "w") as file:
                for user, data in users.items():
                    for task in data["tasks"]:
                        print(f"Saving task: {task}")  # confirms task data is saved
                        file.write(f"{user}|{task['title']}|{task['time']}|{task['duration']}|{task['description']}\n")
            print("Task saved successfully")
        except Exception as e:
            print(f"Error saving task: {e}")


# WELCOME PAGE #
class WelcomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="Admin Login", font=("Georgia", 18),
                  command=lambda: parent.show_page(AdminLoginPage)).pack(pady=10)  # pack places widget in parent widget
        tk.Button(self, text="User Login", font=("Georgia", 18),
                  command=lambda: parent.show_page(UserLoginPage)).pack(pady=10)
        tk.Button(self, text="Register", font=("Georgia", 18),
                  command=self.register_user).pack(pady=10)
        tk.Button(self, text="Exit", font=("Georgia", 18), command=self.quit_application).pack(pady=10)

    def register_user(self):
        username = tk.simpledialog.askstring("Register", "Enter a new username:")
        if not username or username in users:
            messagebox.showerror("Error", "Invalid or duplicate username.")
            return

        password = tk.simpledialog.askstring("Register", "Enter a password:", show="*")
        if not password:
            messagebox.showerror("Error", "Password is required.")
            return

        users[username] = {"password": encrypt(password), "tasks": []}
        self.master.save_users()
        messagebox.showinfo("Success", f"Account '{username}' created successfully.")

    def quit_application(self):
        messagebox.showinfo("TMS", "Thank you for using Task Management System!")
        self.quit()


# ADMIN LOGIN PAGE #
class AdminLoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Admin Login", font=("Georgia", 18)).pack(pady=20)

        ttk.Label(self, text="Username", font=("Georgia", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        ttk.Label(self, text="Password", font=("Georgia", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", font=("Georgia", 12), command=self.login)
        login_button.pack(pady=5)
        back_button = tk.Button(self, text="Back", font=("Georgia", 12), command=lambda: parent.show_page(WelcomePage))
        back_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username]["password"] == encrypt(password):
            self.master.current_user = username
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.master.show_page(TaskPage)
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")


# USER EDIT PAGE #

class UserLoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="User Login", font=("Georgia", 18)).pack(pady=20)

        ttk.Label(self, text="Username", font=("Georgia", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        ttk.Label(self, text="Password", font=("Georgia", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Login", font=("Georgia", 12), command=self.login)
        login_button.pack(pady=5)
        back_button = tk.Button(self, text="Back", font=("Georgia", 12),
                                command=lambda: parent.show_page(WelcomePage))
        back_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in users and users[username]["password"] == encrypt(password):
            self.master.current_user = username
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.master.show_page(TaskPage)
        else:
            messagebox.showerror("Login Failed", "Invalid user credentials.")


# TASK MANAGEMENT MENU/WELCOME PAGE #
class TaskPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        tk.Label(self, text="Welcome to Task Management System", font=("Georgia", 24)).pack(pady=20)  ###
        tk.Button(self, text="Add Task", font=("Georgia", 12), command=self.add_task).pack(pady=10)
        tk.Button(self, text="Edit Task", font=("Georgia", 12), command=self.edit_task).pack(pady=10)
        tk.Button(self, text="Remove Task", font=("Georgia", 12), command=self.remove_task).pack(pady=10)
        tk.Button(self, text="Search Tasks",  font=("Georgia", 12), command=self.search_tasks).pack(pady=10)
        tk.Button(self, text="View Calendar", font=("Georgia", 12), command=lambda: parent.show_page(CalendarPage)).pack(pady=10)

        tk.Button(self, text="User Management", font=("Georgia", 12), command=self.open_user_management).pack(pady=10)

        tk.Button(self, text="Log out", font=("Georgia", 12), command=self.logout_and_go_to_welcome).pack(pady=10)

    def logout_and_go_to_welcome(self):
        self.master.current_user = None  # clear the logged-in user
        messagebox.showinfo("Logout", "You have been logged out.")
        self.master.show_page(WelcomePage)  # redirect to the WelcomePage

    def open_user_management(self):
        self.master.show_page(UserManagementPage)



    # ADD TASK PAGE #
    def add_task(self):  # asks user to input fields. if nothing is entered the add task window closes out

        add_task_window = tk.Toplevel(self)
        add_task_window.title("Add Task")
        add_task_window.geometry("600x500")

        # Logout function
        def logout():
            add_task_window.destroy()
            self.master.show_page(WelcomePage)  # Directs to WelcomePage

        tk.Button(add_task_window, text="Logout", command=logout).pack(anchor="ne", padx=10, pady=10)

        # Task entry form
        task = {}

        def save_task():
            task["title"] = title_entry.get().strip()
            task["time"] = time_entry.get().strip()
            task["duration"] = duration_entry.get().strip()
            task["description"] = description_entry.get().strip()

            if not task["title"] or not task["time"] or not task["duration"] or not task["description"]:
                messagebox.showerror("Error", "All fields must be filled.")
                return

            username = "admin"
            if username in users:
                users[username]["tasks"].append(task)
                print(f"Task added: {task['title']}")
                self.master.save_task()
                messagebox.showinfo("Success", "Task added.")
                add_task_window.destroy()
            else:
                messagebox.showerror("Error", "User not found.")

        #  user enters info in the following fields
        tk.Label(add_task_window, text="Title:").pack(pady=5)
        title_entry = tk.Entry(add_task_window)
        title_entry.pack(pady=5)

        tk.Label(add_task_window, text="Time:").pack(pady=5)
        time_entry = tk.Entry(add_task_window)
        time_entry.pack(pady=5)

        tk.Label(add_task_window, text="Duration:").pack(pady=5)
        duration_entry = tk.Entry(add_task_window)
        duration_entry.pack(pady=5)

        tk.Label(add_task_window, text="Description:").pack(pady=5)
        description_entry = tk.Entry(add_task_window)
        description_entry.pack(pady=5)

        # Save button
        tk.Button(add_task_window, text="Save Task", command=save_task).pack(pady=20)
        tk.Button(add_task_window, text="Cancel", command=add_task_window.destroy).pack(pady=20)

    ########### EDIT TASK ##############

    def edit_task(self):
        username = "admin"

        # To check if there are tasks available for this user
        if not users[username]["tasks"]:
            messagebox.showinfo("No Tasks Available",
                                "No tasks available to edit.")  # shows this message if there are no tasks available to edit
            return

        task_titles = [task["title"] for task in users[username]["tasks"]]  # access the task titles of this user
        task_titles_str = "\n".join(f"{i + 1}. {title}" for i, title in enumerate(
            task_titles))  # creates a single string with the task titles and numbers them
        task_num = tk.simpledialog.askinteger("Edit Task",
                                              f"Select task to edit:\n{task_titles_str}")  # asks to enter the number of the task user wants to edit

        if task_num is None or not (
                1 <= task_num <= len(task_titles)):  # checks if the number selected is in the task list
            messagebox.showerror("Error",
                                 "Invalid selection.")  # if number is not in the task list, shows an error message
            return

        task = users[username]["tasks"][task_num - 1]  # retrieves the task the user wants to edit

        # window for the editing page
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Task")
        edit_window.geometry("600x400")
        #  logout button


        # creates labels and entry fields for task details
        tk.Label(edit_window, text="Task Title").pack(pady=5)
        title_entry = tk.Entry(edit_window)
        title_entry.insert(0, task["title"])  # default value as current title
        title_entry.pack(pady=5, padx=10)

        tk.Label(edit_window, text="Task Time").pack(pady=5)
        time_entry = tk.Entry(edit_window)
        time_entry.insert(0, task["time"])  # default value as current time
        time_entry.pack(pady=5, padx=10)

        tk.Label(edit_window, text="Task Duration").pack(pady=5)
        duration_entry = tk.Entry(edit_window)
        duration_entry.insert(0, task["duration"])  # default value as current duration
        duration_entry.pack(pady=5, padx=10)

        tk.Label(edit_window, text="Task Description").pack(pady=5)
        description_entry = tk.Entry(edit_window)
        description_entry.insert(0, task["description"])  # default value as current description
        description_entry.pack(pady=5, padx=10)

        # frame for buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack(pady=10)

        # save button to update and save the task
        def save_changes():
            task["title"] = title_entry.get() or task[
                "title"]  # saves the updated one or if field empty keeps the initial value
            task["time"] = time_entry.get() or task["time"]
            task["duration"] = duration_entry.get() or task["duration"]
            task["description"] = description_entry.get() or task["description"]

            self.master.save_task()
            messagebox.showinfo("Success", "Task updated successfully!")
            edit_window.destroy()  # Closes the edit window

        save_button = tk.Button(button_frame, text="Save Changes", command=save_changes)
        save_button.pack(side=tk.LEFT, padx=10)

        # a cancel button to close the window without saving
        cancel_button = tk.Button(button_frame, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)

        self.master.save_task()
        messagebox.showinfo("Success", "Task updated successfully!")

        # removes the task based on input user provided

    def remove_task(self):

        remove_window = tk.Toplevel(self)
        remove_window.title("Remove Task")
        remove_window.geometry("400x300")

        username = "admin"

        # Logout button
        def logout():
            remove_window.destroy()
            self.master.show_page(WelcomePage)

        logout_button = tk.Button(remove_window, text="Logout", command=logout)
        logout_button.pack(anchor="ne", padx=10, pady=10)

        #  entry field to enter which task to remove
        tk.Label(remove_window, text="Enter task title to remove:", font=("Georgia", 14)).pack(pady=10)
        task_title_entry = tk.Entry(remove_window, width=30)
        task_title_entry.pack(pady=5)

        #  removes the task based on input user provided
        def remove():
            task_title = task_title_entry.get().strip()  # Retrieve title from the above entry field

            if not task_title:
                messagebox.showerror("Error", "Please enter a task title")
                return

            if username in users:
                task_to_remove = None
                print(f"Looking for task title: {task_title.strip().lower()}")  # Debugging log
                for task in users[username]["tasks"]:
                    print(
                        f"Comparing task '{task_title.strip().lower()}' with stored task '{task['title'].strip().lower()}'")  # Debugging log
                    if task["title"].strip().lower() == task_title.strip().lower():  # Case-insensitive comparison
                        task_to_remove = task
                        break

                if task_to_remove:
                    users[username]["tasks"].remove(task_to_remove)
                    self.master.save_task()
                    messagebox.showinfo("Success", f"Task '{task_title}' removed.")
                    remove_window.destroy()
                else:
                    messagebox.showwarning("Not Found", f"Task '{task_title}' not found.")
            else:
                messagebox.showerror("Error", "User not found.")

        # Buttons for Remove Task and Cancel
        remove_button = tk.Button(remove_window, text="Remove Task", command=remove)
        remove_button.pack(pady=10)

        cancel_button = tk.Button(remove_window, text="Cancel", command=remove_window.destroy)
        cancel_button.pack(pady=10)

    ### SEARCH FUNCTION ###
    def search_tasks(self):
        # Create the main window
        def logout():
            self.destroy()
            self.master.show_page(WelcomePage)


        search_window = tk.Toplevel(self)
        search_window.title("Search tasks")
        search_window.geometry("650x500")

        tk.Label(search_window, text="Enter search term:").pack(pady=10)
        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        #  label to show results header
        task_listbox = tk.Listbox(search_window)
        task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #  function to perform the search
        def perform_search():
            search_term = search_entry.get().strip().lower()  # Get the search term
            # Find tasks that match the search term
            task_listbox.delete(0, tk.END)


            username = self.master.current_user
            if username in users:
                results = [
                    task for task in users[username]["tasks"]
                    if search_term in task["title"].lower()
                ]

                if results:
                    # Insert matching tasks into the listbox
                    for task in results:
                        task_listbox.insert(tk.END, task["title"].strip())
                else:
                    # Show a message if no results are found
                    messagebox.showinfo("No Results", "No tasks match your search.")
            else:
                messagebox.showerror("Error", "User not found")

        def show_task_details(event):
            selection = task_listbox.curselection()
            if not selection:
                return

            selected_task_title = task_listbox.get(selection[0]).strip().lower()
            print(f"Debug: Selected task title: {selected_task_title}")

            username = self.master.current_user
            if not username:
                messagebox.showerror("Error", "No user logged in")
                return

            task_details = next(
                (task for task in users[username]["tasks"] if task["title"].strip().lower() == selected_task_title),
                None
            )
            print(f"Retrieved task details: {task_details}")

            if task_details:

                detail_window = tk.Toplevel(self)
                detail_window.title("Task Details")
                detail_window.geometry("400x300")

                tk.Label(detail_window, text=f"Title: {task_details['title']}").pack(pady=5)
                tk.Label(detail_window, text=f"Time: {task_details['time']}").pack(pady=5)
                tk.Label(detail_window, text=f"Duration: {task_details['duration']}").pack(pady=5)
                tk.Label(detail_window, text=f"Description: {task_details['description']}").pack(pady=5)

                tk.Button(detail_window, text="Close", command=detail_window.destroy).pack(pady=10)
            else:
                messagebox.showerror("Error", "Task not found.")

        task_listbox.bind("<<ListboxSelect>>", show_task_details)

        #  button to trigger the search
        search_button = tk.Button(search_window, text="Search", command=perform_search)
        search_button.pack(pady=5)

        close_button = tk.Button(search_window, text="Close", command=search_window.destroy)
        close_button.pack(pady=5)



    # Create an instance of TaskSearcher and call the search_tasks method


# CALENDAR PAGE #
class CalendarPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.selected_date = None

        ttk.Label(self, text="Task Calendar", font=("Georgia", 24)).pack(pady=20)

        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="<", command=self.prev_month).pack(side=tk.LEFT, padx=10)
        self.month_label = tk.Label(nav_frame, text=self.get_month_year_label(), font=("Georgia", 15))
        self.month_label.pack(side=tk.LEFT)
        tk.Button(nav_frame, text=">", command=self.next_month).pack(side=tk.LEFT, padx=10)

        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(pady=10)
        self.create_calendar()

        tk.Button(self, text="View Tasks", command=self.view_tasks).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: parent.show_page(TaskPage)).pack(pady=10)

        self.task_listbox = tk.Listbox(self, height=10, width=50)
        self.task_listbox.pack(pady=10)

        tk.Button(self, text="Logout", command=self.logout).pack(pady=10)

        tk.Button(self, text="Back", command=lambda: parent.show_page(TaskPage)).pack(pady=10)

    def logout(self):
        #  logout button
        self.master.current_user = None
        messagebox.showinfo("Logout", "You have been logged out.")
        self.master.show_page(WelcomePage)  # Redirect to WelcomePage

    def create_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        def logout():
            add_task_window.destroy()
            self.master.show_page(WelcomePage)  # Directs to WelcomePage

        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]
        first_weekday = calendar.monthrange(self.current_year, self.current_month)[0]

        for day in ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]:
            tk.Label(self.calendar_frame, text=day, font=("Georgia", 10), width=4).grid(row=0,
                                                                                        column=["Mon", "Tues", "Wed",
                                                                                                "Thur", "Fri", "Sat",
                                                                                                "Sun"].index(day))

        row = 1
        col = first_weekday
        for day in range(1, days_in_month + 1):
            day_button = tk.Button(self.calendar_frame, text=str(day), width=4,
                                   command=lambda d=day: self.select_date(d), )
            day_button.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def get_month_year_label(self):
        return f"{calendar.month_name[self.current_month]} {self.current_year}"

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.month_label.config(text=self.get_month_year_label())
        self.create_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.month_label.config(text=self.get_month_year_label())
        self.create_calendar()

    def select_date(self, day):
        try:
            self.selected_date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            print(f"Date selected: {self.selected_date}")
            self.view_tasks()
        except AttributeError:
            print("Error: Current year or month is not defined. Make sure they are initialized")

    def view_tasks(self):
        #  shows tasks for selected date
        self.task_listbox.delete(0, tk.END)
        print(f"Selected date: {self.selected_date}")

        username = self.master.current_user
        if not username:
            messagebox.showerror("Error", "No user logged in")
            return

        selected_date = self.selected_date
        if not selected_date:
            messagebox.showinfo("Info", "Select a date to view tasks")
            return

        tasks = users.get(username, {}).get("tasks", [])
        tasks_on_date = [task for task in tasks if task.get("time", "") == selected_date]

        print(f"Viewing tasks on {selected_date}: {tasks_on_date}")

        if tasks_on_date:
            for task in tasks_on_date:
                self.task_listbox.insert(tk.END, f"{task['title']} - {task['time']}")
        else:
            self.task_listbox.insert(tk.END, "No tasks on this date")

        def logout():
            view_tasks_window.destroy()
            self.master.show_page(WelcomePage)  # Directs to WelcomePage

if __name__ == "__main__":
    app = TaskManagementSystem()
    app.mainloop()
