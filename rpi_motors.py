from time import sleep
from machine import PWM, Pin


class Motor:

    def __init__(self, pin_fwd, pin_rvr):
        self.fwd = PWM(Pin(pin_fwd))
        self.fwd.freq(500)
        self.rvr = PWM(Pin(pin_rvr))
        self.rvr.freq(500)

    def rotate(self, power):
        if (power >= 0):
            self.fwd.duty_u16(int(power * 65535 / 100))
            self.rvr.duty_u16(0)
        else:
            self.rvr.duty_u16(int(-power * 65535 / 100))
            self.fwd.duty_u16(0)

    def stop(self):
        self.rotate(0)


'''
Motor interface.

        front
    M1  _____  M2
       |     |
       |     |
       |     |
    M4 |_____| M3
'''


class Car:
    m1 = Motor(12, 13)
    m2 = Motor(15, 14)
    m3 = Motor(17, 16)
    m4 = Motor(18, 19)

    motors = [m1, m2, m3, m4]

    def __init__(self):
        None

    def move(self, power):
        for i in range(4):
            self.motors[i].rotate(power)

    def move_side(self, power):  # positivo derecha
        self.motors[0].rotate(power)
        self.motors[1].rotate(-power)
        self.motors[2].rotate(power)
        self.motors[3].rotate(-power)

    def move_derecha(self, power):  # mover a la DERECHA
        self.motors[0].rotate(power)
        self.motors[1].rotate(power * 0.5)
        self.motors[2].rotate(power)
        self.motors[3].rotate(power * 0.5)

    def move_izq(self, power):  # mover a la IZQ
        self.motors[0].rotate(power * 0.5)
        self.motors[1].rotate(power)
        self.motors[2].rotate(power * 0.5)
        self.motors[3].rotate(power)

    def stop(self):
        self.move(0)

    def test(self):
        for i in range(4):
            # self.motors[i].rotate(100)
            # sleep(2)
            # self.motors[i].rotate(-100)
            # sleep(2)
            # self.motors[i].stop()
            # self.move_izq(75)
            # self.move(25)
            sleep(2)
            self.stop()
            self.move_izq(30)
            # self.move(100)
            sleep(2)
            self.stop()


if __name__ == "__main__":
    car = Car()
    car.test()


