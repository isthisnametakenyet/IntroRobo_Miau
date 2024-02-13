import bluetooth
from BLUTH import BLESimplePeripheral
import time
from servo import Servo
from ultra import Ultra
from machine import Pin
from tracker import track


# from uart import UartClass

class MiauClass:

    def __init__(self):

        ble = bluetooth.BLE()
        p = BLESimplePeripheral(ble)

        servo = Servo(14)
        led = Pin(2, Pin.OUT)

        tracker0 = track(13)
        tracker1 = track(12)  # num to change
        tracker2 = track(27)  # num to change

        estado = 0

        while (p.is_connected() == 0):
            time.sleep(0.1)

        while (1):
            if estado == 0:
                if (p.on_read() == "Start"):
                    estado = 1
            elif estado == 1:
                servo.move(90)
                self.switchLedValue(led, 0.5)
                if (p.on_read() == "Stop"):
                    estado = 0
                elif (tracker0.on_track() == 1 or tracker1.on_track() == 1 or tracker2.on_track() == 1):
                    estado = 2
            elif estado == 2:
                self.switchLedValue(led, 0.1)

                print("ERORR")
            elif estado == 3:
                print("ERORR")
            else:
                print("ERORR")

    def switchLedValue(self, led, blink):
        if (1 == led.value()):
            led.value(0)
        else:
            led.value(1)
        time.sleep(blink)

