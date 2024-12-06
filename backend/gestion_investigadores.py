import difflib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import unicodedata
import re

class GestionInvestigadores:
    def __init__(self):
        self.investigadores = [
            "Andrea García Rivas", "Armando Díaz Escobar", "Armando Solano Suárez",
            "Camilo Alejandro Corchuelo Rodríguez", "Clara Liliana Montero Rodriguez",
            "Diego Germán Pérez Villamarín", "Eduardo Hernández Ortiz",
            "Fernando Martínez Rodríguez", "Hernán Darío Cortés Silva",
            "Jaime Alberto Páez Páez", "Jenny Esperanza Navas Villegas",
            "Jorge Enrique Pérez Nepta", "Julio Cortés Trujillo", "Luis Alberto Garcia González",
            "Luis Alexander Jimenez Hernández", "Luis Alfonso Melo Ospina",
            "Luis Eduardo Herrera Ramírez", "Martha Cecilia Herrera Romero",
            "Nelson Javier Ruiz Aponte", "Pablo Emilio Góngora Tafur", "Rodrigo Jaimes Abril",
            "Rodrigo Quintero", "Pedro Julio Caro", "Eduardo Antonio Bonilla Norato",
            "Astrid Carolina Rodríguez Cristancho", "Diego Alejandro Rodríguez Peralta"
        ]
        self.cargos_exclusion = ["rector", "vicerrector", "coordinador", "secretario"]
    
    def recortar_nombre(self, nombre_completo):
        partes = nombre_completo.split()
        if len(partes) == 4:  # Si tiene segundo nombre, lo omitimos
            nombre = partes[0]
            primer_apellido = partes[2]
            segundo_apellido = partes[3]
        else:  # Si no tiene segundo nombre
            nombre = partes[0]
            primer_apellido = partes[1]
            segundo_apellido = partes[2] if len(partes) > 2 else ""
        
        return nombre[:2].upper() + primer_apellido[:2].upper() + segundo_apellido[:2].upper()

    def normalizar_texto(self, texto):
        # Eliminar tildes y convertir a minúsculas
        return ''.join(c for c in unicodedata.normalize('NFD', texto.lower())
                    if unicodedata.category(c) != 'Mn')

    def calcular_similitud(self, nombre1, nombre2):
        # Normalizar los nombres antes de comparar
        nombre1_norm = self.normalizar_texto(nombre1)
        nombre2_norm = self.normalizar_texto(nombre2)
        return difflib.SequenceMatcher(None, nombre1_norm, nombre2_norm).ratio()

    def buscar_investigadores_en_texto(self, texto, umbral_similitud=0.82):
        investigadores_encontrados = []
        texto_normalizado = self.normalizar_texto(texto)
        lineas = texto_normalizado.split('\n')
        
        identificadores_encontrados = set()  # Conjunto para almacenar identificadores únicos

        for i, linea in enumerate(lineas):
            for investigador in self.investigadores:
                investigador_normalizado = self.normalizar_texto(investigador)
                if investigador_normalizado in linea:
                    similitud = 1.0  # Coincidencia exacta
                else:
                    # Buscar por partes del nombre
                    partes_nombre = investigador_normalizado.split()
                    similitudes = []
                    for parte in partes_nombre:
                        if parte in linea:
                            similitudes.append(1.0)
                        else:
                            mejor_similitud = max((self.calcular_similitud(parte, palabra)
                            for palabra in linea.split()),
                            default=0)
                            similitudes.append(mejor_similitud)
                    similitud = sum(similitudes) / len(similitudes)

                if similitud >= umbral_similitud:
                    # Verificar si hay cargos de exclusión en las próximas 2 líneas
                    excluir = False
                    for j in range(i + 1, min(i + 3, len(lineas))):
                        if any(cargo in lineas[j] for cargo in self.cargos_exclusion):
                            excluir = True
                            break

                    if not excluir:
                        identificador = self.obtener_identificador(investigador)
                        # Solo agregar si el identificador no ha sido encontrado antes
                        if identificador not in identificadores_encontrados:
                            investigadores_encontrados.append((investigador, identificador, similitud))
                            identificadores_encontrados.add(identificador)  # Agregar a los encontrados

        return investigadores_encontrados



    def obtener_identificador(self, nombre_completo):
        return self.recortar_nombre(nombre_completo)
    