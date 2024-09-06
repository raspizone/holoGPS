import bluetooth 
import threading
import cv2
import matplotlib.pyplot as plt
import time 
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


serial = i2c(port=1, address=0x3C)

# Inicializar la pantalla OLED SH1107
#
device = ssd1306(serial, rotate=0) 

sizeX = 3996
sizeY = 3436

# Coordenadas de la esquina superior izquierda y esquina inferior derecha
x1 = -3.90940805846654
y1 = 38.9974780467993
y0 = 38.9688989737754
x0 = -3.95215840741489

# Tamaño del área a recortarcv2
area_size = 128

# Resolución del mapa en términos de píxeles por longitud y píxeles por latitud
map_resolution = 256 

# Ancho y alto del mapa en grados
ancho_x = abs(x1 - x0)
alto_y = abs(y1 - y0)

# Píxeles por grado en X e Y
pixel_por_grado_x = sizeX / ancho_x
pixel_por_grado_y = sizeY / alto_y


# Abrir la imagen con OpenCV
image_path = "imagen_procesada.png"
imagen = cv2.imread(image_path)

# Color del punto en formato BGR (azul, verde, rojo)
color = (0, 0, 255)  # Rojo en este caso
thickness = -1  # Para rellenar el círculo


def imprimir_coordenadas(y,x,g):
    if g>10:
        grados = int(g/10)
        grados = grados*10
    else:
        grados = int(g)
    print("Coordenada recibida:", x, y, grados)
    # DiferenciaA en coordenadas X e Y
    diferencia_x = abs(x - x0)
    diferencia_y = abs(y1 - y)

    # Conversión de coordenadas geográficas a coordenadas en píxeles
    px = int(diferencia_x * pixel_por_grado_x)
    py = int(diferencia_y * pixel_por_grado_y)  # Invertir el eje Y

    # Calcular límites del área a recortar
    top_left_x = px - area_size // 2
    top_left_y = py - area_size // 2
    bottom_right_x = px + area_size // 2
    bottom_right_y = py + area_size // 2

    # Asegurarse de que los límites estén dentro de los límites de la imagen
    top_left_x = max(0, top_left_x)
    top_left_y = max(0, top_left_y)
    bottom_right_x = min(sizeX, bottom_right_x)
    bottom_right_y = min(sizeY, bottom_right_y)

    # Dibujar el punto en la imagen
    cv2.circle(imagen, (px, py), 3, color, thickness)

    # Recortar el área de interés de la imagen
    area_recortada = imagen[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    
    center = (area_recortada.shape[1] // 2, area_recortada.shape[0] // 2)
    # Obtener la matriz de rotación
    M = cv2.getRotationMatrix2D(center, grados*-1, 1.0)
    # Aplicar la rotación
    rotated_area = cv2.warpAffine(area_recortada, M, (area_recortada.shape[1], area_recortada.shape[0]))
    # Mostrar el área recortada
    
    cv2.imwrite("rotada.jpg",rotated_area )
    cv2.imwrite("recorte.jpg",area_recortada )
    cv2.imshow('Frame completo', area_recortada)
    
    
    
    """ax.imshow(cv2.cvtColor(area_recortada, cv2.COLOR_BGR2RGB))
    ax.set_title(f"Coordenada: ({x}, {y})")
    plt.draw()  # Actualizar la ventana de visualización
    plt.pause(1)  # Pausa la ejecución durante 1 segundo
    ax.clear()  # Limpiar el eje para la próxima iteración
    
plt.close()  # Cerrar la ventana después de completar todas las iteraciones
    
    
    
    x = (device.width - sizeX) // 2
    y = (device.height - sizeY) // 2

    # Muestra la imagen en la pantalla OLED
    with canvas(device) as draw:
        draw.bitmap((x, y), image, fill="white")

    """
   


def imprimir_oled():
    
        # Configura la interfaz I2C
    serial = i2c(port=1, address=0x3C)

    # Inicializa el dispositivo OLED SSD1306
    device = ssd1306(serial, rotate=0)

    # Carga la imagen BMP
    image_path = "recorte.jpg"
    image = Image.open(image_path).convert("1")  # Convierte la imagen a blanco y negro
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # Calcula el tamaño de la imagen y la posición para centrarla en la pantalla
    image_width, image_height = image.size
    x = (device.width - image_width) // 2
    y = (device.height - image_height) // 2
    while True:
        image_path = "rotada.jpg"
        image = Image.open(image_path).convert("1")
        # Muestra la imagen en la pantalla OLED
        with canvas(device) as draw:
            draw.bitmap((x, y), image, fill="white")
        
        # Espera unos segundos antes de salir
        

# Función para inicializar la conexión Bluetooth
def iniciar_servidor_bluetooth():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
    port = 22  # Puedes cambiar el puerto si lo necesitas
    server_sock.bind(("", port)) 
    server_sock.listen(1) 
    print("Esperando conexión Bluetooth...")
    client_sock, address = server_sock.accept() 
    print("Conexión realizada con:", address) 
    return server_sock, client_sock


# Función para recibir coordenadas por Bluetooth en un hilo separado
def recibir_coordenadas(client_sock):


    while True:
        data = client_sock.recv(1024)
        if not data:
            print("Cliente desconectado.")
            break
        # Suponiendo que recibimos las coordenadas en formato "x,y"
        coordenada = data.decode().split(",")
        print(coordenada)
        if len(coordenada) == 3:
            try:
                x = float(coordenada[0])
                y = float(coordenada[1])
                g = float(coordenada[2])
                imprimir_coordenadas(x, y, g)
                time.sleep(1)
            except ValueError:
                print("Formato de coordenadas inválido:", data.decode())

# Función para imprimir la imagen correspondiente a la coordenada recibida

server_sock, client_sock = iniciar_servidor_bluetooth()

# Iniciar el hilo para recibir coordenadas
hilo_recepcion = threading.Thread(target=recibir_coordenadas, args=(client_sock,))
hilo_recepcion.start()

imprimir = threading.Thread(target=imprimir_oled, args=())
imprimir.start()
cv2.destroyAllWindows()


# Inicializar la conexión Bluetooth
