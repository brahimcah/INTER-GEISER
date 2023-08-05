import os
import fitz  # PyMuPDF
import csv

def leer_pdf(nombre_archivo):
    try:
        # Abre el archivo PDF
        documento = fitz.open(nombre_archivo)

        # Verifica si el PDF tiene al menos una página
        if documento.page_count == 0:
            print(f"El PDF '{nombre_archivo}' no contiene páginas.")
            return

        # Lee todas las páginas del PDF y extrae el texto
        texto_completo = ""
        for num_pagina in range(documento.page_count):
            pagina = documento.load_page(num_pagina)
            texto_completo += pagina.get_text()

        # Cierra el documento
        documento.close()

        return texto_completo

    except Exception as e:
        print(f"Error al procesar el PDF '{nombre_archivo}': {e}")
        return None

# Función para obtener la palabra siguiente a una cadena específica
def obtener_palabra_siguiente(texto, cadena, longitud_max):
    indice_inicio = texto.find(cadena)
    if indice_inicio != -1:
        indice_inicio += len(cadena)  # Avanza hasta el final de la cadena
        palabra = texto[indice_inicio:indice_inicio + longitud_max]
        # Verificar si la palabra tiene la longitud adecuada
        if len(palabra) == longitud_max:
            return palabra.strip()  # Elimina los espacios en blanco al inicio y final
    return None

# Carpeta con los archivos PDF
ruta_carpeta = r'C:\\Geiser\\INTER'

# Lista de archivos PDF en la carpeta
archivos_pdf = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".pdf")]

# Procesar cada archivo PDF y guardar en el archivo CSV
with open('informacion.csv', 'w', newline='') as archivo_csv:
    campos = ['NIF', 'Código de Tasa']
    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

    escritor_csv.writeheader()

    for archivo_pdf in archivos_pdf:
        ruta_pdf = os.path.join(ruta_carpeta, archivo_pdf)
        texto_del_pdf = leer_pdf(ruta_pdf)

        if texto_del_pdf:
            # Obtener palabras después de "NIF:" y "Código de Tasa"
            nif = obtener_palabra_siguiente(texto_del_pdf, "NIF:", 10)
            codigo_tasa = obtener_palabra_siguiente(texto_del_pdf, "Código de Tasa", 12)

            # Guardar en el archivo CSV si ambos valores son válidos
            if nif and codigo_tasa:
                escritor_csv.writerow({'NIF': nif, 'Código de Tasa': codigo_tasa})
                print(f"Datos guardados del PDF '{archivo_pdf}'")
            else:
                print(f"No se encontraron valores válidos para NIF o Código de Tasa en el PDF '{archivo_pdf}'")

print("Proceso completado.")
