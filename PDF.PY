import fitz  # PyMuPDF
import csv

def leer_pdf(nombre_archivo):
    try:
        # Abre el archivo PDF
        documento = fitz.open(nombre_archivo)

        # Verifica si el PDF tiene al menos una página
        if documento.page_count == 0:
            print("El PDF no contiene páginas.")
            return

        # Lee todas las páginas del PDF
        texto_completo = ""
        for num_pagina in range(documento.page_count):
            pagina = documento.load_page(num_pagina)
            texto_completo += pagina.get_text()

        # Cierra el documento
        documento.close()

        return texto_completo

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def guardar_en_csv(texto, nombre_archivo_csv):
    # Busca las posiciones de las cadenas "NIF:" y "Código de Tasa"
    pos_nif = texto.find("NIF:")
    pos_codigo_tasa = texto.find("Código de Tasa")

    # Obtiene los resultados después de "NIF:" y "Código de Tasa"
    resultado_nif = texto[pos_nif + 4:pos_codigo_tasa].strip()
    resultado_codigo_tasa = texto[pos_codigo_tasa + 15:].strip()

    # Guarda los resultados en un archivo CSV
    with open(nombre_archivo_csv, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["NIF:"])
        writer.writerow([resultado_nif, resultado_codigo_tasa])

# Llamada a la función para leer el PDF
nombre_archivo = r'pdf.pdf'  # Reemplaza con la ruta de tu archivo PDF
texto_del_pdf = leer_pdf(nombre_archivo)

if texto_del_pdf:
    print(texto_del_pdf)
    nombre_archivo_csv = r'resultados.csv'  # Nombre del archivo CSV a guardar
    guardar_en_csv(texto_del_pdf, nombre_archivo_csv)
    print("Resultados guardados en el archivo CSV:", nombre_archivo_csv)
