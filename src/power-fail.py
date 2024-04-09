#!/usr/bin/env python3

import signal
import sys
import time
import threading
import keyboard

try:
    import RPi.GPIO as GPIO
    isRasp = True
except:
    print("RPi.GPIO module not found. This code can only be run on a Raspberry Pi.")
    print("Executing example...")
    isRasp = False
    pass

BUTTON_GPIO = 16

def main():
    if(isRasp):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
                              callback=button_pressed_callback, bouncetime=100)

    else:
        # Inicia o thread para simular o evento de botão pressionado
        keyboard_thread = threading.Thread(target=simulate_button_pressed)
        keyboard_thread.start()

    # Configura o manipulador de sinal
    signal.signal(signal.SIGINT, signal_handler)

    # Aguarda o sinal de interrupção
    signal.pause()

def signal_handler(sig, frame):
    if(isRasp):
        GPIO.cleanup()
    sys.exit(0)

def simulate_button_pressed():
    while True:
        char = sys.stdin.read(1)
        if (char=="\n"):
            button_pressed_callback(BUTTON_GPIO)

def button_pressed_callback(channel):
    print("Interrupção gerada")

if __name__ == '__main__':
    main()
