

class NombreArchivo:
    
    # Función para recortar nombre
    def recortar_nombre(nombre_completo):
        partes = nombre_completo.split()
        if len(partes) == 4:
            nombre = partes[0][:2].lower() + partes[1][:2].lower() + partes[3][:2].lower()
        else:
            nombre = partes[0][:2].lower() + partes[1][:2].lower() + partes[2][:2].lower()
        return nombre
    
    
    def recortar_nombre(nombre_completo):
        partes = nombre_completo.split()

        if len(partes) == 4:  # Si tiene segundo nombre, lo omitimos
            nombre = partes[0]
            primer_apellido = partes[2]
            segundo_apellido = partes[3]
        else:  # Si no tiene segundo nombre
            nombre = partes[0]
            primer_apellido = partes[1]
            segundo_apellido = partes[2] if len(partes) > 2 else ""
        
        # Generar el código: 2 primeras letras del nombre + 2 del primer apellido + 2 del segundo apellido
        return nombre[:2].upper() + primer_apellido[:2].upper() + segundo_apellido[:2].upper()
