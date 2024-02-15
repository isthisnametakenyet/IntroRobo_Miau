import bluetooth
from BLUTH import BLESimplePeripheral
import time
from servo import Servo
from ultra import Ultra
from machine import Pin
from tracker import track
from uart import UartClass


# from uart import UartClass

class MiauClass:

    def __init__(self):

        ble = bluetooth.BLE()
        p = BLESimplePeripheral(ble)

        servo = Servo(14)
        led = Pin(2, Pin.OUT)
        sender = UartClass(1,4,5)
        receiver = UartClass(2,13,14)


        tracker0 = track(13)
        tracker1 = track(12)  # num to change
        tracker2 = track(27)  # num to change

        estado = 0

        while (p.is_connected() == 0):
            time.sleep(0.1)

        while (1):
            if estado == 0:
                if (p.on_read() == "Start"):
                    sender.send_command("start")
                    estado = 1
                    
            elif estado == 1:
                if (p.on_read() == "Stop"):
                    sender.send_command("stop")
                    estado = 0
            else:
                print("ERORR")

    def switchLedValue(self, led, blink):
        if (1 == led.value()):
            led.value(0)
        else:
            led.value(1)
        time.sleep(blink)

