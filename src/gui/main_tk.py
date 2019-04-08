import tkinter as tk

from src.gui.operations_tkinter import LoginFrame
from src.config.configure import Configuration


class Mainframe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = LoginFrame(self)
        self.frame.grid()


    def change(self, frame):
        self.frame = frame(self)
        self.frame.grid()

def run():
    #if __name__ == "__main__":
        check_cfg=Configuration()
        check_cfg.checkRecoveryCfg()
        app = Mainframe()
        app.mainloop()









# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame=Frame(root)
# bottomFrame.pack(side=BOTTOM)
# button1 = Button(topFrame,text='Button 1',fg='red')
# button2 = Button(topFrame,text='Button 1',fg='orange')
# button3 = Button(topFrame,text='Button 1',fg='blue')
# button4 = Button(bottomFrame,text='Button 4',fg='green')
#
# button1.pack(side=LEFT)
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack(side=BOTTOM)
#__________
# one = Label(root,text="One",bg='red',fg='white')
# one.pack()
# two = Label(root,text="Two",bg='green',fg='black')
# two.pack(fill=X)
# three = Label(root,text="Three",bg='blue',fg='white')
# three.pack(side=LEFT,fill=Y)
#_________________________
#grid
# label_1 = Label(root,text="Name")
# label_2 = Label(root,text="Password")
# entry_1 =Entry(root)
# entry_2 =Entry(root)
#
# label_1.grid(row=0,sticky=E)
# label_2.grid(row=1,sticky=E)
# entry_1.grid(row=0,column=1)
# entry_2.grid(row=1,column=1)
# checkBox=Checkbutton(root,text="Keep me logged in")
# checkBox.grid(columnspan=2)
#___________________________________________
#function bind
#
# def printName():
#     print('siemka')
#
# button_1=Button(root,text='print cos tam',command=printName)
# button_1.pack()
#___________________________________________
#functionbind cdn
# def leftClick(event):
#     print("left")
# def rightClick(event):
#     print("right")
# def middClick(event):
#     print("midd")
# frame=Frame(root,width=300,height=250)
# frame.bind("<Button-1>",leftClick)
# frame.bind("<Button-3>",rightClick)
# frame.bind("<Button-2>",middClick)
# frame.pack()
#_______________________________
# class Buttons:
#     def __init__(self,master):
#         frame = Frame(master)
#         frame.pack()
#         self.printButton = Button(frame, text="Print test",command=self.printMessage)
#         self.printButton.pack(side=LEFT)
#         self.quitButton= Button(frame, text="quit",command=frame.quit)
#         self.quitButton.pack(side=LEFT)
#
#     def printMessage(self):
#         print("siemka")
#_______________________________

#
# def doNothing():
#     print("ok, i won't")
# menu = Menu(root)
# root.config(menu=menu)
# subMenu=Menu(menu)
# menu.add_cascade(label="File",menu=subMenu)
# subMenu.add_command(label="new Project...",command=doNothing)
# subMenu.add_command(label="new",command=doNothing)
# subMenu.add_separator()
# subMenu.add_command(label="Exit",command=doNothing)
# editMenu=Menu(menu)
# menu.add_cascade(label="Edit",menu=editMenu)
# editMenu.add_command(label="Redo",command=doNothing)
#
# toolbar = Frame(root,bg="blue")
# insertButt= Button(toolbar,text="Insert Image",command=doNothing)
# insertButt.pack(side=LEFT,padx=2, pady=2)
# printButt=Button(toolbar,text="Print",command=doNothing)
# printButt.pack(side=LEFT,padx=2, pady=2)
# toolbar.pack(side=TOP,fill=X)
#
# statusbar=Label(root,text="Preparing to do nothing...",bd=1,relief=SUNKEN,anchor=W)
# statusbar.pack(side=BOTTOM,fill=X)
#______________________________________
# tkinter.messagebox.showinfo("windows that popup","bllballbalbla")
# answer=tkinter.messagebox.askquestion('question 1','Zapisac zmiany')
# if answer == 'yes':
#     print('OK zapisany do bazy')
