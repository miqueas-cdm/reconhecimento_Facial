from machine import Pin
import sys
import select
import time

led = Pin(15, Pin.OUT)

print("Aguardando comandos....")

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        comando = sys.stdin.readline().strip().upper()
        
        print("Recebido: ", comando)
        
        if comando == "OK":
            led.on()
            print("LED LIGADO")
            
        elif comando == "OFF":
            led.off()
            print("LED DESLIGADO")
            
    time.sleep(0.1)