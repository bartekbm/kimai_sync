import tkinter as tk
import tkinter.messagebox as tm
from src.processing.load_to_kimai import KimaiLoader


class LoginFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.label_name = tk.Label(master, text="Username", fg="black")
        self.label_password = tk.Label(master, text="Password", fg="black")
        self.input_name = tk.Entry(master)
        self.input_password = tk.Entry(master, show="*")

        self.label_name.grid(row=0, column=0, sticky=tk.E)
        self.label_password.grid(row=1, column=0, sticky=tk.E)

        self.input_name.grid(row=0, column=1)
        self.input_password.grid(row=1, column=1)

        self.login_button = tk.Button(master, text="Login")
        self.login_button.grid(row=1, column=2)

        self.login_button = tk.Button(master, text="Login", command=self._login_btn_clicked)
        self.login_button.grid(row=1, column=2)

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.input_name.get()
        password = self.input_password.get()

        print(username, password)
        new = KimaiLoader()
        auth = new.authentication(username, password)
        try:
            global api_key
            api_key = new.catch_api_key(auth)

        except KeyError:
            tm.showerror("window","zly login albo haslo")
        else:
            for widget in self.master.winfo_children():
                widget.grid_remove()
            self.master.change(MainAppTk)


class MainAppTk(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("Main application")
        master.geometry("400x200")
        self.content(master)
        menu=tk.Menu(master)
        master.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="Operacje",menu=filemenu)
        filemenu.add_command(label="Opcje",command=self.windows_options)
        filemenu.add_command(label="Wyjdź", command=master.quit)
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        # helpmenu.add_command(label="About...", command=About)

    def _submit_btn_clicked(self):
        start_day = self.input_start_day.get()
        end_day = self.input_end_day.get()
        start_hour = self.input_start_hour.get()
        end_hour = self.input_end_hour.get()
        new_records = KimaiLoader()
        new_records.set_new_record(api_key,start_day,end_day,start_hour,end_hour)

    def windows_options(self):
        top = tk.Toplevel()
        top.title("options")
        ProjectList = tk.Listbox(top)
        ProjectList.insert(1,"Projekt operatorzy")
        ProjectList.insert(1, "Projekt inny")
        ProjectList.insert(1, "Projekt cos tam")
        ProjectList.pack()



    def content(self,master):
        self.label_start_day = tk.Label(master, text="Data wprowadzenia początkowa", fg="black")
        self.label_start_hour = tk.Label(master, text="Godzina Wprowadzenia Początkowa", fg="black")
        self.input_start_day = tk.Entry(master)
        self.input_start_hour = tk.Entry(master)
        self.label_end_day = tk.Label(master, text="Data wprowadzenia końcowa", fg="black")
        self.label_end_hour = tk.Label(master, text="Godzina Wprowadzenia końcowa", fg="black")
        self.input_end_day = tk.Entry(master)
        self.input_end_hour = tk.Entry(master)
        self.label_start_day.grid(row=0, column=0, sticky=tk.W)
        self.label_start_hour.grid(row=1, column=0, sticky=tk.W)
        self.input_start_day.grid(row=0, column=1)
        self.input_start_hour.grid(row=1, column=1)
        self.label_end_day.grid(row=2, column=0, sticky=tk.W)
        self.label_end_hour.grid(row=3, column=0, sticky=tk.W)
        self.input_end_day.grid(row=2, column=1)
        self.input_end_hour.grid(row=3, column=1)
        self.submit_button = tk.Button(master, text="Zapisz do KIMAI", command=self._submit_btn_clicked)
        self.submit_button.grid(row=4, column=0)