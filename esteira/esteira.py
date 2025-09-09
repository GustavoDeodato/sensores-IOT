from machine import Pin, time_pulse_us
import time


PINO_TRIG = d4
PINO_ECHO = d18
PINO_LED_INTRUSO = d15

trig = Pin(PINO_TRIG, Pin.OUT)
echo = Pin(PINO_ECHO, Pin.IN)
led_intruso = Pin(PINO_LED_INTRUSO, Pin.OUT)


contador_itens = 0
contador_caixas = 0
distancia_limite = 10  
detectar_ativo = False  


def obter_distancia():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duracao = time_pulse_us(echo, 1, 30000)
    if duracao < 0:  
        return 1000  
    distancia = (duracao / 2) * 0.0343
    return distancia


while True:
    dist = obter_distancia()
    print("Distância:", dist, "cm")

    if dist <= distancia_limite:
        led_intruso.value(1)  

        if not detectar_ativo:
            contador_itens += 1
            detectar_ativo = True
            print("Item detectado! Total de itens:", contador_itens)

            
            if contador_itens >= 10:
                contador_caixas += 1
                contador_itens = 0  
                print("Caixa completa! Total de caixas:", contador_caixas)

        time.sleep(1)  

    else:
        led_intruso.value(0)  
        detectar_ativo = False  

    time.sleep(0.5)