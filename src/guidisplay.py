#!/usr/bin/python
import threading
from tkinter import *
from tkinter import messagebox


def functionBindingtoWidget(controler):
    root = Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            controler.shutdown_server()
            root.destroy()

    def on_start():
            pid = threading.Thread(target=controler.initiate_server, name="EEGprocess")
            pid.start()

    def on_stop():
            controler.shutdown_server()


    root.protocol("WM_DELETE_WINDOW",on_closing)
    button1 = Button(root, text="StartDispatcher",command=on_start)
    button1.pack()
    button2 = Button(root, text="StopDispatcher",bg="red", command=on_stop)
    button2.pack()
    root.mainloop()
