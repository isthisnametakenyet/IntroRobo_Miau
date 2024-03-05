import bluetooth
from BLUTH import BLESimplePeripheral
import time
from machine import Pin
from example_uartClass import UartClass

class MiauClass:

    def __init__(self):

        ble = bluetooth.BLE()
        p = BLESimplePeripheral(ble)

        estado = 0
        stopped = False
        
        sender = UartClass(1,4,5)

        while (p.is_connected() == 0):
            time.sleep(0.1)

        while (1):
            if (p.on_read() == "Start"):
                    sender.send_command("start")
            if (p.on_read() == "Stop"):
                    sender.send_command("stop")

