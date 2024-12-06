import re
from nltk.corpus import stopwords
from rapidfuzz import fuzz
from typing import List, Optional, Tuple

class GestionAnios:
    def __init__(self):
        # Rangos de años
        self.anos = [str(a) for a in range(2007, 2025)]
        self.anos_decimal = [f"2.{str(a)[1:]}" for a in range(2007, 2025)]
        
        # Palabras base para comparación
        self.palabra_base = "expide"
        
        # Patrones para detectar años escritos en texto
        self.patron_ano_texto = r'dos mil (\w+)'
        self.numeros_texto = {
            'dieciséis': '2016', 'diecisiete': '2017', 'dieciocho': '2018',
            'diecinueve': '2019', 'veinte': '2020', 'veintiuno': '2021',
            'veintidós': '2022', 'veintitres': '2023', 'veinticuatro': '2024'
        }
        
        # Configuración
        self.stop_words = set(stopwords.words('spanish')).union(set(stopwords.words('english')))
        self.umbral_similitud = 0.80

    def es_similar_a_expide(self, palabra: str) -> bool:
        """
        Compara si una palabra es similar a 'expide' usando similitud de Levenshtein.
        """
        similitud = fuzz.ratio(palabra.lower(), self.palabra_base) / 100.0
        return similitud >= self.umbral_similitud

    def extract_year_from_text(self, text: str) -> List[Tuple[str, int]]:
        """
        Extrae años en varios formatos y sus posiciones:
        - Formato numérico (2016)
        - Formato decimal (2.016)
        - Formato texto (dos mil dieciséis)
        """
        anos_encontrados = []
        
        # Buscar años en formato numérico
        for ano in self.anos:
            for match in re.finditer(r'\b' + ano + r'\b', text):
                anos_encontrados.append((ano, match.start()))
        
        # Buscar años en formato decimal
        matches = re.finditer(r'2\.(\d{3})', text)
        for match in matches:
            ano = f"2{match.group(1)}"
            anos_encontrados.append((ano, match.start()))
            
        # Buscar años escritos en texto
        matches = re.finditer(self.patron_ano_texto, text.lower())
        for match in matches:
            numero_texto = match.group(1)
            if numero_texto in self.numeros_texto:
                ano = self.numeros_texto[numero_texto]
                anos_encontrados.append((ano, match.start()))
        
        return anos_encontrados

    def encontrar_ultima_palabra_expide(self, text: str) -> Optional[int]:
        """
        Encuentra la posición de la última palabra similar a 'expide'.
        """
        ultima_posicion = -1
        
        # Dividir el texto en palabras manteniendo la información de posición
        palabras = [(m.group(), m.start()) for m in re.finditer(r'\b\w+\b', text.lower())]
        
        for palabra, posicion in palabras:
            if self.es_similar_a_expide(palabra):
                ultima_posicion = posicion
                
        return ultima_posicion if ultima_posicion != -1 else None

    def extraer_ano(self, text: str) -> List[str]:
        """
        Extrae el año más apropiado del texto, considerando las nuevas condiciones:
        1. Prioriza el año al inicio del texto.
        2. Descarta años seguidos por un guion.
        3. Si no hay año al inicio, busca después de 'expide'.
        4. Si no se cumple ninguna condición, devuelve todos los años encontrados.
        """
        # Obtener todos los años y sus posiciones
        anos_con_posicion = self.extract_year_from_text(text)
        
        if not anos_con_posicion:
            return []

        # Verificar si hay un año al inicio del texto
        primer_ano = min(anos_con_posicion, key=lambda x: x[1])
        if primer_ano[1] == 0:
            # Verificar si el año está seguido por un guion
            siguiente_caracter = text[len(primer_ano[0]):len(primer_ano[0])+1]
            if siguiente_caracter != '-':
                return [primer_ano[0]]
        
        # Encontrar la posición de la última palabra similar a 'expide'
        pos_expide = self.encontrar_ultima_palabra_expide(text)
        
        if pos_expide is not None:
            # Filtrar años que aparecen después de 'expide'
            anos_despues_expide = [(ano, pos) for ano, pos in anos_con_posicion if pos > pos_expide]
            if anos_despues_expide:
                # Retornar el primer año que aparece después de 'expide'
                ano_candidato = min(anos_despues_expide, key=lambda x: x[1])[0]
                # Verificar si está seguido por un guion
                indice = text.index(ano_candidato)
                if text[indice + len(ano_candidato):indice + len(ano_candidato) + 1] != '-':
                    return [ano_candidato]
        
        # Si no se cumple ninguna condición, retornar todos los años encontrados
        # excluyendo los que están seguidos por un guion
        return list(set(ano for ano, pos in anos_con_posicion 
                        if text[pos + len(ano):pos + len(ano) + 1] != '-'))