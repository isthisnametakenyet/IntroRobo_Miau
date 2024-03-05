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
        
    def get_raw_value(self):
        """ Gets the raw value from the sensor, and it passes
                though the value to the user reading the analog value from an ADC
                pin associated with an LDR Sensor.
        """
        #return self.ldr_pin.read_u16()
        return self.ldr_pin

    
    def get_light_percentage(self):
        """Calculates and returns the light percentage based on the raw analog value obtained
               from the LDR sensor. The raw value is normalized to a percentage scale (0-100),
               where 0 represents minimum light and 100 represents maximum light.
        """
        #print("ldr_pin: " + str(self.ldr_pin))
        #print("raw_value: " + str(self.get_raw_value()))

        return round(self.get_raw_value()/65535*100,2)
    
    def on_track(self):
        #if (self.get_light_percentage() < 25):
        #    return 1
        #else:
        #    return 0
        print(self.get_light_percentage())
        if (self.get_light_percentage()):
            return 1
        else:
            return 0
 

if __name__ == "__main__":
    """Nominal behavior test for track sensor implementation.
       An instance of the track class is created with a 
       specified pin, and the raw and percentage light 
       values are printed in a loop.
        
        Wiring:
        pin 4
        pin 5
        pin 6

    """
    ldr_sensor1 = track(4)
    ldr_sensor2 = track(5)
    ldr_sensor3 = track(6)


    while True:
        raw_value1 = ldr_sensor1.get_raw_value()
        light_percentage1 = ldr_sensor1.get_light_percentage()
        raw_value2 = ldr_sensor2.get_raw_value()
        light_percentage2 = ldr_sensor2.get_light_percentage()
        raw_value3 = ldr_sensor3.get_raw_value()
        light_percentage3 = ldr_sensor3.get_light_percentage()

        print(f"Raw Value1: {raw_value1}, Light Percentage1: {light_percentage1}%")
        print(f"Raw Value2: {raw_value2}, Light Percentage2: {light_percentage2}%")
        print(f"Raw Value3: {raw_value3}, Light Percentage3: {light_percentage3}%")

        time.sleep(1)

