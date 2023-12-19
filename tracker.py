from machine import Pin
import time
 
 
class track:
    def __init__(self, pin):
        self.ldr_pin = machine.ADC(Pin(pin))
        
    def get_raw_value(self):
        return self.ldr_pin.read_u16()
    
    def get_light_percentage(self):
        return round(self.get_raw_value()/65535*100,2)
 
#ldr = track(27)

#while True:
 #    print(ldr.get_light_percentage())
  #   time.sleep(1)