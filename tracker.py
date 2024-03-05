from machine import Pin, ADC
import time
 
 
class track:
    """A class used to simplify and use the Track Sensor
            This class will initialize the pin and get the values that that
            sensor is catching.
    """
    def __init__(self, pin):
        """track constructor
                It initializes the Pin of the Track Sensor
        """
        self.ldr_pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        
    def on_track(self):
        #if (self.get_light_percentage() < 25):
        #    return 1
        #else:
        #    return 0
        
        if self.ldr_pin.value() == 0:
            #print("line present")
            return 0
        else:
            #print("No line present")
            return 1
 
#ldr = track(27)

#while True:
 #    print(ldr.get_light_percentage())
  #   time.sleep(1)

if __name__ == "__main__":
    """Nominal behavior test for track sensor implementation.
       An instance of the track class is created with a 
       specified pin, and the raw and percentage light 
       values are printed in a loop.
        
        Wiring:
        pin 18
    """
    ldr_sensor = track(6)

    while True:
        ldr_sensor.on_track()

        time.sleep(1)
