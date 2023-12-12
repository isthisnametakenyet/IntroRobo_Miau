from machine import uart


Class UartClass:
    
    def __init__(self,tx_pin,rx_pin):
        self.uart=UART(1,115200,tx=tx_pin,rx=rx_pin)
    
    def sendCommand(self,command):
        self.uart.write(command)
    
    def read_command(self):
        return self.uart.read()

        