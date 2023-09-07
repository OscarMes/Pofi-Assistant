import tkinter as tk
import json

def leer_json():
    try:
        with open('mensaje.json', 'r') as archivo:
            datos = json.load(archivo)
            # Actualiza la interfaz de usuario con los datos leídos
            etiqueta.config(text=f'Valor 1: {datos["User"]}, Valor 2: {datos["AI"]}')
    except FileNotFoundError:
        # Manejo de errores si el archivo no se encuentra
        etiqueta.config(text='Archivo JSON no encontrado')
    ventana.after(1000, leer_json)  # Llama a leer_json cada 1000 milisegundos (1 segundo)

# Crear la ventana principal de tkinter
ventana = tk.Tk()
ventana.title('Lectura de JSON en tiempo real')

# Crear una etiqueta para mostrar los datos JSON
etiqueta = tk.Label(ventana, text='', font=('Helvetica', 14))
etiqueta.pack(pady=20)

# Iniciar la lectura JSON
leer_json()

# Iniciar el bucle de tkinter
ventana.mainloop()
