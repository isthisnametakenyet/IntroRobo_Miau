from rpi_motors import Car
from servo import Servo
from ultra import Ultra
from machine import Pin
from tracker import track
from uart import UartClass

class MiauClass:
    
    def __init__(self):

        ultra_sensor = Ultra(3, 2, 10000)  # pines a decidir/buscar

        tracker0 = track(4)
        tracker1 = track(5) # num to change
        tracker2 = track(6) # num to change
        
        servo = Servo(7)

        car = Car()
        
        receiver = UartClass(1,-1,-1)

        estado = 0
        moved = 0
        stopped = False
        prev_estado = 0
        
        tiempo_sidemove = 0.25
        tiempo_forwardmove = 3
        led=Pin(2,Pin.OUT)

        while 1:
            print("estado: " + str(estado))

            if receiver.is_stop:
                    # nos guardamos en el código que hemos parado
                    prev_estado = estado
                    stopped = True
                    # volvemos a un estado esperando a que empecemos
                    estado = 0
            if estado == 0 :
                # esperamos a que recibamos un start para comenzar el código
                if receiver.is_started:
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
                if distance > 20:
                    estado = 2  # nos movemos adelante sin problemas mirando la línea
                else:
                    estado = 3 # hemos encontrado el objeto procedemos a activar protocolo de esquivaje de objeto
                #blink led T=1s
                switchLedValue(led,0.5)
            elif estado == 2:
                if tracker0.on_track() or tracker1.on_track() or tracker2.on_track():
                    # si aún no hemos llegado al final de la línea seguirla
                    if tracker1.on_track() == 1:
                        car.move_izq(50)
                    elif tracker0.on_track() == 1:
                        car.move(50)  # Move forward
                    elif tracker2.on_track() == 1:
                        car.move_derecha(50)

                    time.sleep(tiempo_sidemove)  # sujeto a cambios tiempo que sigue para adelante
                    car.stop()
                    estado = 1
                else: # si hemos llegado a la línea final
                    estado = 6
                #blink led T=0.2s
                switchLedValue(led,0.1)
            elif estado == 3:
                # Nos movemos hacia la derecha hasta que no detectamos
                # el objeto
                car.move_side_derecha(50)
                time.sleep(tiempo_sidemove)
                car.stop()
                distance = ultra_sensor.distance_cm()
                moved += 1
                if distance > 50:
                    estado = 4
                #led ON
                led.value(1)
            elif estado == 4:
                # nos movemos hacia delante durante 3s pensando que rodearemos
                # el objeto
                car.move(50)
                time.sleep(tiempo_forwardmove)
                car.stop()
                estado = 5
                led.value(0)
            elif estado == 5:
                # volvemos al estado original al que estuvimos
                # moviendonos a la izquierda
                car.move_side_izquierda(50)
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
                led.value(0)
            elif estado == 6:
                car.stop()
            else:
                    print("ERORR")
        

    def switchLedValue(self, led, blink):
        if(1 == led.value()):
            led.value(0)
        else:
            led.value(1)
        time.sleep(blink)    
    
