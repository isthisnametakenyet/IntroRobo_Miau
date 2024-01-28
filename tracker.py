from machine import Pin
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
        self.ldr_pin = machine.ADC(Pin(pin))
        
    def get_raw_value(self):
        """ Gets the raw value from the sensor, and it passes
                though the value to the user reading the analog value from an ADC
                pin associated with an LDR Sensor.
        """
        return self.ldr_pin.read_u16()
    
    def get_light_percentage(self):
        """Calculates and returns the light percentage based on the raw analog value obtained
               from the LDR sensor. The raw value is normalized to a percentage scale (0-100),
               where 0 represents minimum light and 100 represents maximum light.
        """
        return round(self.get_raw_value()/65535*100,2)
 
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
    ldr_sensor = track(18)

    while True:
        raw_value = ldr_sensor.get_raw_value()
        light_percentage = ldr_sensor.get_light_percentage()

        print(f"Raw Value: {raw_value}, Light Percentage: {light_percentage}%")

        time.sleep(1)