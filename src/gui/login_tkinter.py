from tkinter import *
import tkinter.messagebox as tm
from src.processing.load_to_kimai import KimaiLoader

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)
        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        print(username, password)
        new = KimaiLoader()
        auth = new.authentication(username,password)
        if auth:
            api_key = new.catch_api_key(auth)
            tm.showinfo("window",api_key)
        else:
            tm.showerror("Login error", "Incorrect username")