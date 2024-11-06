import tkinter as tk
from tkinter import messagebox
import mysql.connector 
import datetime

class LMS:
    def __init__(self, library_name):
        self.library_name = library_name
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="librarymanagement"
        )
        self.cursor = self.db.cursor()
        self.current_user_role = None
        self.root = tk.Tk()
        self.root.title(f"{self.library_name} Library Management System")
        self.login_screen()

    def login_screen(self):
        self.root.geometry("400x400")
        lbl_role = tk.Label(self.root, text="Select Role:")
        lbl_role.pack(pady=5)
        
        self.role_var = tk.StringVar(value="User")
        role_admin = tk.Radiobutton(self.root, text="Admin", variable=self.role_var, value="Admin")
        role_user = tk.Radiobutton(self.root, text="User", variable=self.role_var, value="User")
        role_admin.pack()
        role_user.pack()

        lbl_password = tk.Label(self.root, text="Enter Password:")
        lbl_password.pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=5)

        btn_login = tk.Button(self.root, text="Login", command=self.verify_login)
        btn_login.pack(pady=10)

    def verify_login(self):
        role = self.role_var.get()
        password = self.entry_password.get()
        if role == "Admin" and password == "admin123":
            self.current_user_role = "Admin"
            self.root.geometry("500x400")
            self.main_menu()
        elif role == "User":
            self.current_user_role = "User"
            self.root.geometry("500x400")
            self.main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid password for Admin.")

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        btn_display_books = tk.Button(self.root, text="Display Books", command=self.display_books)
        btn_display_books.pack(pady=10)

        if self.current_user_role == "Admin":
            btn_add_books = tk.Button(self.root, text="Add Book", command=self.add_books)
            btn_add_books.pack(pady=10)

        btn_issue_books = tk.Button(self.root, text="Issue Book", command=self.issue_books)
        btn_issue_books.pack(pady=10)

        btn_return_books = tk.Button(self.root, text="Return Book", command=self.return_books)
        btn_return_books.pack(pady=10)

        if self.current_user_role == "Admin":
            btn_filter_books = tk.Button(self.root, text="Filter Books by Semester", command=self.filter_books_by_semester)
            btn_filter_books.pack(pady=10)

        btn_quit = tk.Button(self.root, text="Quit", command=self.close)
        btn_quit.pack(pady=10)

    def display_books(self):
        self.cursor.execute("SELECT * FROM Books")
        books = self.cursor.fetchall()
        display_window = tk.Toplevel(self.root)
        display_window.title("List of Books")
        display_window.geometry("700x400")
        
        text = tk.Text(display_window)
        text.pack(expand=True, fill=tk.BOTH)
        
        text.insert(tk.END, "------------------------------------------------------------------------ List of Books ------------------------------------------------------------------------\n")
        text.insert(tk.END, "UID\t\t\tBook ID\t\t\tTitle\t\t\tStatus\t\t\tSemester\t\t\tIssued by\t\t\tIssued Date\n")
        text.insert(tk.END, "---------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        for book in books:
            lender_name = book[3] if book[3] else "N/A"
            lend_date = book[4] if book[4] else "N/A"
            semester = book[5] if book[5] else "N/A"
            text.insert(tk.END, f"{book[6]}\t\t\t{book[0]}\t\t\t{book[1]}\t\t\t{book[2]}\t\t\t{semester}\t\t\t{lender_name}\t\t\t{lend_date}\n")
        text.config(state=tk.DISABLED)

    def add_books(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")
        add_window.geometry("300x250")

        lbl_uid = tk.Label(add_window, text="Enter Book UID:")
        lbl_uid.pack(pady=5)
        entry_uid = tk.Entry(add_window)
        entry_uid.pack(pady=5)

        lbl_title = tk.Label(add_window, text="Enter Book Title:")
        lbl_title.pack(pady=5)
        entry_title = tk.Entry(add_window)
        entry_title.pack(pady=5)

        lbl_semester = tk.Label(add_window, text="Enter Semester:")
        lbl_semester.pack(pady=5)
        entry_semester = tk.Entry(add_window)
        entry_semester.pack(pady=5)

        def add():
            book_uid = entry_uid.get()
            new_title = entry_title.get()
            semester = entry_semester.get()
            if book_uid and new_title and semester:
                self.cursor.execute("INSERT INTO Books (UID, Title, Semester) VALUES (%s, %s, %s)", (book_uid, new_title, semester))
                self.db.commit()
                messagebox.showinfo("Success", f"The book '{new_title}' has been added successfully!")
                add_window.destroy()

        btn_add = tk.Button(add_window, text="Add Book", command=add)
        btn_add.pack(pady=10)

    def issue_books(self):
        issue_window = tk.Toplevel(self.root)
        issue_window.title("Issue Book")
        issue_window.geometry("300x250")

        lbl_book_uid = tk.Label(issue_window, text="Enter Book UID:")
        lbl_book_uid.pack(pady=5)
        entry_book_uid = tk.Entry(issue_window)
        entry_book_uid.pack(pady=5)

        lbl_semester = tk.Label(issue_window, text="Enter Semester:")
        lbl_semester.pack(pady=5)
        entry_user_uid = tk.Entry(issue_window)
        entry_user_uid.pack(pady=5)

        def issue():
            book_uid = entry_book_uid.get()
            user_uid = entry_user_uid.get()
            self.cursor.execute("SELECT Status FROM Books WHERE UID = %s", (book_uid,))
            result = self.cursor.fetchone()
            if result and result[0] == 'Available':
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute(
                    "UPDATE Books SET Status = 'Issued', LenderName = %s, LendDate = %s WHERE UID = %s",
                    (user_uid, current_date, book_uid)
                )
                self.db.commit()
                messagebox.showinfo("Success", "Book Issued Successfully!")
                issue_window.destroy()
            else:
                messagebox.showerror("Error", "Book is either not available or already issued.")

        btn_issue = tk.Button(issue_window, text="Issue Book", command=issue)
        btn_issue.pack(pady=10)
        
    def return_books(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")
        return_window.geometry("300x200")

        lbl_book_uid = tk.Label(return_window, text="Enter Book UID:")
        lbl_book_uid.pack(pady=5)
        entry_book_uid = tk.Entry(return_window)
        entry_book_uid.pack(pady=5)

        def return_book():
            book_uid = entry_book_uid.get()
            self.cursor.execute("SELECT Status FROM Books WHERE UID = %s", (book_uid,))
            result = self.cursor.fetchone()
            if result and result[0] == 'Issued':
                self.cursor.execute(
                    "UPDATE Books SET Status = 'Available', LenderName = NULL, LendDate = NULL WHERE UID = %s",
                    (book_uid,)
                )
                self.db.commit()
                messagebox.showinfo("Success", "Book Returned Successfully!")
                return_window.destroy()
            else:
                messagebox.showerror("Error", "This book is either not issued or does not exist.")

        btn_return = tk.Button(return_window, text="Return Book", command=return_book)
        btn_return.pack(pady=10)

    def filter_books_by_semester(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filter Books by Semester")
        filter_window.geometry("300x200")

        lbl_semester = tk.Label(filter_window, text="Enter Semester:")
        lbl_semester.pack(pady=5)
        entry_semester = tk.Entry(filter_window)
        entry_semester.pack(pady=5)

        def filter_books():
            semester = entry_semester.get()
            self.cursor.execute("SELECT * FROM Books WHERE Semester = %s", (semester,))
            books = self.cursor.fetchall()
            display_window = tk.Toplevel(filter_window)
            display_window.title("Filtered Books")
            display_window.geometry("700x400")
            
            text = tk.Text(display_window)
            text.pack(expand=True, fill=tk.BOTH)
            
            text.insert(tk.END, "---------------------------------------------------------- Filtered Books ----------------------------------------------------------\n")
            text.insert(tk.END, "UID\t\t\tBook ID\t\t\tTitle\t\t\tStatus\t\t\tSemester\t\t\tIssued by\t\t\tIssued Date\n")
            text.insert(tk.END, "------------------------------------------------------------------------------------------------------------------------------------------------\n")
            for book in books:
                lender_name = book[3] if book[3] else "N/A"
                lend_date = book[4] if book[4] else "N/A"
                text.insert(tk.END, f"{book[6]}\t\t\t{book[0]}\t\t\t{book[1]}\t\t\t{book[2]}\t\t\t{book[5]}\t\t\t{lender_name}\t\t\t{lend_date}\n")
            text.config(state=tk.DISABLED)

        btn_filter = tk.Button(filter_window, text="Filter Books", command=filter_books)
        btn_filter.pack(pady=10)

    def close(self):
        self.db.close()
        self.root.quit()

if __name__ == "__main__":
    mylms = LMS("Python's")
    mylms.root.mainloop()