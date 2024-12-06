import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rapidfuzz import fuzz

class GestionCategorias:
    def __init__(self):
        self.categorias = {
            "Evento Cientifico Asistente": ["asistente", "asistió"],
            "Evento Cientifico Participación": ["participante", "participo"],
            "Evento Científico Ponente": ["ponente"],
            "Evento Cientifico Tallerista": ["tallerista", "impartio"],
            "Evento Cientifico ORGANIZ": [],
            "Constancia": ["Consta", "Constar"],
            "Consultorías científicas y tecnológicas": ["como consultor","asesor tecnico"],
            "Informes técnicos finales": ["informe técnico", "final"],
            "Innovaciones en procedimientos": ["datos innovacion", "innovación en"],
            "Libro": ["libro", "datos de la producción", "bibliografica"],
            "Reconocimientos": ["hace constar","reconocimiento como"],
            "Software, Redes de Conocimiento": ["datos software"],
            "Artículo": ["resumen", "palabras clave", "abstract"],
            "Dirección Trabajo de Grado Maestría": ["acta de sustentacion", "trabajo de grado", "maestria"],
            "Empresas de base tecnológica creadas": ["spin", "off", "empresa"],}
        self.stop_words = set(stopwords.words('spanish')).union(set(stopwords.words('english')))

    def clean_text(self, text):
        """
        Limpia el texto eliminando caracteres especiales y números.
        """
        text = text.lower()  # Minúsculas
        text = re.sub(r'[^a-záéíóúüñ\s]', '', text)  # Eliminar caracteres no deseados
        text = re.sub(r'\s+', ' ', text).strip()  # Múltiples espacios
        return text

    def tokenize_text(self, cleaned_text):
        """
        Tokeniza el texto eliminando stopwords.
        """
        tokens = word_tokenize(cleaned_text)
        tokens = [word for word in tokens if word not in self.stop_words]  # Filtrar stopwords
        return tokens

    def palabra_similar(self, palabra, palabras_clave, umbral=0.80):
        """
        Compara la palabra con las palabras clave usando la similitud de Levenshtein
        y devuelve True si alguna palabra clave se aproxima al umbral de similitud.
        """
        for palabra_clave in palabras_clave:
            similitud = fuzz.ratio(palabra, palabra_clave) / 100.0  # Convertir similitud a un valor entre 0 y 1
            if similitud >= umbral:
                return True
        return False
#leiderre24@outlook.com
    def classify(self, text, umbral=0.83):
        """
        Clasifica el texto según las categorías definidas.
        """
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize_text(cleaned_text)
        
        categorias_encontradas = set()
        for token in tokens:
            for categoria, palabras_clave in self.categorias.items():
                if self.palabra_similar(token, palabras_clave, umbral):
                    categorias_encontradas.add(categoria)
        
        return list(categorias_encontradas)
    
    def recortar_nombre_categoria(self, nombre_categoria):
        """
        Recorta el nombre de la categoría y devuelve las iniciales en mayúsculas,
        ignorando las stopwords.
        """
        partes = nombre_categoria.split()
        iniciales = ''.join([parte[0].upper() for parte in partes if parte.lower() not in self.stop_words])  # Ignorar stopwords
        return iniciales