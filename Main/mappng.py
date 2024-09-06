import bluetooth 
import threading
import cv2
import matplotlib.pyplot as plt
import time 
from luma.core.interface.serial import i2c
from luma.oled.device import sh1107
from PIL import Image




# Función para inicializar la conexión Bluetooth
def iniciar_servidor_bluetooth():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
    port = 1  # Puedes cambiar el puerto si lo necesitas
    server_sock.bind(("", port)) 
    server_sock.listen(1) 
    print("Esperando conexión Bluetooth...")
    client_sock, address = server_sock.accept() 
    print("Conexión realizada con:", address) 
    return server_sock, client_sock

# Función para recibir coordenadas por Bluetooth en un hilo separado
def recibir_coordenadas(client_sock):
    coordenadas = []
    while True:
        data = client_sock.recv(1024)
        if not data:
            print("Cliente desconectado.")
            break
        # Suponiendo que recibimos las coordenadas en formato "x,y"
        coordenada = data.decode().split(",")
        if len(coordenada) == 2:
            try:
                x = float(coordenada[0])
                y = float(coordenada[1])
                coordenadas.append([x, y])
                imprimir_coordenada(coordenadas)
                print("Coordenada recibida:", x, y)
            except ValueError:
                print("Formato de coordenadas inválido:", data.decode())




# Crear un hilo para recibir coordenadas por Bluetooth

        # Hacer algo con las coordenadas recibidas, como procesarlas o mostrarlas
server_sock, client_sock = iniciar_servidor_bluetooth()
# Iniciar el hilo para recibir coordenadas
hilo_recepcion = threading.Thread(target=recibir_coordenadas)
hilo_recepcion.start()
#serial = i2c(port=1, address=0x3C)

# Inicializar la pantalla OLED SH1107
#device = sh1107(serial, rotate=0) 

# Dimensiones de la imagen
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
image = cv2.imread(image_path)

# Color del punto en formato BGR (azul, verde, rojo)
color = (0, 0, 255)  # Rojo en este caso
thickness = -1  # Para rellenar el círculo


# Iterar sobre las coordenadas y realizar la operación en cada posición
def imprimir_coordenadas(coordenadas):
    x, y = coordenadas

    # Diferencia en coordenadas X e Y
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
    cv2.circle(image, (px, py), 3, color, thickness)

    # Recortar el área de interés de la imagen
    area_recortada = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

    # Mostrar el área recortada
    cv2.imshow('Frame completo', area_recortada)
    
    
    """ax.imshow(cv2.cvtColor(area_recortada, cv2.COLOR_BGR2RGB))
    ax.set_title(f"Coordenada: ({x}, {y})")
    plt.draw()  # Actualizar la ventana de visualización
    plt.pause(1)  # Pausa la ejecución durante 1 segundo
    ax.clear()  # Limpiar el eje para la próxima iteración
    
plt.close()"""  # Cerrar la ventana después de completar todas las iteraciones
    
    
    #imagen_pil = Image.fromarray(cv2.cvtColor(area_recortada, cv2.COLOR_BGR2RGB))
    #imagen_pil.show()
    # Mostrar la imagen en la pantalla OLED
    #device.display(imagen_pil)
    
    time.sleep(1)
cv2.destroyAllWindows()
