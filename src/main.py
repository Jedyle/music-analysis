from interface import *

#main method
itf = Interface()
loop = True
#main loop
while(loop):
    itf.update_screen()
    loop = itf.event_handler()
            
