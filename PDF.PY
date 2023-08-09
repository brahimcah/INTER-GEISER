import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import zipfile
import fitz  # PyMuPDF
import csv
from os import system

def extract_zips(source_folder, destination_folder):
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Obtener la lista de archivos en la carpeta de origen
    files = os.listdir(source_folder)

    # Iterar sobre los archivos y extraer los ZIPs
    for file in files:
        file_path = os.path.join(source_folder, file)
        if file.endswith('.zip') and os.path.isfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            print(f"Extrayendo {file} a {destination_folder}")

def eliminar_archivos_con_guion_bajo(directorio):
    try:
        # Obtener la lista de archivos en el directorio
        archivos = os.listdir(directorio)
        
        for archivo in archivos:
            # Comprobar si el nombre del archivo contiene el carácter '_'
            if '_' in archivo:
                # Construir la ruta completa del archivo
                ruta_completa = os.path.join(directorio, archivo)
                
                # Eliminar el archivo
                os.remove(ruta_completa)
                print(f"Archivo eliminado: {ruta_completa}")
        
        print("Eliminación completada.")
    
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


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

def proceso():
    # Definir aquí la lógica del primer proceso
    messagebox.showinfo("Proceso", "El primer proceso ha sido ejecutado.")
    if __name__ == "__main__":
        #Indicamos la Rutas que vamos a usar
        source_folder = r'C:\\Geiser\\ZIP'
        destination_folder = r'C:\\Geiser\\INTER'
        ruta_csv = r'C:\\Geiser\\info.csv'
        
        extract_zips(source_folder, destination_folder)
        eliminar_archivos_con_guion_bajo(destination_folder)

        # Lista de archivos PDF en la carpeta
        archivos_pdf = [archivo for archivo in os.listdir(destination_folder) if archivo.endswith(".pdf")]

        # Procesar cada archivo PDF y guardar en el archivo CSV
        with open(ruta_csv, 'w', newline='') as archivo_csv:
            campos = ['NIF', 'Código de Tasa']
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)

            escritor_csv.writeheader()

            for archivo_pdf in archivos_pdf:
                ruta_pdf = os.path.join(destination_folder, archivo_pdf)
                texto_del_pdf = leer_pdf(ruta_pdf)

                if texto_del_pdf:
                    # Obtener palabras después de "NIF:" y "Código de Tasa"
                    nif = obtener_palabra_siguiente(texto_del_pdf, "NIF:", 10)
                    codigo_tasa = obtener_palabra_siguiente(texto_del_pdf, "Código de Tasa", 13)

                    # Guardar en el archivo CSV si ambos valores son válidos
                    if nif and codigo_tasa:
                        escritor_csv.writerow({'NIF': nif, 'Código de Tasa': codigo_tasa})
                        print(f"Datos guardados del PDF '{archivo_pdf}'")
                    else:
                        print(f"No se encontraron valores válidos para NIF o Código de Tasa en el PDF '{archivo_pdf}'")

        print("Proceso completado.")
        system('"C:\Program Files\LibreOffice\program\scalc.exe" c:\Geiser\info.csv')
        

def limpio():
    # Definir aquí la lógica de la función 'limpio'
    system("del /s /q c:\Geiser\INTER\*.*")
    system("del /s /q c:\Geiser\ZIP\*.*")
    messagebox.showinfo("Limpio", "La función 'limpio' ha sido ejecutada.")

# Crear una ventana principal
root = tk.Tk()
root.title("GESTOR INTERNACIONALES GEISER")

# Crear estilo para widgets ttk
style = ttk.Style()
style.theme_use("clam")  # Puedes cambiar el tema según tus preferencias

# Crear los botones con estilo
btn_proceso = ttk.Button(root, text="Ejecutar Proceso", command=proceso)
btn_limpio = ttk.Button(root, text="Ejecutar Limpio", command=limpio)

# Estilo personalizado para los botones
style.configure("TButton", padding=10, relief="flat", background="#3498db", foreground="white")

# Colocar los botones en la ventana con espaciado
btn_proceso.pack(pady=10)
btn_limpio.pack(pady=10)

# Agregar etiqueta con el texto de autoría
autor_label = tk.Label(root, text="Creado por \n Ian Brahim Chahbouni - ONISTE GIRONA\nUNIDAD INFORMÁTICA JPTGI", font=("Helvetica", 10))
autor_label.pack(pady=20)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
