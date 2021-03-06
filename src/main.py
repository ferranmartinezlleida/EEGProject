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
    # TODO: Multiprocessing per cridar al script
    # TODO: ACONSEGUIR LIVE GRAPH DISPLAY
    # TODO: Override Mouse
    # TODO: Multidioma Arxiu clau-valor
    # TODO: Fer funcio que canvii 0 a 1 i k es guardi al fitxer de sessio com a event
    # https://www.youtube.com/watch?v=BRagbwst5I4

    printMod = printModule()
    dispatcher = ModularDispatcher(printMod)

    controler = OSCcontroler(dispatcher)
    controler.buildServer()

    functionBindingtoWidget(controler)
