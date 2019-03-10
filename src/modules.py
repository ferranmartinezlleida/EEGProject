import os
from tkinter import *

routes = ["/muse/eeg", "/muse/eeg/quantization","/muse/elements/alpha_relative",
          "/muse/elements/beta_relative","/muse/elements/delta_relative",
          "/muse/elements/gamma_relative","/muse/elements/theta_relative",
          "/muse/elements/horseshoe","/muse/elements/is_good","/muse/elements/raw_fft0",
          "/muse/elements/raw_fft1","/muse/elements/raw_fft2","/muse/elements/raw_fft3",
          "/muse/elements/low_freqs_absolute","/muse/elements/alpha_absolute",
          "/muse/elements/beta_absolute","/muse/elements/delta_absolute",
          "/muse/elements/gamma_absolute","/muse/elements/theta_absolute",
          "/muse/elements/alpha_session_score","/muse/elements/beta_session_score",
          "/muse/elements/delta_session_score","/muse/elements/gamma_session_score",
          "/muse/elements/theta_session_score","/muse/acc","/muse/drlref",
          "/muse/batt","/muse/elements/blink","/muse/elements/jaw_clench","/muse/elements/touching_forehead"]

modules = ["printModule","printModuleTest","ExperimentalModule",]

class printModule:

    def __init__(self):
        pass

    def mapAllForPrint(self,dispatcher,function=print):
        dispatcher.mapSameFunctionToPaths(function, routes)

    def configure(self, dispatcher):
        self.mapAllForPrint(dispatcher)


class printModuleTest:

    def __init__(self):
        pass

    def printLOL(self,osc_path,*args):
        print(str(args).replace("(","").replace(")",""))
        print (osc_path)


    def mapAllForPrint(self,dispatcher,function=printLOL):
        dispatcher.mapSameFunctionToPaths(function,routes,True)

    def configure(self, dispatcher):
        self.mapAllForPrint(dispatcher)

class ExperimentalModule:

    def __init__(self,userRoutes,filename,userEventName="Event"):
        self.fd = open("../signals_files/" + filename + ".txt", "a+") # ERROR HANDLING AND OS USAGE
        self.event = 0
        self.userEventName = userEventName
        self.routes = userRoutes

    def changeEventState(self):
        if self.event:
            self.event = 0
        else:
            self.event = 1
        return self.event

    def saveResults(self,osc_path,*args):
        import datetime

        expModule = args[0][0][0]
        values = str(args[1])
        for x in range(2, len(args)):
            values = values + "," + str(args[x])
        time = datetime.datetime.utcnow()
        expModule.fd.write('['+str(time)+']'+osc_path+":"+values+";"+ str(expModule.userEventName) +": "+ str(expModule.event) + '\n')
        print('['+str(time)+']'+osc_path+":"+values+";"+ str(expModule.userEventName) +": "+ str(expModule.event) + '\n')


    def mapAllToFile(self,dispatcher,function=saveResults):
        dispatcher.mapSameFunctionToPaths(function,self.routes,True,self)


    def configure(self, dispatcher):
        self.mapAllToFile(dispatcher)

class MouseModule:

    def __init__(self):
        import pyautogui
        self.userEventName = "OnlytoFunction"
        self.event = 0
        self.counter = 0
        self.size = pyautogui.size()

    def changeEventState(self):
        if self.event:
            self.event = 0
        else:
            self.event = 1
        return self.event

    def move(self,unused_addr,*args): #Thread millor opcio - Trobar un smooth movement i velocitat - Deadzone(Sobretot)
        import pyautogui

        pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
        pyautogui.PAUSE = 0
        mouseModule = args[0][0][0]

        def calculatex(x):
            return ((x)-(-51))*3.21
        try:
            print(args[1])
            print()
            if mouseModule.counter == 36:

                if args[1] < -50:
                    pyautogui.moveTo(None,0, duration=0.2)
                elif args[1] > 230:
                    pyautogui.moveTo(None,mouseModule.size[1]-1, duration=0.2)
                else:
                    pyautogui.moveTo(None,calculatex(args[1]), duration=0.2)
                mouseModule.counter = 0

            mouseModule.counter +=1

        except KeyboardInterrupt:
            print("Stop\n")

    def configure(self, dispatcher):
        dispatcher.mapPath("/muse/acc", self.move,False,self)



