import tkinter as tk
import tkinter.messagebox as tm
from src.processing.load_to_kimai import KimaiLoader
from src.config.configure import Configuration
conf = Configuration()
import datetime
from tkcalendar import Calendar


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
            tm.showerror("LOGIN ERROR","Błąd logowania, sprawdź czy zmieniłeś hasło w kimai")
        except ValueError:
            cfg=conf.readFromConfig()['cfg']
            tm.showerror("WEB ERROR", f"Błąd parsowania strony kimai, sprawdź czy zgadza się strona z {cfg}")

        else:
            for widget in self.master.winfo_children():
                widget.grid_remove()
            self.master.change(MainAppTk)


class MainAppTk(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        master.title("Main application")
        master.geometry("370x200")
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

    def firstSecondDateTimeValidation(self,first,second,start_h,end_h):
        try:
            first_date=datetime.datetime.strptime(first,"%Y-%m-%d")
            second_date=datetime.datetime.strptime(second,"%Y-%m-%d")
        except ValueError:
            tm.showerror("DATE ERROR", "Zły format daty, powinnien być RRRR-MM-DD")
            return False
        if second_date < first_date:
            tm.showerror("DATE ERROR", f"DATA OD {first} powinna być większa niż DO {second}")
            self.input_end_day.delete(0, 10)
        try:
            datetime.datetime.strptime(start_h, "%H:%M")
        except ValueError:
            tm.showerror("TIME ERROR", "Zły format godzin, powinnien być HH:MM")
            self.input_start_hour.delete(0, 10)
            return False
        try:
            datetime.datetime.strptime(end_h, "%H:%M")
        except ValueError:
            tm.showerror("TIME ERROR", "Zły format godzin, powinnien być HH:MM")
            self.input_end_hour.delete(0,10)
            return False


    def _submit_btn_clicked(self):
        start_day = self.input_start_day.get()
        end_day = self.input_end_day.get()
        start_hour = self.input_start_hour.get()
        end_hour = self.input_end_hour.get()
        if self.firstSecondDateTimeValidation(start_day,end_day,start_hour,end_hour) == False:
            pass
        else:
            new_records = KimaiLoader()
            new_records.set_new_record(api_key,start_day,end_day,start_hour,end_hour)



    def windows_options(self):
        top = tk.Toplevel()
        top.geometry("450x400")
        top.title("Opcje")
        list = KimaiLoader()


        # frame_customer = tk.Frame(top)
        # frame_customer.pack()
        def saveInputHours():
            a = f"{input_hours_a_start.get()},{input_hours_a_end.get()}"
            if a !=(','):
                conf.saveToFile(shift_a=a)
            b = f"{input_hours_b_start.get()},{input_hours_b_end.get()}"
            if b !=(','):
                conf.saveToFile(shift_b=b)
            c = f"{input_hours_c_start.get()},{input_hours_c_end.get()}"
            if c !=(','):
                conf.saveToFile(shift_c=c)
            cc = f"{input_hours_cc_start.get()},{input_hours_cc_end.get()}"
            if cc !=(','):
                conf.saveToFile(shift_cc=cc)
            w = f"{input_hours_w_start.get()},{input_hours_w_end.get()}"
            if w !=(','):
                conf.saveToFile(shift_w=w)
            random = f"{input_hours_random_start.get()},{input_hours_random_end.get()}"
            if random !=(','):
                conf.saveToFile(shift_random=random)
            if (a or b or c or cc or w or random) != (',') :
                tm.showinfo("Information", "Zapisano")

        frame_project = tk.Frame(top)
        frame_project.pack(side=tk.TOP,anchor="w")
        frame_task = tk.Frame(top)
        frame_task.pack(side=tk.TOP,anchor="w")
        hours_project = tk.Frame(top)
        hours_project.pack(side=tk.LEFT)
        # tk.Label(frame_customer, text="Wybierz zespół domyślny").pack()
        # tk.Label(frame_customer, text="Aktualnie domyślny jest:").pack()
        tk.Label(frame_project, text="Wybierz projekt domyślny").grid(row=1,column=0,sticky=tk.W)
        tk.Label(frame_project, text=f"Domyślny jest: {conf.readFromConfig()['project_name']}").grid(row=0,column=2,sticky=tk.W)
        tk.Label(frame_task, text="Wybierz zadanie domyślne").grid(row=1,column=0,sticky=tk.W)
        tk.Label(frame_task, text=f"Domyślny jest: {conf.readFromConfig()['task_name']}").grid(row=0,column=2,sticky=tk.W,pady=10)
        label_hours_a = tk.Label(hours_project, text=f'A, jest od {conf.readFromConfig()["shift_a"][0]} do {conf.readFromConfig()["shift_a"][1]}, zmień na: ', fg="black")
        label_hours_between_a = tk.Label(hours_project,text=f'do',fg="black")
        label_hours_between_b = tk.Label(hours_project, text=f'do', fg="black")
        label_hours_between_c = tk.Label(hours_project, text=f'do', fg="black")
        label_hours_between_cc = tk.Label(hours_project, text=f'do', fg="black")
        label_hours_between_w = tk.Label(hours_project, text=f'do', fg="black")
        label_hours_between_random = tk.Label(hours_project, text=f'do', fg="black")
        label_hours_b = tk.Label(hours_project, text=f'B, jest od {conf.readFromConfig()["shift_b"][0]} do {conf.readFromConfig()["shift_b"][1]}, zmień na: ', fg="black")
        label_hours_c = tk.Label(hours_project, text=f'C, jest od {conf.readFromConfig()["shift_c"][0]} do {conf.readFromConfig()["shift_c"][1]}, zmień na: ', fg="black")
        label_hours_cc = tk.Label(hours_project, text=f'CC, jest od {conf.readFromConfig()["shift_cc"][0]} do {conf.readFromConfig()["shift_cc"][1]}, zmień na: ', fg="black")
        label_hours_w = tk.Label(hours_project, text=f'W, jest od {conf.readFromConfig()["shift_w"][0]} do {conf.readFromConfig()["shift_w"][1]}, zmień na: ', fg="black")
        label_hours_random = tk.Label(hours_project, text=f'Własna, jest od {conf.readFromConfig()["shift_random"][0]} do {conf.readFromConfig()["shift_random"][1]}, zmień na: ', fg="black")

        input_hours_a_start = tk.Entry(hours_project,width = 6)
        input_hours_a_end = tk.Entry(hours_project,width = 6)
        input_hours_b_start = tk.Entry(hours_project, width=6)
        input_hours_b_end = tk.Entry(hours_project, width=6)
        input_hours_c_start = tk.Entry(hours_project, width=6)
        input_hours_c_end = tk.Entry(hours_project, width=6)
        input_hours_cc_start = tk.Entry(hours_project, width=6)
        input_hours_cc_end = tk.Entry(hours_project, width=6)
        input_hours_w_start = tk.Entry(hours_project, width=6)
        input_hours_w_end = tk.Entry(hours_project, width=6)
        input_hours_random_start = tk.Entry(hours_project, width=6)
        input_hours_random_end = tk.Entry(hours_project, width=6)

        submit_button = tk.Button(hours_project, text="Zapisz godziny", command=saveInputHours)
        label_hours_a.grid(row=0, column=0, sticky=tk.W)
        input_hours_a_start.grid(row=0, column=1)
        label_hours_between_a.grid(row=0,column=2)
        input_hours_a_end.grid(row=0, column=3)

        label_hours_b.grid(row=1, column=0, sticky=tk.W)
        input_hours_b_start.grid(row=1, column=1)
        label_hours_between_b.grid(row=1, column=2)
        input_hours_b_end.grid(row=1, column=3)

        label_hours_c.grid(row=2, column=0, sticky=tk.W)
        input_hours_c_start.grid(row=2, column=1)
        label_hours_between_c.grid(row=2, column=2)
        input_hours_c_end.grid(row=2, column=3)

        label_hours_cc.grid(row=3, column=0, sticky=tk.W)
        input_hours_cc_start.grid(row=3, column=1)
        label_hours_between_cc.grid(row=3, column=2)
        input_hours_cc_end.grid(row=3, column=3)

        label_hours_w.grid(row=4, column=0, sticky=tk.W)
        input_hours_w_start.grid(row=4, column=1)
        label_hours_between_w.grid(row=4, column=2)
        input_hours_w_end.grid(row=4, column=3)

        label_hours_random.grid(row=5, column=0, sticky=tk.W)
        input_hours_random_start.grid(row=5, column=1)
        label_hours_between_random.grid(row=5, column=2)
        input_hours_random_end.grid(row=5, column=3)

        submit_button.grid(row=6, column=0)


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
        def insertTasks(tasks_list):
            a = 0
            TasksList.delete(0, tk.END)
            while a != len(tasks_list):
                insert=(tasks_list[a].get('id')),tasks_list[a].get('name')

                TasksList.insert(a, insert)
                a += 1
        ProjectList = tk.Listbox(frame_project, width=30, height=3, font=("Helvetica", 8))
        project=list.get_project(api_key)
        project_list=list.catch_result(project)
        a = 0
        while a != len(project_list):
            insert=(project_list[a].get('project_id')),project_list[a].get('project_name')
            ProjectList.insert(a,insert)
            a+=1
        scrollbar_project = tk.Scrollbar(frame_project, orient="vertical")
        scrollbar_project.config(command=ProjectList.yview)
        scrollbar_project.grid(row=2,column=1,sticky=tk.W)
        ProjectList.config(yscrollcommand=scrollbar_project.set)
        ProjectList.grid(row=2,column=0,sticky=tk.W)
        def return_clicked_project():
            clicked_project = ProjectList.curselection()
            get=ProjectList.get(clicked_project)
            i =0
            n = False
            while n !=True:
                if get[1] == project_list[i].get('project_name'):
                    list=(project_list[i].get('tasks_list'))
                    insertTasks(list)
                    n = True
                else:
                    i+=1
            p = get[0]
            conf.saveToFile(project_value=str(p),project_name=get[1])
            conf.saveToFile(taskId_value="", taskId_name="")
            tm.showinfo("Information","Zapisano, zadania wyzerowane, zapisz zadanie")
        button = tk.Button(frame_project,text="zapisz",command=return_clicked_project)
        button.grid(row=2,column=2,sticky=tk.W)
        TasksList = tk.Listbox(frame_task, width=30, height=3, font=("Helvetica", 8))

        scrollbar_task = tk.Scrollbar(frame_task, orient="vertical")
        scrollbar_task.config(command=TasksList.yview)
        scrollbar_task.grid(row=2,column=1,sticky=tk.W)
        TasksList.config(yscrollcommand=scrollbar_task.set)
        TasksList.grid(row=2,column=0,sticky=tk.W)
        def return_clicked_task():
             clicked_task = TasksList.curselection()
             get=TasksList.get(clicked_task)
             conf.saveToFile(taskId_value=str(get[0]),taskId_name=get[1])
             tm.showinfo("Information", "Zapisano")

        button = tk.Button(frame_task,text="zapisz",command=return_clicked_task)
        button.grid(row=2,column=2,sticky=tk.W)


    def gui_calendar_start(self):
        def print_sel():
            date_clicked= cal.selection_get()
            date_clicked = date_clicked.strftime("%Y-%m-%d")
            self.input_start_day.delete(0, 10)
            self.input_start_day.insert(10,date_clicked)
            top.destroy()


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
            top.destroy()


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
        elif value == 'własna':
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
                'zmiana c', 'zmiana cc', 'zmiana w','własna']

        lb = tk.Listbox(master,height=6,width=10)

        for i in acts:
            lb.insert(tk.END, i)

        lb.bind("<<ListboxSelect>>", self.onSelect)

        #master.columnconfigure(0, weight=3)
        lb.grid(row=0,column=3,columnspan=1, rowspan=3,pady=5,padx=5)

        self.var = tk.StringVar()


        label_start_day = tk.Label(master, text="Data OD", fg="black")
        label_start_hour = tk.Label(master, text="Godzina OD", fg="black")
        self.input_start_day = tk.Entry(master)
        self.input_start_hour = tk.Entry(master)
        label_end_day = tk.Label(master, text="Data DO", fg="black")
        label_end_hour = tk.Label(master, text="Godzina DO", fg="black")
        date_button = tk.Button(master, text='Data', command=self.gui_calendar_start)
        date_buttone = tk.Button(master, text='Data', command=self.gui_calendar_end)

        self.input_end_day = tk.Entry(master)
        self.input_end_hour = tk.Entry(master)
        label_start_day.grid(row=0, column=0, sticky=tk.W)
        label_start_hour.grid(row=1, column=0, sticky=tk.W)
        self.input_start_day.grid(row=0, column=1)
        date_button.grid(row=0, column=2,padx=5)
        self.input_start_hour.grid(row=1, column=1)
        #lbox.grid(column=3, row=0, rowspan=5, sticky=tk.W)
        label_end_day.grid(row=2, column=0, sticky=tk.W)
        label_end_hour.grid(row=3, column=0, sticky=tk.W)
        self.input_end_day.grid(row=2, column=1)
        date_buttone.grid(row=2, column=2,padx=5)
        self.input_end_hour.grid(row=3, column=1)
        submit_button = tk.Button(master, text="Zapisz do KIMAI", command=self._submit_btn_clicked)
        submit_button.grid(row=4,column=2,pady=20)
        tk.Label(master, text=f"Ustawiony projekt: {conf.readFromConfig()['project_name']}").grid(row=5, column=0,
                                                                                                     sticky=tk.W)
        tk.Label(master, text=f"Domyślny jest: {conf.readFromConfig()['task_name']}").grid(row=6, column=0,
                                                                                               sticky=tk.W)
