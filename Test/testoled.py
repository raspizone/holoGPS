from PIL import Image
import numpy as np
import Adafruit_SSD1306
import time

# Función para cargar y convertir la imagen a una matriz binaria
def image_to_binary(image_path, new_width, new_height):
    # Abrir la imagen
    img = Image.open(image_path).convert('L')  # Convierte la imagen a escala de grises

    # Redimensionar la imagen
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Convertir la imagen a una matriz numpy binaria
    img_binary = np.array(img)

    # Invertir los valores (blanco -> 0, negro -> 1)
    img_binary = 1 - (img_binary / 255)

    return img_binary

# Configuración del display
RST = None  # Pin de reset (no se utiliza)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()

# Limpiar el display
disp.clear()
disp.display()

# Cargar imagen y convertirla a binario
image_path = 'ejemplo.jpg'  # Ruta de la imagen JPEG
binary_image = image_to_binary(image_path, 128, 64)

# Mostrar imagen en el display
image = Image.new('1', (128, 64))
image.putdata(binary_image.ravel())
disp.image(image)
disp.display()

# Esperar unos segundos
time.sleep(10)
