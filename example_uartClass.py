from machine import UART
import json
from time import sleep_ms
import _thread

class UartClass:
    """A class used to simplify and use the micropython UART
    
    The UartClass has been used in the subject of "Introducció a la Robotica"
    as an example of the expected results. For further reference on how to
    document a class check:
    https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    
    Aditionally to the documentation, this example class will keep the length
    of lines in the code under 80 characters, as it is a well known good
    practice to keep code readable.
    
    This class will initialize a micropython UART with a fixed boudrate.
    It offers a writing interface in the function send_command() and a
    listening thread on the background that will update flag_start and
    flag_stop upon receiving a "start" or "stop" message.
    
    Internally the messages are sent using the JSON format as it will improve
    scalability of the class. Messages after parsing are stored in a dictionary
    that can be accessed by name of the field instead of by index.
    

    Attributes
    ----------
    flag_start (bool): flag used to record if the listening thread received a
                       start message
    flag_stop (bool): flag used to record if the listening thread received a
                      stop message

    """
        
    def __init__(self, identifier, tx_pin=-1, rx_pin=-1):
        """UartClass constructor
        
        During initialization the class creates a UART and launches the
        listenning thread.
        
        Args:
            identifier (int): UART to use. ESP32 provides 0,1 and 2.
                              0 is not recommended. RPI recommended 0.
            tx_pin (int): Pin number that will be transmiting data
            rx_pin (int): Pin number that will be receiving data

        """
        self.lcd = None
        
        self.flag_start = False
        self.flag_stop = False
        
        if (tx_pin!=-1 and rx_pin!=-1):
            self.uart = UART(identifier, 115200, tx = tx_pin, rx = rx_pin)
        else:
            self.uart = UART(identifier, 115200)
            
        
        _thread.start_new_thread(self.__listener, ())
        sleep_ms(200)
        
        
    def set_lcd(seld, lcd):
        """This function sets an lcd output for the uartClass
        
        This function will set a lcd display for the uartClass to report the
        messages it receives. If it is not set the class won't try to print
        
        Args:
            lcd (LCD): instance of a LCD class already initialized for use.

        """
        self.lcd = lcd        
        self.lcd.puts("LCD - UART OK",1,0)
        
        
    def send_command(self, command : str):
        """This function will send the introduced command

        This function will build a JSON object, fill it with the desired
        information (as of now, only the command), then it will dump the
        structure in a string and send it through the UART.
        
        As this is meant to be a multipurpose class the command values are not
        checked.
        
        Args:
            command (string): String holding the command that will be sent.
            
        """
        obj = {}
        obj['command'] = command;
        json_str = json.dumps(obj) + "\r\n"
        self.uart.write(json_str)
        print("--sending: " + json_str)
        
    
    def __listener(self):
        """Listening thread main function.
        
        This function is launched as a thread by the class constructor.
        Periodically it checks if a new message has been received, parses it
        and updates the status flags {flag_start, flag_stop} acordingly.
        
        """
        while True:
            line = self.uart.readline()
            if(line != None):
                if (self.lcd!=None):
                    self.lcd.puts("                ", 0,0)	#clear line
                    self.lcd.puts(line, 0,0)
                else:
                    print(line)
                try:
                    obj = json.loads(line)
                    if('command' in obj):
                        if obj['command'] == 'start':
                            self.flag_start = True
                        if obj['command'] == 'stop':
                            self.flag_stop = True
                        if obj['command'] == 'move':
                            None
                except:
                    None
            sleep_ms(100)
        
        
    def is_started(self):
        """Checks if a start message has been received.
        
        This function will check if a start message was received and set the
        internal flag flag_start back to false. This way each reading will
        return True once for each received message.
        
        Return:
            bool: True for new start message received, false otherwise
        
        """
        if(self.flag_start == True):
            self.flag_start = False
            return True
        return False


    def is_stop(self):
        """Checks if a stop message has been received.
        
        This function will check if a stop message was received and set the
        internal flag flag_stop back to false. This way each reading will
        return True once for each received message.
        
        Return:
            bool: True for new stop message received, false otherwise
        
        """
        if(self.flag_stop == True):
            self.flag_stop = False
            return True
        return False
    
        
def uartClass_receive_test():
    """Nominal behaviour test for UartClass listener on Rasberry Pi Pico

    An instance is created for the UART 0 in the Raspberry Pi Pico with the
    default values for the pins.
    
    """
    comms = UartClass(0)
    while True:
        if(comms.is_started() == True):
            print("Start")
        sleep_ms(1000)
    
def uartClass_singleBoard_test():
    """Nominal behaviour test for UartClass implementation

    Two instances of the UartClass will be created in the same board to
    validate writing and reading work.
    The expected behaviour is sender UART sending a message every 1 second
    and receiver UART reading it with a short delay.
    
    Wiring:
        pin 4 --- pin 14
        pin 5 --- pin 13

    """
    sender = UartClass(1,4,5)
    receiver = UartClass(2,13,14)
    
    while True:
        if(receiver.is_started() == True):
            print("Start")
        sender.send_command("start")
        sleep_ms(1000)
        
        
if __name__ == "__main__":
    uartClass_receive_test()