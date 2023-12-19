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
        
    def __init__(self, identifier, tx_pin, rx_pin):
        """UartClass constructor
        
        During initialization the class creates a UART and launches the
        listenning thread.
        
        Args:
            identifier (int): UART to use. ESP32 provides 0,1 and 2.
                              0 is not recommended. RPI recommended 0.
            tx_pin (int): Pin number that will be transmiting data
            rx_pin (int): Pin number that will be receiving data

        """
        self.flag_start = False
        self.flag_stop = False
        self.uart = UART(identifier, 115200, tx = tx_pin, rx = rx_pin)
        
        _thread.start_new_thread(self.__listener, ())
        sleep_ms(1000)
        
        
    
        
        
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
            #print(line)
            if(line != None):
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
    sender = UartClass(1,4,5)
    receiver = UartClass(2,13,14)
    
    while True:
        if(receiver.is_started() == True):
            print("Start")
        sender.send_command("start")
        sleep_ms(1000)
    

