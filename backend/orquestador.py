import httpx
import pytesseract
import os
import difflib
import openpyxl
from gestion_categorias import GestionCategorias
from gestion_anios import GestionAnios
from detectar_rotacion import DetectarRotacion
from codigo_producto import CodigoProducto
from pdf2image import convert_from_bytes
from gestion_investigadores import GestionInvestigadores
from ms_graph import MS_GRAPH_BASE_URL, get_access_token
#from guardar_excel import GuardarExcel
from guardar_mysql import GuardarMySQL
import re

class Orquestador:
    
    def __init__(self):
        self.contenidos_procesados = []
        self.gestion_categorias = GestionCategorias()
        self.gestion_anios = GestionAnios()
        self.detectar_rotacion = DetectarRotacion()
        #self.guardar_excel = GuardarExcel()
        self.gestion_investigadores = GestionInvestigadores()
        self.SIZE_LIMIT = 10 * 1024 * 1024
        
        self.db_config = {
            'host': 'localhost',
            'user': 'user',
            'password': 'password',
            'database': 'bdvirtus',
            'port':'3306'
        }
        
        self.guardar_mysql = GuardarMySQL(self.db_config)
        
    # Procesar el PDF con OCR
    def process_pdf_with_ocr(self, pdf_bytes):
            paginas = convert_from_bytes(pdf_bytes)
            texto_completo = ""
            
            for num_pagina, imagen in enumerate(paginas[:2]):  # Solo procesamos las 2 primeras páginas
                # Detectamos si la imagen necesita rotación
                rotacion = self.detectar_rotacion.detectar_rotacion(imagen)
                if rotacion != 0:
                    print(f"La página {num_pagina + 1} está rotada {rotacion} grados. Corrigiendo...")
                    imagen = self.detectar_rotacion.rotar_imagen(imagen, -rotacion)  # Aplicamos la rotación inversa

                # Extraemos el texto de la imagen procesada
                texto_extraido = pytesseract.image_to_string(imagen)
                texto_completo += texto_extraido + "\n\n"  # Añade dos saltos de línea entre páginas

            # Aplicar limpieza y tokenización al texto extraído
            texto_completo = texto_completo.strip()
            
            return texto_completo
        
    def contenido_esta_repetido(self, nuevo_contenido, umbral=0.95):
        for contenido_existente in self.contenidos_procesados:
            similitud = difflib.SequenceMatcher(None, nuevo_contenido, contenido_existente).ratio()
            if similitud > umbral:
                return True
        
        # Si no se encontró ninguna coincidencia por encima del umbral, agregamos el nuevo contenido a la lista
        self.contenidos_procesados.append(nuevo_contenido)
        return False

    def process_pdf_in_memory(self, headers, file_id, file_name):
        url = f'{MS_GRAPH_BASE_URL}/me/drive/items/{file_id}'
        try:
            response = httpx.get(url, headers=headers, follow_redirects=True)
            if response.status_code == 200:
                data = response.json()
                if data['size'] > self.SIZE_LIMIT:
                    print(f"El archivo {file_name} excede el límite de tamaño de 10 MB. Se omitirá su procesamiento.")
                    return None
                download_url = data['@microsoft.graph.downloadUrl']
                pdf_response = httpx.get(download_url, follow_redirects=True)
                if pdf_response.status_code == 200:
                    pdf_bytes = pdf_response.content
                    texto_extraido = self.process_pdf_with_ocr(pdf_bytes)
                    if texto_extraido:
                        if self.contenido_esta_repetido(texto_extraido):
                            print(f"El contenido del archivo {file_name} está repetido. Se omitirá su procesamiento.")
                            return None
                        
                        categorias = self.gestion_categorias.classify(texto_extraido)
                        print(f"Categorías encontradas: {categorias}")
                        
                        años = self.gestion_anios.extraer_ano(texto_extraido)
                        print(f"Años encontrados: {años if años else 'Ninguno encontrado'}")
                        
                        return texto_extraido, categorias, data['size'], años
                    else:
                        print(f"No se pudo extraer texto del archivo {file_name}")
                else:
                    print(f"Error al descargar el archivo desde la URL: {pdf_response.status_code}")
            else:
                print(f"Error al obtener los detalles del archivo: {response.status_code}")
        except httpx.RequestError as exc:
            print(f"Ocurrió un error solicitando {exc.request.url!r}")
        return None

    def list_and_process_files_in_onedrive_folder(self, headers, folder_path='root'):
            MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'  # Asegúrese de definir esta constante
            folder_path_encoded = folder_path.replace(" ", "%20")
            url = f'{MS_GRAPH_BASE_URL}/me/drive/root:/{folder_path_encoded}:/children'
            resultados_mysql = []
            
            try:
                response = httpx.get(url, headers=headers, follow_redirects=True)
                if response.status_code == 200:
                    data = response.json()
                    for item in data['value']:
                        if 'folder' in item:
                            print(f"-> Explorando carpeta: {item['name']}")
                            sub_resultados = self.list_and_process_files_in_onedrive_folder(headers, folder_path + '/' + item['name'])
                            resultados_mysql.extend(sub_resultados)
                        elif item['name'].lower().endswith('.pdf'):
                            print(f"\nProcesando archivo: {item['name']}")
                            resultado = self.process_pdf_in_memory(headers, item['id'], item['name'])
                            link_archivo = item['@microsoft.graph.downloadUrl']
                            
                            if resultado:
                                texto_extraido, categorias, tamanio, años = resultado
                                investigadores_encontrados = self.gestion_investigadores.buscar_investigadores_en_texto(texto_extraido)
                                print(f"Investigadores encontrados en {item['name']}: {len(investigadores_encontrados)}")
                                
                                for investigador, identificador, similitud in investigadores_encontrados:
                                    fila = [
                                        investigador,                    # INVESTIGADOR
                                        item['name'],                    # TÍTULO DEL PRODUCTO
                                        ", ".join(categorias),           # TIPO DEL PRODUCTO
                                        ", ".join(años),                 # AÑO
                                        identificador,                   # NOMBRE DEL ARCHIVO
                                        link_archivo                     # LINK ARCHIVO
                                    ]
                                    resultados_mysql.append(fila)
                                    print(f" - Investigador: {investigador} (similitud: {similitud:.2f})")
                            else:
                                print("No se pudo procesar el archivo.")
                                # Guardar solo el título y el link para procesarlo manualmente
                                fila = [
                                    "",                                # INVESTIGADOR vacío
                                    item['name'],                      # TÍTULO DEL PRODUCTO
                                    "",                                # TIPO DEL PRODUCTO vacío
                                    "",                                # AÑO vacío
                                    "",                                # NOMBRE DEL ARCHIVO vacío
                                    link_archivo                       # LINK ARCHIVO
                                ]
                                resultados_mysql.append(fila)
                else:
                    print(f'Error al listar archivos en la carpeta {folder_path}: {response.status_code}')
            except httpx.RequestError as exc:
                print(f"Ocurrió un error solicitando {exc.request.url!r}")
            
            return resultados_mysql

    def procesar_y_guardar_resultados(self, headers, carpeta_raiz='root'):
        try:
            self.guardar_mysql.conectar()
            
            # Procesar los archivos
            resultados_totales = self.list_and_process_files_in_onedrive_folder(headers, carpeta_raiz)
            
            # Guardar resultados en MySQL
            self.guardar_mysql.guardar_datos(resultados_totales)
            
            print(f"Se encontraron {len(resultados_totales)} menciones de investigadores en total.")
            print("Los resultados se han guardado en la base de datos MySQL.")
        
        except Exception as e:
            print(f"Error durante el procesamiento: {str(e)}")
            raise
        finally:
            # Cerrar la conexión a MySQL
            if hasattr(self, 'guardar_mysql'):
                self.guardar_mysql.cerrar_conexion()

# Función principal para iniciar el procesamiento
def main():
    scopes = ['User.Read', 'Files.Read.All']
    try:
        access_token = get_access_token(scopes=scopes)
        headers = {'Authorization': 'Bearer ' + access_token}
        
        # Carpeta en OneDrive
        folder_path = '_CvLAC/pruebas'
        #folder_path = 'Base-Evidencias-G-VIRTUS'
        print(f'Listando y procesando archivos en: "{folder_path}"')
        
        # Instanciar la clase para orquestar investigadores
        orquestador = Orquestador()
        
        # Procesar los archivos y guardar los resultados
        orquestador.procesar_y_guardar_resultados(headers, folder_path)
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
    
#import nltk
#nltk.download('stopwords')