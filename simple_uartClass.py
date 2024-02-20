from machine import UART
import json
from time import sleep_ms

class UartClass:
    #Remember to document this class
    
    def __init__(self, identifier, tx_pin, rx_pin):
        if (tx_pin == -1):
            self.uart = UART(identifier, 115200)
        else:
            self.uart = UART(identifier, 115200, tx = tx_pin, rx = rx_pin)
        
    def send_command(self, command : str):
        self.uart.write(command)
        
    def receive_command(self):
        receivedCommand = self.uart.read().decode("utf-8")
        return receivedCommand
    
if __name__ == "__main__":
    sender = UartClass(1,4,5)
    receiver = UartClass(2,13,14)
    
    while True:
        sender.send_command("start")
        sleep_ms(1000)
        message = receiver.receive_command()
        print(message)
    #Your code to test the class here
