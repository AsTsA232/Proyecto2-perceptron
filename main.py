from lib.bmp280 import BMP280
import lib.ssd1306
import machine
from machine import I2C, Pin, SoftI2C
import time

#pesos para los perceptrones
peso1=-1.41
b1=0.22999999999999993
peso2=0.26
b2=-0.07000000000000015

#funcion de activacion
def act (peso,x1,b):
    z=peso * x1
    sumatoria=z+b
    
    if sumatoria>0:
        return 1
    else:
        return 0
    
#funcion valores normales
def norm (e1,e2):
    if (e1==0 and e2==0):
        return 1
    else:
        return 0
    
    
#INICIALIZACION DE PANTALLA
bus = SoftI2C(scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = lib.ssd1306.SSD1306_I2C(oled_width, oled_height, bus)
devices = bus.scan()
if devices:
    print('Pantalla encontrada en la direccion', devices)
    oled.text("INICIANDO...", 20, 30)
    oled.show()
    time.sleep(3)
else:
    print('No se encontraron dispositivos I2C')


#INICIALIZACION DEL SENSOR HUMEDAD Y TEMPERATURA
i2c = I2C(0, scl=Pin(1), sda=Pin(0),freq=40000)  
bmp = BMP280(i2c)
bmp.normal_measure()

#LEDS DE SALIDA
led_r=machine.Pin(13,machine.Pin.OUT)
led_v=machine.Pin(14,machine.Pin.OUT)
led_b=machine.Pin(15,machine.Pin.OUT)


devices = i2c.scan()
if devices:
    print('Sensor encontrado en las direccion', devices)
    oled.fill(0)
    oled.text("SENSOR LISTO", 20, 30)
    oled.show()
    time.sleep(3)
else:
    print('No se encontraron dispositivos I2C')

#CICLO PRINCIPAL
while True:

#DEFINICION DE VARIABLES PARA DATOS
    oled.fill(0)
    temp_pantalla = bmp.temperature
    pres_pantalla = round(bmp.pressure)

#IMPRESION DE LOS DATOS EN PANTALLA
    print("*******************************************")
    print("Temperatura: {:.2f} C".format(temp_pantalla))

#VALORES EN LA OLED
    oled.text('Temperatura:', 15, 25)
    oled.text("{:.2f} C".format(temp_pantalla), 35, 35)
    oled.show()
    
#ENCENDIDO DE LOS LEDS 
    led_r.value(act(peso2,(bmp.temperature/(100)),b2))
    led_v.value(norm((act(peso2,(bmp.temperature/(100)),b2)),(act(peso1,(bmp.temperature/(100)),b1))))
    led_b.value(act(peso1,(bmp.temperature/(100)),b1))
