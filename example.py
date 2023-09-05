import json

# Nombre del archivo JSON
nombre_archivo = 'datos.json'

# Leer el contenido del archivo JSON
with open("mensaje.json", 'r', encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Ahora, puedes acceder a los datos como un diccionario de Python
nombre = datos['nombre']
edad = datos['edad']
ciudad = datos['ciudad']

# Imprimir los datos leídos
print("Nombre:", nombre)
print("Edad:", edad)
print("Ciudad:", ciudad)

# Modificar los datos
datos['edad'] = 31

# Escribir los datos modificados de nuevo en el archivo JSON
with open("mensaje.json", 'w', encoding="utf-8") as archivo:
    json.dump(datos, archivo, indent=4)  # indent para una escritura formateada
