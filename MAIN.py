import bluetooth
from BLUTH import BLESimplePeripheral
import time
from servo import Servo
from ultra import Ultra
from uart import UartClass

if __name__ == "__main__":
    #motor = Servo(14)
    #angulo = 0
    #while(1):
        #motor.move(angulo) # tourne le servo à 0°
        #angulo = angulo + 5
        #time.sleep(0.1)
        
        #if(angulo >= 180):
            #angulo = 0

    

    #sensor = Ultra(5,18,10000)
    #while(1):
            
    #    distance = sensor.distance_cm()
    #    print('Distance:', distance, 'cm')
    #    time.sleep(2)

    #touch = Touch(14)

    #while(1):
    #    print('Tocado: ', touch.isTouched())
    #    time.sleep(1)


    

    #ble = bluetooth.BLE()
    #p = BLESimplePeripheral(ble)

    #def on_rx(rx_data):
        #print("RX", rx_data)

    #p.on_write(on_rx)

    #print("Please use LightBlue to connect to ESP32.")

    #while True:
        #if p.is_connected():
            # Short burst of queued notifications.
            #tx_data = input("Enter anything: ")
            #print("Send: ", tx_data)
            #p.send(tx_data)



    motor = Servo(12)
    angulo=90
    sensor = Ultra(18,19,10000)
    while(1):
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        time.sleep(0.1)
        flag=1
        if (distance <= 50): #&& flag):
            motor.move(angulo) # tourne le servo à 0°
            flag=0
        elif(distance > 0):
            motor.move(0)
        
        
        
        
        
        #lo de la uart
        sender= UartClass(1,4,5)
        receiver=UartClass(2,13,14)
