import cv2
import numpy as np

# Cargar la imagen en escala de grises
image_path = "imagen_grande2.png"
binary_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Aplicar el filtro de Sobel para detectar bordes
sobel_x = cv2.Sobel(binary_image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(binary_image, cv2.CV_64F, 0, 1, ksize=3)

# Calcular la magnitud de los gradientes
sobel_combined = cv2.magnitude(sobel_x, sobel_y)

# Binarizar la imagen resultante
_, binary_result = cv2.threshold(sobel_combined, 1, 255, cv2.THRESH_BINARY)

#binary_result = cv2.bitwise_not(binary_result)
"""kernel = np.ones((9,9), np.uint8)
binary_result = cv2.dilate(binary_result, kernel, iterations=3)

kernel = np.ones((11,11), np.uint8)
binary_result = cv2.erode(binary_result, kernel, iterations=3)"""
# Guardar la imagen binarizada
#cv2.imwrite('imagen_procesada.png', binary_result)

# Mostrar la imagen binarizada
cv2.imshow('Bordes detectados y binarizados', binary_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
