import time
import machine
from PiicoDev_Servo import PiicoDev_Servo, PiicoDev_Servo_Driver
from rfid import MFRC522
controller = PiicoDev_Servo_Driver()
servo = PiicoDev_Servo(controller, 1)

doorbell = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
doorbell_last = time.ticks_ms()
light = machine.Pin(1, machine.Pin.OUT)
light.on()
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

def activate_servo():
    global servo
    
    servo.angle = 0
    time.sleep(5)
    servo.angle = 90
    time.sleep(1)
    

def button_handler(pin):
    global doorbell, doorbell_last
      
    if pin is doorbell:
        if time.ticks_diff(time.ticks_ms(), doorbell_last) > 500:
            print("Triggered")
            light.off()
            activate_servo()
            light.on()
    doorbell_last = time.ticks_ms()        




 
 
while True:
    known_cards = [1483934330]
    doorbell.irq(trigger = machine.Pin.IRQ_RISING, handler = button_handler)
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            
            if card in known_cards:
                print("Card ID: "+ str(card)+" PASS: Green Light Activated")
                light.off()
                activate_servo()
                light.on()
                
                
            else:
                print("Card ID: "+ str(card)+" UNKNOWN CARD! Red Light Activated")
                for x in range(0,5):
                    light.off()
                    time.sleep_ms(200)
                    light.on()
                    time.sleep_ms(200)
    # time.sleep_ms(2500)
