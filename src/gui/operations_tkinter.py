import tkinter as tk
import tkinter.messagebox as tm
from src.processing.load_to_kimai import KimaiLoader
from src.config.configure import Configuration
conf = Configuration()
from tkcalendar import Calendar, DateEntry

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
        top.geometry("200x300")
        top.title("Options")
        list = KimaiLoader()

        frame_customer = tk.Frame(top)
        frame_customer.pack()
        frame_project = tk.Frame(top)
        frame_project.pack()
        frame_task = tk.Frame(top)
        frame_task.pack()
        tk.Label(frame_customer, text="Wybierz zespół domyślny").pack()
        tk.Label(frame_customer, text="Aktualnie domyślny jest:").pack()
        tk.Label(frame_project, text="Wybierz projekt domyślny").pack()
        tk.Label(frame_project, text=f"Aktualnie domyślny jest {conf.readFromConfig()[2]}").pack()
        tk.Label(frame_task, text="Wybierz zadanie domyślne").pack()
        tk.Label(frame_task, text=f"Aktualnie domyślny jest{conf.readFromConfig()[3]}").pack()
        CustomerList = tk.Listbox(frame_customer, width=30, height=3, font=("Helvetica", 8))
        customer = list.get_customer(api_key)
        customer_list = list.catch_result(customer)
        a = 0
        while a != len(customer_list):
            CustomerList.insert(a, customer_list[a])
            a += 1
        scrollbar_customer = tk.Scrollbar(frame_customer, orient="vertical")
        scrollbar_customer.config(command=CustomerList.yview)
        scrollbar_customer.pack(side="right", fill="y")
        CustomerList.config(yscrollcommand=scrollbar_customer.set)
        CustomerList.pack()
        def return_clicked_customer():
            clicked_customer = CustomerList.curselection()
            get=CustomerList.get(clicked_customer)
            print(get)
        button = tk.Button(frame_customer,text="zapisz",command=return_clicked_customer)
        button.pack()
        ProjectList = tk.Listbox(frame_project, width=30, height=3, font=("Helvetica", 8))
        project=list.get_project(api_key)
        project_list=list.catch_result(project)
        a = 0
        while a != len(project_list):
            ProjectList.insert(a,project_list[a])
            a+=1
        scrollbar_project = tk.Scrollbar(frame_project, orient="vertical")
        scrollbar_project.config(command=ProjectList.yview)
        scrollbar_project.pack(side="right", fill="y")
        ProjectList.config(yscrollcommand=scrollbar_project.set)
        ProjectList.pack()
        def return_clicked_project():
            clicked_project = ProjectList.curselection()
            get=ProjectList.get(clicked_project)
            p = get[0]
            conf.saveToFile(p=str(p),pn=get[1])
        button = tk.Button(frame_project,text="zapisz",command=return_clicked_project)
        button.pack()
        TasksList = tk.Listbox(frame_task, width=30, height=3, font=("Helvetica", 8))
        tasks = list.get_tasks(api_key)
        tasks_list = list.catch_result(tasks,'yes')
        a = 0
        while a != len(tasks_list):
            TasksList.insert(a, tasks_list[a])
            a += 1
        scrollbar_task = tk.Scrollbar(frame_task, orient="vertical")
        scrollbar_task.config(command=TasksList.yview)
        scrollbar_task.pack(side="right", fill="y")
        TasksList.config(yscrollcommand=scrollbar_task.set)
        TasksList.pack()
        def return_clicked_task():
            clicked_task = TasksList.curselection()
            get=TasksList.get(clicked_task)
            print(get[0])
            conf.saveToFile(None,t=str(get[0]),pn=None,tn=get[1])
        button = tk.Button(frame_task,text="zapisz",command=return_clicked_task)
        button.pack()


    def gui_calendar(self):
        def print_sel():
            date= cal.selection_get()
            date = date.strftime("%m/%d/%Y")
            return date

        top = tk.Toplevel(self.master)

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand1")

        cal.pack(fill="both", expand=True)
        while True:
            tk.Button(top, text="ok", command=print_sel).pack()
            return print_sel()

    def content(self,master):
        self.label_start_day = tk.Label(master, text="Data wprowadzenia początkowa", fg="black")
        self.label_start_hour = tk.Label(master, text="Godzina Wprowadzenia Początkowa", fg="black")
        self.input_start_day = tk.Entry(master)
        self.input_start_hour = tk.Entry(master)
        self.label_end_day = tk.Label(master, text="Data wprowadzenia końcowa", fg="black")
        self.label_end_hour = tk.Label(master, text="Godzina Wprowadzenia końcowa", fg="black")
        self.date_button = tk.Button(master, text='DateEntry', command=self.gui_calendar)
        self.date_buttone = tk.Button(master, text='DateEntry', command=self.gui_calendar)
        self.input_end_day = tk.Entry(master)
        self.input_end_hour = tk.Entry(master)
        self.label_start_day.grid(row=0, column=0, sticky=tk.W)
        self.label_start_hour.grid(row=1, column=0, sticky=tk.W)
        self.input_start_day.grid(row=0, column=1)
        self.date_button.grid(row=0, column=2)
        self.input_start_day.insert(10,"test")
        self.input_start_hour.grid(row=1, column=1)
        self.label_end_day.grid(row=2, column=0, sticky=tk.W)
        self.label_end_hour.grid(row=3, column=0, sticky=tk.W)
        self.input_end_day.grid(row=2, column=1)
        self.date_buttone.grid(row=2, column=2)
        self.input_end_hour.grid(row=3, column=1)
        self.submit_button = tk.Button(master, text="Zapisz do KIMAI", command=self._submit_btn_clicked)
        self.submit_button.grid(row=4, column=0)