#!/usr/bin/python

from guidisplay import *
from eegcontroler import *
from modules import *

# Def params amb MAP:
# unused_addr: El primer parametre no s'utilitze
# args: es la informació que t'arriba per OSC i els
# parametres adicionals que tu li fiquis (son una llista i estan a args[0])

def print_volume_handler(unused_addr,*args):

#Aditional parameters
    for x in range(0, len(args[0])):
        print(args[0][x])

#EEG DATA
    for x in range(1,len(args)):
        print(args[x])


if __name__ == "__main__":
    import pyautogui
    # TODO: Multiprocessing per cridar al script
    # TODO: Modul Mouse
    # TODO: Multidioma Arxiu clau-valor
    # TODO: Solucionar tema dels checkboxs (Seleccionar tots)
    # TODO: Fer un disseny millor dels Checkboxs
    # TODO: Millorar la pantalla del Dispatcher

    #selectModuleMenu()

    module = MouseModule()
    dispatcher = ModularDispatcher(module)
    controler = OSCcontroler(dispatcher)
    controler.buildServer()
    functionBindingtoWidget(controler,module)

