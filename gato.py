from rpi_motors import Car
from servo import Servo
from ultra import Ultra
from machine import Pin
from tracker import track
from example_uartClass import UartClass
import time
#from simple_uartClass import UartClass

class MiauClass:
    
    def __init__(self):

        ultra_sensor = Ultra(3,2,10000)  # pines a decidir/buscar

        tracker0 = track(5)
        tracker1 = track(4) # num to change
        tracker2 = track(6) # num to change
        
        servo = Servo(7)

        car = Car()
        
        receiver = UartClass(0,-1,-1)

        estado = 1
        moved = 0
        stopped = False
        prev_estado = 0
        prev_move = 0

        tiempo_sidemove = 0.2
        tiempo_forwardmove = 0.2
        #led=Pin(2,Pin.OUT)

        while 1:
            print("estado: " + str(estado))
            #message = receiver.receive_command()
            #print("Message: " + message)

            if receiver.is_stop():
                print("Stop StateMachine")
                # nos guardamos en el código que hemos parado
                prev_estado = estado
                stopped = True
                # volvemos a un estado esperando a que empecemos
                estado = 0
            if estado == 0 :
                # esperamos a que recibamos un start para comenzar el código
                if receiver.is_started():
                    print("Start StateMachine")
                    # si es la primera vez que se ejecuta seguir la línea
                    if not stopped:
                        estado = 1
                    # si hemos parado la ejecución continuar con la anterior
                    else:
                        # cargamos estado anterior
                        estado = prev_estado
                        # borramos la información anterior del estado
                        prev_estado = 0
                        stopped = False
            elif estado == 1:
                #check if there's something ahead
                distance = ultra_sensor.distance_cm()
                print('Distance:', distance, 'cm')
                if distance < 0 or distance > 20:
                    estado = 2  # nos movemos adelante sin problemas mirando la línea
                else:
                    estado = 3 # hemos encontrado el objeto procedemos a activar protocolo de esquivaje de objeto
                #blink led T=1s
                #switchLedValue(led,0.5) #isn't defined
            elif estado == 2:
                time.sleep(0.5)
                if tracker0.on_track() and tracker1.on_track() and tracker2.on_track(): # si hemos llegado a la línea final
                    estado = 8
                elif tracker0.on_track() or tracker1.on_track() or tracker2.on_track():
                    # si aún no hemos llegado al final de la línea seguirla
                    if tracker0.on_track():
                        car.move(30) # Move forward
                        print("forward")
                    elif tracker1.on_track():
                        car.move_izq(30)
                        print("izq")
                        prev_move = 2
                    elif tracker2.on_track():
                        car.move_derecha(30)
                        print("der")
                        prev_move = 1
                    time.sleep(tiempo_sidemove)  # sujeto a cambios tiempo que sigue para adelante
                    car.stop()
                    estado = 1
                else:
                    estado = 7# 7
                #blink led T=0.2s
                #switchLedValue(led,0.1)
            elif estado == 3:
                # Nos movemos hacia la derecha hasta que no detectamos
                # el objeto
                car.move_side_derecha(30)
                time.sleep(tiempo_sidemove)
                car.stop()
                distance = ultra_sensor.distance_cm()
                moved += 1
                if distance > 50:
                    estado = 4
                #led ON
                #led.value(1)
            elif estado == 4: # llega un momento donde no lo vemos pero sigue habiendo caja
                car.move_side_derecha(30)
                time.sleep(tiempo_sidemove)
                car.stop()
                moved += 1
                estado = 5
            elif estado == 5:
                # nos movemos hacia delante durante 3s pensando que rodearemos
                # el objeto
                car.move(30)
                time.sleep(tiempo_forwardmove)
                car.stop()
                estado = 6
                #led.value(0)
            elif estado == 6:
                # volvemos al estado original al que estuvimos
                # moviendonos a la izquierda
                car.move_side_izquierda(30)
                time.sleep(tiempo_sidemove)
                car.stop()
                moved -= 1
                # miramos por si de casualidad hemos encontrado la línea
                if tracker0.on_track() or tracker1.on_track() or tracker2.on_track():
                    moved = 0
                    estado = 2 # seguimos el procedimiento de seguir a la línea
                # si hemos vuelto a nuestro lugar original según la variable
                elif moved == 0:
                    estado = 2# Return to initial state
                #.led.value(0)
            elif estado == 7: # si hemos llegado (teoricamente a la línea)
                if  prev_move == 0:
                    car.move(30) # Move forward
                    prev_move = 0
                    print("forward")
                elif prev_move == 1:
                    car.move_izq(30)
                    print("izq")
                    prev_move = 1
                elif prev_move == 2:
                    car.move_derecha(30)
                    print("der")
                    prev_move = 2
                time.sleep(tiempo_sidemove)  # sujeto a cambios tiempo que sigue para adelante
                car.stop()
                estado = 1
            elif estado == 8:
                # si sigue siendo la línea blanca es que NO hemos acabado
                if tracker0.on_track() or tracker1.on_track() or tracker2.on_track():
                    estado = 2
                # si encontramos negro hemos llegado
                else:
                    estado = 9
            elif estado == 9: # si hemos llegado (teoricamente a la línea)
                car.stop()
                break
            else:
                print("ERORR")
    # mirar el problema de que tenemos que movernos una vez más a la izquierda 
    

if __name__  == "__main__":
    gato = MiauClass()

