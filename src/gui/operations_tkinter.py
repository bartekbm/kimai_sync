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
        master.geometry("500x350")
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
        top.geometry("500x500")
        top.title("Options")
        list = KimaiLoader()
        # frame_customer = tk.Frame(top)
        # frame_customer.pack()

        frame_project = tk.Frame(top)
        frame_project.pack()
        frame_task = tk.Frame(top)
        frame_task.pack()
        hours_project = tk.Frame(top)
        hours_project.pack()
        # tk.Label(frame_customer, text="Wybierz zespół domyślny").pack()
        # tk.Label(frame_customer, text="Aktualnie domyślny jest:").pack()
        tk.Label(frame_project, text="Wybierz projekt domyślny").pack()
        tk.Label(frame_project, text=f"Aktualnie domyślny jest {conf.readFromConfig()['project_name']}").pack()
        tk.Label(frame_task, text="Wybierz zadanie domyślne").pack()
        tk.Label(frame_task, text=f"Aktualnie domyślny jest{conf.readFromConfig()['task_name']}").pack()
        label_hours_a = tk.Label(hours_project, text=f'Zmiana A, jest od {conf.readFromConfig()["shift_a"][0]} do {conf.readFromConfig()["shift_a"][1]}, zmień na: ', fg="black")
        label_hours_a_between = tk.Label(hours_project,text=f'do',fg="black")
        label_hours_b = tk.Label(hours_project, text=f'Zmiana B, jest od {conf.readFromConfig()["shift_b"][0]} do {conf.readFromConfig()["shift_b"][1]}, zmień na: ', fg="black")
        label_hours_c = tk.Label(hours_project, text=f'Zmiana C, jest od {conf.readFromConfig()["shift_c"][0]} do {conf.readFromConfig()["shift_c"][1]}, zmień na: ', fg="black")
        label_hours_cc = tk.Label(hours_project, text=f'Zmiana CC, jest od {conf.readFromConfig()["shift_cc"][0]} do {conf.readFromConfig()["shift_cc"][1]}, zmień na: ', fg="black")
        label_hours_w = tk.Label(hours_project, text=f'Zmiana W, jest od {conf.readFromConfig()["shift_w"][0]} do {conf.readFromConfig()["shift_w"][1]}, zmień na: ', fg="black")
        label_hours_random = tk.Label(hours_project, text=f'Zmiana do wprowadzenia, jest od {conf.readFromConfig()["shift_random"][0]} do {conf.readFromConfig()["shift_random"][1]}, zmień na: ', fg="black")
        input_hours_a_start = tk.Entry(hours_project,width = 6)
        input_hours_a_end = tk.Entry(hours_project,width = 6)
        label_hours_a.grid(row=0, column=0, sticky=tk.W)
        input_hours_a_start.grid(row=0, column=1)
        label_hours_a_between.grid(row=0,column=2)
        input_hours_a_end.grid(row=0, column=3)
        label_hours_b.grid(row=1, column=0, sticky=tk.W)
        label_hours_c.grid(row=2, column=0, sticky=tk.W)
        label_hours_cc.grid(row=3, column=0, sticky=tk.W)
        label_hours_w.grid(row=4, column=0, sticky=tk.W)
        label_hours_random.grid(row=5, column=0, sticky=tk.W)
        def saveInputHours():
            pass
        # CustomerList = tk.Listbox(frame_customer, width=30, height=3, font=("Helvetica", 8))
        # customer = list.get_customer(api_key)
        # customer_list = list.catch_result(customer)
        # a = 0
        # while a != len(customer_list):
        #     CustomerList.insert(a, customer_list[a])
        #     a += 1
        # scrollbar_customer = tk.Scrollbar(frame_customer, orient="vertical")
        # scrollbar_customer.config(command=CustomerList.yview)
        # scrollbar_customer.pack(side="right", fill="y")
        # CustomerList.config(yscrollcommand=scrollbar_customer.set)
        # CustomerList.pack()
        # def return_clicked_customer():
        #     clicked_customer = CustomerList.curselection()
        #     get=CustomerList.get(clicked_customer)
        #     print(get)
        # button = tk.Button(frame_customer,text="zapisz",command=return_clicked_customer)
        # button.pack()
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


    def gui_calendar_start(self):
        def print_sel():
            date_clicked= cal.selection_get()
            date_clicked = date_clicked.strftime("%Y-%m-%d")
            self.input_start_day.delete(0, 10)
            self.input_start_day.insert(10,date_clicked)


        top = tk.Toplevel(self.master)

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand1")

        cal.pack(fill="both", expand=True)
        tk.Button(top, text="ok", command=lambda: print_sel()).pack()

    def gui_calendar_end(self):
        def print_sel():
            date_clicked= cal.selection_get()
            date_clicked = date_clicked.strftime("%Y-%m-%d")
            self.input_end_day.delete(0, 10)
            self.input_end_day.insert(10,date_clicked)


        top = tk.Toplevel(self.master)

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand1")

        cal.pack(fill="both", expand=True)
        tk.Button(top, text="ok", command=lambda: print_sel()).pack()

    def onSelect(self, val):

        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)
        if value == 'zmiana a':
            value_s = conf.readFromConfig()['shift_a'][0]
            value_e = conf.readFromConfig()['shift_a'][1]
        elif value == 'zmiana b':
            value_s = conf.readFromConfig()['shift_b'][0]
            value_e = conf.readFromConfig()['shift_b'][1]
        elif value == 'zmiana c':
            value_s = conf.readFromConfig()['shift_c'][0]
            value_e = conf.readFromConfig()['shift_c'][1]
        elif value == 'zmiana cc':
            value_s = conf.readFromConfig()['shift_cc'][0]
            value_e = conf.readFromConfig()['shift_cc'][1]
        elif value == 'zmiana w':
            value_s = conf.readFromConfig()['shift_w'][0]
            value_e = conf.readFromConfig()['shift_w'][1]
        elif value == 'zmiana do ustawienia':
            value_s = conf.readFromConfig()['shift_random'][0]
            value_e = conf.readFromConfig()['shift_random'][1]
        else:
            value_s =""
            value_e=""
        self.input_start_hour.delete(0, tk.END)
        self.input_start_hour.insert(10, value_s)
        self.input_end_hour.delete(0, tk.END)
        self.input_end_hour.insert(10, value_e)


    def content(self,master):

        #cnames = 'a'

        acts = ['zmiana a', 'zmiana b',
                'zmiana c', 'zmiana cc', 'zmiana w','zmiana do ustawienia']

        lb = tk.Listbox(self)

        for i in acts:
            lb.insert(tk.END, i)

        lb.bind("<<ListboxSelect>>", self.onSelect)

        lb.pack(pady=15)

        self.var = tk.StringVar()
        self.label = tk.Label(self, text=0, textvariable=self.var)
        self.label.pack()

        label_start_day = tk.Label(master, text="Data wprowadzenia początkowa", fg="black")
        label_start_hour = tk.Label(master, text="Godzina Wprowadzenia Początkowa", fg="black")
        self.input_start_day = tk.Entry(master)
        self.input_start_hour = tk.Entry(master)
        label_end_day = tk.Label(master, text="Data wprowadzenia końcowa", fg="black")
        label_end_hour = tk.Label(master, text="Godzina Wprowadzenia końcowa", fg="black")
        date_button = tk.Button(master, text='Data', command=self.gui_calendar_start)
        date_buttone = tk.Button(master, text='Data', command=self.gui_calendar_end)

        self.input_end_day = tk.Entry(master)
        self.input_end_hour = tk.Entry(master)
        label_start_day.grid(row=0, column=0, sticky=tk.W)
        label_start_hour.grid(row=1, column=0, sticky=tk.W)
        self.input_start_day.grid(row=0, column=1)
        date_button.grid(row=0, column=2)
        self.input_start_hour.grid(row=1, column=1)
        #lbox.grid(column=3, row=0, rowspan=5, sticky=tk.W)
        label_end_day.grid(row=2, column=0, sticky=tk.W)
        label_end_hour.grid(row=3, column=0, sticky=tk.W)
        self.input_end_day.grid(row=2, column=1)
        date_buttone.grid(row=2, column=2)
        self.input_end_hour.grid(row=3, column=1)
        submit_button = tk.Button(master, text="Zapisz do KIMAI", command=self._submit_btn_clicked)
        submit_button.grid(row=4, column=0)