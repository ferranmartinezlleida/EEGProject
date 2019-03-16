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
        self.userEventName = "GetReference"
        self.event = 0
        self.counter = 0
        self.referenced = 0
        self.x = 0
        self.y = 0

    def changeEventState(self):
        if self.event:
            self.event = 0
        else:
            self.event = 1
        self.counter = 0
        return self.event

    def move(self,unused_addr,*args): #Thread millor opcio - Trobar un smooth movement i velocitat - Deadzone(Sobretot)
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        mouseModule = args[0][0][0]

        def calculatey(y):
            if y < mouseModule.y - 60:
                return -10
            elif y > mouseModule.y + 60:
                return 10
            else:
                return 0

        def calculatex(x):
            if x < mouseModule.x - 25:
                return 10
            elif x > mouseModule.x + 25:
                return -10
            else:
                return 0

        def calculateStop(x,y):
            if 60 + mouseModule.y >= y and mouseModule.y -60 <= y and 25 + mouseModule.x >= x and mouseModule.x - 25 <= x:
                return True
            else:
                return False
        if mouseModule.event:
            if mouseModule.referenced:

                try:
                    if mouseModule.counter == 15:
                        print("X:")
                        print(args[3])
                        print("Y:")
                        print(args[1])
                        if calculateStop(args[3],args[1]):
                            pass
                        else:
                            pyautogui.moveRel(calculatex(args[3]),calculatey(args[1]), duration=0.1)
                        mouseModule.counter = 0

                    mouseModule.counter +=1

                except KeyboardInterrupt:
                    print("Stop\n")
            else:
                print("RefY:")
                print(args[1])
                print("RefX:")
                print(args[3])
                mouseModule.x,mouseModule.y = args[3],args[1]
                mouseModule.referenced = 1
        else:
            if mouseModule.counter == 40:
                print("RefY:" + str(args[1]))
                print("RefX:" + str(args[3]))
                mouseModule.counter = 0
            mouseModule.counter+=1

    def configure(self, dispatcher):
        dispatcher.mapPath("/muse/acc", self.move,False,self)



