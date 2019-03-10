#!/usr/bin/python
import threading
from tkinter import *
from tkinter import messagebox
from modules import *
from eegcontroler import *


#DOCS
#http://effbot.org/tkinterbook/label.htm


def getNewRoot(title):
    root = Tk()
    root.title(title)
    return root


def functionBindingtoWidget(controler,module):
    root = Tk()
    root.title("Experimental Module")

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
    button1 = Button(root, text="Start Dispatcher",command=on_start)
    button1.pack()
    button2 = Button(root, text="Pause Dispatcher",bg="red", command=on_stop)
    button2.pack()
    button3 = Button(root, text=module.userEventName, bg="red", command=module.changeEventState)
    button3.pack()
    root.mainloop()



def factoryModuleGui(selected):
    if selected == 1:
        module = printModule()
        dispatcher = ModularDispatcher(module)
        controler = OSCcontroler(dispatcher)
        controler.buildServer()
        functionBindingtoWidget(controler,module)
    elif selected == 2:
        module = printModuleTest
        dispatcher = ModularDispatcher(module)
        controler = OSCcontroler(dispatcher)
        controler.buildServer()
        functionBindingtoWidget(controler,module)
    elif selected == 3:
        mg = ModularGui(ExperimentalGui())
        mg.setModuleConfigurationTools()
        mg.startDisplay()




def selectModuleMenu():
    root = getNewRoot('Modular EEG System')
    selected = IntVar()
    radlist = []

    welcome = Label(root,text ="Benvinguts a Modular EEG System!")
    welcome.grid(columnspan=2, row=0,sticky="N")
    select = Label(root, text="Elegeix un modul:")
    select.grid(columnspan=2, row=1, sticky="N")

    value = 1
    for module in modules:
        radlist.append(Radiobutton(root, text=module, value=value, variable=selected))
        value+=1

    value = 2
    for radio in radlist:
        radio.grid(column=0,row =value,sticky="W")
        value +=1
    radlist[0].select()

    def clicked():
        root.destroy()
        factoryModuleGui(selected.get())


    btn = Button(root, text="Confirma", command=clicked)
    btn.grid(columnspan=2, row=value,sticky="N")
    root.mainloop()


class ModularGui:

    def __init__(self,moduleGUI):
        self.module = moduleGUI
        self.root = Tk()

    def setModuleConfigurationTools(self):
        self.root.title("Configuració")
        btn = Button(self.root, text="Confirma", command=self.endConfiguration)
        btn.grid(column=0, row=0)

        config = Label(self.root, text="Configuració")
        config.grid(column=1, row=0)
        self.module.attachConfigurationWidgets(self.root)

    def startDisplay(self):
        self.root.mainloop()

    def endConfiguration(self):
        configuredModule =  self.module.confirm()
        dispatcher = ModularDispatcher(configuredModule)
        controler = OSCcontroler(dispatcher)
        controler.buildServer()
        self.root.destroy()
        functionBindingtoWidget(controler,configuredModule) #Provisional



class ExperimentalGui:

    def __init__(self):
        self.checkboxValues = []

    def attachConfigurationWidgets(self,root):

        filename = Label(root, text="Nom del fitxer")
        filename.grid(column=0, row=1, sticky="W")

        self.filename = Entry(root)
        self.filename.grid(column=1, row=1)

        eventName = Label(root, text="Nom de l'event")
        eventName.grid(column=0, row=2, sticky="W")

        self.event = Entry(root)
        self.event.grid(column=1, row=2)

        def selectAll():
            for checkBox in routeBoxes:
                    checkBox.toggle()

        var = StringVar()
        c = Checkbutton(root, text="Selecciona tots", variable=var, command=selectAll)
        c.grid(column=3, row=1)

        vrow = 2
        routeBoxes = []
        for route in routes:
            var = StringVar()
            c = Checkbutton(root, text=route, variable=var, onvalue=route, offvalue="!selected")
            c.grid(column=3, row=vrow)
            self.checkboxValues.append(var)
            routeBoxes.append(c)
            vrow += 1

    def confirm(self):
        filename = self.filename.get()
        eventname = self.event.get()
        selected = []

        for var in self.checkboxValues:
            if var.get() != "!selected":
                selected.append(var.get())

        return ExperimentalModule(selected,filename,eventname)