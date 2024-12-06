import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import cv2
import numpy as np

#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract

class DetectarRotacion:
    def __init__(self):
        pass
    
    def detectar_rotacion(self, imagen):
        """
        Detecta la orientación del texto en la imagen usando pytesseract.
        """
        try:
            # Usa pytesseract para obtener la orientación de la imagen
            orientation_data = pytesseract.image_to_osd(imagen)
            # Extraemos el ángulo de rotación
            rotacion = int(orientation_data.split("Rotate:")[1].split("\n")[0].strip())
            return rotacion
        except Exception as e:
            print(f"Error al detectar rotación: {e}")
            return 0  # Si hay un error, asumimos que no hay rotación

    def rotar_imagen(self, imagen, angulo):
        """
        Rota la imagen en el ángulo especificado.
        """
        if angulo == 0:
            return imagen  # Si no hay rotación, devolver la imagen original

        # Rotar la imagen usando PIL
        return imagen.rotate(angulo, expand=True)