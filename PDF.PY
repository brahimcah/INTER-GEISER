import PyPDF2

def leer_pdf(nombre_archivo):
    try:
        # Abre el archivo PDF en modo lectura binaria ('rb')
        with open(nombre_archivo, 'rb') as archivo:
            # Crea un objeto PDFReader
            lector_pdf = PyPDF2.PdfFileReader(archivo)

            # Verifica si el PDF tiene al menos una página
            if lector_pdf.numPages == 0:
                print("El PDF no contiene páginas.")
                return

            # Lee todas las páginas del PDF
            texto_completo = ""
            for num_pagina in range(lector_pdf.numPages):
                pagina = lector_pdf.getPage(num_pagina)
                texto_completo += pagina.extractText()

            return texto_completo

    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
    except PyPDF2.utils.PdfReadError:
        print(f"No se pudo leer el archivo '{nombre_archivo}'. Asegúrate de que sea un PDF válido.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llamada a la función para leer el PDF
nombre_archivo = 'ruta/del/archivo.pdf'  # Reemplaza con la ruta de tu archivo PDF
texto_del_pdf = leer_pdf(nombre_archivo)

if texto_del_pdf:
    print(texto_del_pdf)
