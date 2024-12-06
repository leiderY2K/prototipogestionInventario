from gestion_anios import GestionAnios
from gestion_categorias import GestionCategorias
from gestion_investigadores import GestionInvestigadores

class CodigoProducto:
    def __init__(self):
        self.gestion_categorias = GestionCategorias()
        self.gestion_anios = GestionAnios()
        self.gestion_investigadores = GestionInvestigadores()

    def generar_codigo_producto(self, nombre, ano, categoria):
        nom_corto = self.gestion_investigadores.recortar_nombre(nombre)
        ano_corto = self.gestion_anios.extraer_ano(ano)[0]
        cat_corta = self.gestion_categorias.recortar_nombre_categoria(categoria)
        print(f"Generando código: {nom_corto} - {ano_corto} - {cat_corta}")  # Debugging
        return f"{nom_corto}{ano_corto}{cat_corta}"