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

modules = ["ExperimentalModule","MouseModule"]

class printModule:

    def __init__(self):
        pass

    def mapAllForPrint(self,dispatcher,function=print):
        dispatcher.mapSameFunctionToPaths(function, routes)

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
        expModule.fd.write(str(time)+','+osc_path+","+values+","+ str(expModule.userEventName) +","+ str(expModule.event) + '\n')
        print(str(time)+','+osc_path+","+values+","+ str(expModule.userEventName) +","+ str(expModule.event) + '\n')


    def mapAllToFile(self,dispatcher,function=saveResults):
        dispatcher.mapSameFunctionToPaths(function,self.routes,True,self)


    def configure(self, dispatcher):
        self.mapAllToFile(dispatcher)

class MouseModule:

    def __init__(self):
        import datetime
        self.x = 0
        self.y = 0
        self.userEventName = "Reinicia"
        self.event = 0
        self.counter = 0
        self.referenced = 0
        self.ignore = 0
        self.timeReference = datetime.datetime.now()
        self.blinkCounter = 0
        self.deadzone = 40
        self.signalRec = 10
        self.blinkNumb = 4
        self.blinkInterval = 1

    def getDeadzone(self):
        return self.deadzone

    def getSignalRec(self):
        return self.signalRec

    def getBlinkNumb(self):
        return self.blinkNumb

    def getBlinkInterval(self):
        return self.blinkInterval

    def setDeadzone(self,deadzone):
        self.deadzone = deadzone

    def setSignalRec(self,signalRec):
        self.signalRec = signalRec

    def setBlinkNumb(self,blinkNumb):
        self.blinkNumb = blinkNumb

    def setBlinkInterval(self,blinkInterval):
        self.blinkInterval = blinkInterval

    def changeEventState(self):
        if self.event:
            self.event = 0
        else:
            self.event = 1
        self.counter = 0
        return self.event

    def calculatey(self,y):
        if y < self.y - self.deadzone:
            return -10
        elif y > self.y + self.deadzone:
            return 10
        else:
            return 0

    def calculatex(self,x):
        if x < self.x - self.deadzone:
            return 10
        elif x > self.x + self.deadzone:
            return -10
        else:
            return 0


    def calculateStop(self,x, y):
        if self.deadzone + self.y >= y and self.y - self.deadzone <= y and self.deadzone + self.x >= x and self.x - self.deadzone <= x:
            return True
        else:
            return False

    def move(self,unused_addr,*args):
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        mouseModule = args[0][0][0]

        if mouseModule.event:
            if mouseModule.referenced:
                try:
                    if mouseModule.counter == self.signalRec:
                        if mouseModule.calculateStop(args[3],args[1]):
                            pass
                        else:
                            pyautogui.moveRel(mouseModule.calculatex(args[3]),mouseModule.calculatey(args[1]), duration=0.1)
                        mouseModule.counter = 0

                    mouseModule.counter +=1

                except KeyboardInterrupt:
                    print("Stop\n")
            else:
                mouseModule.x,mouseModule.y = args[3],args[1]
                mouseModule.referenced = 1
        else:
            if mouseModule.counter == 30:
                #print("RefY:" + str(args[1]))
                #print("RefX:" + str(args[3]))
                mouseModule.counter = 0
            mouseModule.counter+=1

    def click(self, unused_addr, *args):
        import pyautogui
        mouseModule = args[0][0][0]

        if mouseModule.referenced:

            if mouseModule.ignore == 0 or mouseModule.ignore >= 5:
                if args[1] and mouseModule.ignore == 0:
                    pyautogui.click()
                    mouseModule.ignore += 1
                elif args[1] and 10 >= mouseModule.ignore >= 5:
                    pyautogui.doubleClick()
                else:
                    mouseModule.ignore = 0
            else:
                mouseModule.ignore+=1
        else:
            print("LeftC: " + str(args[1]))


    def blink(self,unused_addr,*args):
        import datetime
        import pyautogui
        mouseModule = args[0][0][0]


        if mouseModule.referenced:
            if args[1]:
                mouseModule.blinkCounter += 1

                now = datetime.datetime.now()
                elapsedTime = now - mouseModule.timeReference
                elapsedTime = divmod(elapsedTime.total_seconds(),1)[0]

                if elapsedTime <= self.blinkInterval:
                    if mouseModule.blinkCounter == self.blinkNumb:
                        print("BlinkC: " + str(mouseModule.blinkCounter))
                        print("BlinkN: " + str(self.blinkNumb))
                        pyautogui.rightClick()
                        mouseModule.timeReference = datetime.datetime.now()
                        mouseModule.blinkCounter = 0
                else:
                    mouseModule.timeReference = datetime.datetime.now()
                    mouseModule.blinkCounter = 0
        else:
            print("RightC: " + str(args[1]))

    def configure(self, dispatcher):
        dispatcher.mapPath("/muse/elements/jaw_clench",self.click,False,self)
        dispatcher.mapPath("/muse/acc",self.move,False,self)
        dispatcher.mapPath("/muse/elements/blink",self.blink, False, self)



