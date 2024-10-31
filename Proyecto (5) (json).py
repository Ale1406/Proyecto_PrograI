import json
import os

# Datos iniciales de la empresa
empresa_suc = [
    ["Sucursal Pedrito", {
        "Pan": (1200, 50),
        "Leche": (1000, 20),
        "Azúcar": (1500, 60),
        "Arroz": (800, 30),
        "Harina": (700, 25)
    }],
    ["Sucursal Juan", {
        "Pan": (1100, 55),
        "Leche": (1050, 22),
        "Café": (900, 35),
        "Yerba": (1200, 40),
        "Galletitas": (750, 50),
        "Aceite": (950, 30)
    }],
    ["Maxi Sucursal", {
        "Pan": (1150, 60),
        "Leche": (1080, 25),
        "Huevos": (1300, 15),
        "Queso": (1600, 45)
    }]
]

# Guardar en JSON
def guardar_datos(empresa_suc, archivo="inventario.json"):
    with open(archivo, "w") as file:
        json.dump(empresa_suc, file, indent=4)
    print("Datos guardados correctamente en JSON.")

# Cargar desde JSON
def cargar_datos(archivo="inventario.json"):
    if os.path.exists(archivo):
        with open(archivo, "r") as file:
            return json.load(file)
    return empresa_suc  # Si el archivo no existe, retorna los datos por defecto

# Funciones del sistema
def busqueda(empresa_suc, buscado):
    for i, sucursal in enumerate(empresa_suc):
        if sucursal[0] == buscado:
            return i
    return -1

def validar_longitud(nombre):
    return len(nombre) <= 15

def long_dic(diccionario):
    return len(diccionario) < 8

def mostrar_inventarios(empresa):
    for almacen in empresa:
        nombre_almacen = almacen[0]
        productos = almacen[1]
        
        print(f"\nInventario de {nombre_almacen}:")
        print(f"{'Producto':<10} {'Cantidad':<10} {'Precio':<10}")  
        for producto, (precio, cantidad) in productos.items():
            print(f"{producto:<10} {cantidad:<10} ${precio:.2f}")  

if __name__ == "__main__":
    # Cargar datos desde JSON al iniciar el programa
    empresa_suc = cargar_datos()
    print("Bienvenido al sistema de inventario.")
    
    # Ejemplo de mostrar el inventario
    mostrar_inventarios(empresa_suc)
    
    # Guardar datos en JSON al finalizar el programa
    guardar_datos(empresa_suc)
