#!/usr/bin/python
import threading
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

    def createGui(mg):
        mg.setModuleConfigurationTools()
        mg.startDisplay()

    if selected == "ExperimentalModule":
        mg = ModularGui(ExperimentalGui())
        createGui(mg)
    elif selected == "MouseModule":
        mg = ModularGui(MouseGui())
        createGui(mg)




def selectModuleMenu():
    root = getNewRoot('Modular EEG System')
    selected = StringVar()
    radlist = []

    welcome = Label(root,text ="Benvinguts a Modular EEG System!")
    welcome.grid(columnspan=2, row=0,sticky="N")
    select = Label(root, text="Elegeix un modul:")
    select.grid(columnspan=2, row=1, sticky="N")

    value = 1
    for module in modules:
        radlist.append(Radiobutton(root, text=module, value=module, variable=selected))
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
        self.moduleGUI = moduleGUI
        self.root = Tk()
        self.configured = 0

    def setModuleConfigurationTools(self):
        self.root.title("Configuració")
        btn = Button(self.root, text="Confirma", command=self.endConfiguration)
        btn.grid(column=0, row=0)

        config = Label(self.root, text="Configuració")
        config.grid(column=1, row=0)
        self.moduleGUI.attachConfigurationWidgets(self.root)

    def setRuntimeDispatcherTools(self,controler,configuredModule):

        def on_start():
            pid = threading.Thread(target=controler.initiate_server, name="EEGprocess")
            pid.start()

        def on_stop():
            controler.shutdown_server()

        if self.configured:
            self.root = Tk()
            self.root.title("Controlador Interficie Modular")
            dispatcher = Label(self.root, text="Interficie")
            dispatcher.grid(columnspan=2, row=0)
            btn_start = Button(self.root, text="Inicia", command=on_start)
            btn_start.grid(column=0, row=1,sticky="E")
            btn_pause = Button(self.root, text="Pausa", bg="red", command=on_stop)
            btn_pause.grid(column=1, row=1)
            module = Label(self.root, text="Modul")
            module.grid(columnspan=2, row=2,sticky="W")

            self.moduleGUI.setRuntimeModuleTools(self.root,configuredModule)


    def startDisplay(self):
        self.root.mainloop()

    def endConfiguration(self):
        configuredModule =  self.moduleGUI.confirm()
        dispatcher = ModularDispatcher(configuredModule)
        controler = OSCcontroler(dispatcher)
        controler.buildServer()
        self.root.destroy()
        self.configured = 1
        #functionBindingtoWidget(controler, configuredModule)
        self.setRuntimeDispatcherTools(controler,configuredModule)


class MouseGui:

    def __init__(self):
        self.movement_deadzone = 40
        self.movement_signalRecon = 10
        self.blinking_forButtonR = 4
        self.blinking_windowSec = 1


    def attachConfigurationWidgets(self,root):

        self.movement_deadzDef = IntVar(root,value=self.movement_deadzone)
        self.movement_signalrDef = IntVar(root,value=self.movement_signalRecon)
        self.blinking_forButtonRDef = IntVar(root,value=self.blinking_forButtonR)
        self.blinking_windowSDef = IntVar(root,value=self.blinking_windowSec)

        move = Label(root, text="Moviment")
        move.grid(column=0, row=1, sticky="N")

        move_deadzone = Label(root, text="Sensibilitat aturada")
        move_deadzone.grid(column=0, row=2, sticky="W")
        move_dEntry = Entry(root, width=4, textvariable=self.movement_deadzDef)
        move_dEntry.grid(column=1, row=2, sticky="W")

        move_signalRecon = Label(root, text="Interval de captura (senyals)")
        move_signalRecon.grid(column=0, row=3, sticky="W")
        move_sREntry = Entry(root, width=4, textvariable=self.movement_signalrDef)
        move_sREntry.grid(column=1, row=3, sticky="W")

        move_buttonR = Label(root, text="Botó dret")
        move_buttonR.grid(column=0, row=4, sticky="N")

        buttonR_blink = Label(root, text="Nº parpadejos")
        buttonR_blink.grid(column=0, row=5, sticky="W")
        buttonR_bEntry = Entry(root, width=4,textvariable=self.blinking_forButtonRDef)
        buttonR_bEntry.grid(column=1, row=5, sticky="W")

        buttonR_interval = Label(root, text="Interval parpadejos (segons)")
        buttonR_interval.grid(column=0, row=6, sticky="W")
        buttonrRi_Entry = Entry(root, width=4,textvariable=self.blinking_windowSDef)
        buttonrRi_Entry.grid(column=1, row=6, sticky="W")


    def confirm(self):

        mmd = MouseModule()
        mmd.setDeadzone(self.movement_deadzDef.get())
        mmd.setSignalRec(self.movement_signalrDef.get())
        mmd.setBlinkNumb(self.blinking_forButtonRDef.get())
        mmd.setBlinkInterval(self.blinking_windowSDef.get())

        return mmd

    def setRuntimeModuleTools(self,root,module):

        self.movement_deadzDef = IntVar(root,value=module.getDeadzone())
        self.movement_signalrDef = IntVar(root,value=module.getSignalRec())
        self.blinking_forButtonRDef = IntVar(root,value=module.getBlinkNumb())
        self.blinking_windowSDef = IntVar(root,value=module.getBlinkInterval())

        reference = Label(root, text="Referencia posicional")
        reference.grid(column=0, row=3, sticky="W")
        reference_restart = Button(root, text=module.userEventName, bg="red", command=module.changeEventState)
        reference_restart.grid(column=1, row=3, sticky="W")

        conf = Label(root, text="Configuració")
        conf.grid(columnspan=2, row=4, sticky="N")

        move = Label(root, text="Moviment")
        move.grid(column=0, row=5, sticky="W")

        move_deadzone = Label(root, text="Sensibilitat aturada")
        move_deadzone.grid(column=0, row=6, sticky="W")
        move_dEntry = Entry(root, width=4, textvariable=self.movement_deadzDef)
        move_dEntry.grid(column=1, row=6, sticky="W")

        move_signalRecon = Label(root, text="Interval de captura (senyals)")
        move_signalRecon.grid(column=0, row=7, sticky="W")
        move_sREntry = Entry(root, width=4, textvariable=self.movement_signalrDef)
        move_sREntry.grid(column=1, row=7, sticky="W")

        move_buttonR = Label(root, text="Botó dret")
        move_buttonR.grid(column=0, row=8, sticky="W")

        buttonR_blink = Label(root, text="Nº parpadejos")
        buttonR_blink.grid(column=0, row=9, sticky="W")
        buttonR_bEntry = Entry(root, width=4, textvariable=self.blinking_forButtonRDef)
        buttonR_bEntry.grid(column=1, row=9, sticky="W")

        buttonR_interval = Label(root, text="Interval parpadejos (segons)")
        buttonR_interval.grid(column=0, row=10, sticky="W")
        buttonrRi_Entry = Entry(root, width=4, textvariable=self.blinking_windowSDef)
        buttonrRi_Entry.grid(column=1, row=10, sticky="W")

        def saveRuntimeChanges():
            module.setDeadzone(self.movement_deadzDef.get())
            module.setSignalRec(self.movement_signalrDef.get())
            module.setBlinkNumb(self.blinking_forButtonRDef.get())
            module.setBlinkInterval(float(self.blinking_windowSDef.get()))


        save = Button(root, text="Guarda",command=saveRuntimeChanges)
        save.grid(columnspan=2, row=11, sticky="N")



