import smbus
from time import sleep

# Dirección I2C de la pantalla SSH1107
LCD_I2C_ADDR = 0x3C

# Comandos para la pantalla SSH1107
CMD_DISPLAY_SETUP = 0xAE
CMD_SET_DISP = 0xAF
CMD_SET_CONTRAST = 0x81
CMD_SET_NORMAL_DISPLAY = 0xA6
CMD_DISPLAY_ON = 0xAF
CMD_DISPLAY_OFF = 0xAE

# Inicialización del bus I2C
bus = smbus.SMBus(1)  # 1 indica el bus I2C 1 en la Raspberry Pi 3 y 4

def send_command(cmd):
    bus.write_byte_data(LCD_I2C_ADDR, 0x00, cmd)

def send_data(data):
    bus.write_byte_data(LCD_I2C_ADDR, 0x40, data)

def init_lcd():
    send_command(CMD_DISPLAY_SETUP)
    send_command(0xD3)  # Set display offset
    send_command(0x00)  # No offset
    send_command(0x40)  # Set display start line
    send_command(CMD_SET_NORMAL_DISPLAY)
    send_command(0xA8)  # Set multiplex ratio
    send_command(0x3F)  # 1/64 duty
    send_command(CMD_SET_CONTRAST)
    send_command(0xCF)  # Set contrast
    send_command(0xD5)  # Set display clock divide ratio/oscillator frequency
    send_command(0x80)  # Set clock divide ratio
    send_command(0xD9)  # Set pre-charge period
    send_command(0xF1)
    send_command(0xDA)  # Set com pins hardware configuration
    send_command(0x12)
    send_command(0xDB)  # Set VCOMH
    send_command(0x40)
    send_command(0x8D)  # Set charge pump
    send_command(0x14)
    send_command(CMD_SET_DISP)
    send_command(CMD_DISPLAY_ON)

def clear_lcd():
    for i in range(0, 128):
        send_data(0x00)

def display_text(text):
    for char in text:
        send_data(ord(char))

if __name__ == "__main__":
    try:
        init_lcd()  # Inicializa la pantalla
        clear_lcd()  # Borra la pantalla
        display_text("Hola, Raspberry Pi!")  # Muestra el texto en la pantalla
        sleep(5)  # Espera 5 segundos
        clear_lcd()  # Borra la pantalla nuevamente
    except KeyboardInterrupt:
        clear_lcd()  # Borra la pantalla si se interrumpe el programa
