from uart import UartClass
from machine import Pin
from time import sleep_ms


if __name__ == "__main__":
    """Nominal behaviour test for UartClass implementation

    Two instances of the UartClass will be created in the same board to
    validate writing and reading work.
    The expected behaviour is sender UART sending a message every 1 second
    and receiver UART reading it with a short delay.
    
    Wiring:
        pin 4 --- pin 14
        pin 5 --- pin 13

    """
    #sender = UartClass(1,4,5)
    receiver = UartClass(0, -1, -1)
    
    while True:
        if(receiver.is_started() == True):
            print("Start")
        #sender.send_command("start")
        sleep_ms(1000)