class ExperimentalGui:

    def __init__(self):
        self.checkboxValues = []

    def attachConfigurationWidgets(self,root):

        filename = Label(root, text="Nom del fitxer")
        filename.grid(column=0, row=1, sticky="W")

        self.filename = Entry(root,width=15)
        self.filename.grid(column=1, row=1,padx=(0,20))

        eventName = Label(root, text="Nom de l'event")
        eventName.grid(column=0, row=2, sticky="W")

        self.event = Entry(root,width=15)
        self.event.grid(column=1, row=2,padx=(0,20))

        def selectAll():
            count = 0
            for checkboxValue in self.checkboxValues:
                    if checkboxValue[0].get() != checkboxValue[1]:
                        checkboxValue[0].set(checkboxValue[1])
                    else:
                        count+=1
            if count == len(self.checkboxValues):
                for checkboxValue in self.checkboxValues:
                    checkboxValue[0].set("!selected")

        c = Button(root, text="Selecciona tot", command=selectAll,anchor="w")
        c.grid(sticky="W",column=3, row=1)

        vrow = 2
        routeBoxes = []
        for route in routes:
            var = StringVar()
            c = Checkbutton(root, text=route, variable=var, onvalue=route, offvalue="!selected")
            var.set("!selected")
            c.grid(sticky="W",column=3, row=vrow)
            self.checkboxValues.append((var,route))
            routeBoxes.append(c)
            vrow += 1
        root.resizable(False,False)

    def confirm(self):
        filename = self.filename.get()
        eventname = self.event.get()
        selected = []

        for var in self.checkboxValues:
            if var[0].get() != "!selected":
                selected.append(var[0].get())

        return ExperimentalModule(selected,filename,eventname)

    def setRuntimeModuleTools(self, root, module):

        self.eventName = StringVar(root)

        capture_event = Label(root, text="Captura Event")
        capture_event.grid(column=0, row=3, sticky="W")
        btn_capture = Button(root, text=module.userEventName, bg="red", command=module.changeEventState,width=8)
        btn_capture.grid(column=1, row=3, sticky="W")

        conf = Label(root, text="Configuració")
        conf.grid(columnspan=2, row=4, sticky="N")

        eventName = Label(root, text="Nom Event")
        eventName.grid(column=0, row=5, sticky="W")
        entry_EventName = Entry(root, width=8, textvariable=self.eventName)
        entry_EventName.grid(column=1, row=5, sticky="W")

        def saveRuntimeChanges():
            module.userEventName = self.eventName.get()
            btn_capture.configure(text=module.userEventName)
            self.eventName.set("")

        save = Button(root, text="Guarda", command=saveRuntimeChanges)
        save.grid(columnspan=2, row=6, sticky="N")