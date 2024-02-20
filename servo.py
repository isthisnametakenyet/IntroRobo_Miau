from machine import Pin, PWM
import time


class Servo:
    """A class used to simplify and use the Servo Motor
        This class will initialize the angles and frequencies the servo needs to move smoothly.
        
    """
    __servo_pwm_freq = 50
    __min_u10_duty = 26 - 0 # offset for correction
    __max_u10_duty = 123- 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001
    

    def __init__(self, pin):
        """UartClass constructor
        It initialize the Pin
        """
        self.__initialise(pin)


    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        """ Round the decimal (2 places) for adjusting. We check if we need to move or stay the same and calculate the
        new duty cycle
        """
        angle = round(angle, 2)
        if angle == self.current_angle:
            return
        self.current_angle = angle
        duty_u10 = self.__angle_to_u10_duty(angle)
        self.__motor.duty(duty_u10)

    def __angle_to_u10_duty(self, angle):
        """Calculates the angle depending on the duty and the conversion angle
        """
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty


    def __initialise(self, pin):
        """ Creates a PWM which is send to the pin.
        """
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)
        
        
    if __name__  == "__main__":
        """Nominal behaviour test for servo implementation
        Two instances of the Servo class and one instances from library time is used to test the code and implementation.
        The expected behaviour is moving the servo from 0 degrees to 180, which we accomplished by adding 5 to the angle until is 180,
        in this case the servo returns to 0 degrees.
        
          Wiring:
        pin 12

        """
        
        motor = Servo(12)
        angulo = 0
        while(1):
            motor.move(angulo) # tourne le servo à 0°
            angulo = angulo + 5
            time.sleep(0.1)
        
            if(angulo >= 180):
                angulo = 0 