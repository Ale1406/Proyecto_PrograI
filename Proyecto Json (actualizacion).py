import json

# Archivo JSON donde se guardarán las sucursales
ARCHIVO_JSON = "sucursales.json"

# Cargar datos desde JSON al inicio del programa
def cargar_sucursales():
    try:
        with open(ARCHIVO_JSON, "r") as archivo:
            datos = json.load(archivo)
            # Convertir listas de precios/stock a tuplas
            for sucursal in datos:
                for producto, valores in sucursal["Productos"].items():
                    sucursal["Productos"][producto] = tuple(valores)
            return [[suc["Sucursal"], suc["Productos"]] for suc in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, retornar la matriz inicial
        print("Archivo JSON no encontrado o vacío. Usando datos iniciales.")
        return [
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

# Guardar datos en JSON después de modificaciones
def guardar_sucursales(empresa_suc):
    datos = []
    for sucursal in empresa_suc:
        datos.append({
            "Sucursal": sucursal[0],
            "Productos": {producto: list(valores) for producto, valores in sucursal[1].items()}
        })
    with open(ARCHIVO_JSON, "w") as archivo:
        json.dump(datos, archivo, indent=4)
    print("Cambios guardados en el archivo JSON.")

# Inicialización de las sucursales al cargar el programa
empresa_suc = cargar_sucursales()

# Función para no repetir la misma condición
def volver_a_menu(accion, func):
    if accion == 0:
        print("\nHome")
        main()
    elif accion == 9:
        print("\nRol ", func) 
        func()
    else:
        print("Programa Terminado")
        exit() 

# Función para buscar una sucursal por nombre
def busqueda(empresa_suc, buscado):
    for i in range(len(empresa_suc)):
        if empresa_suc[i][0] == buscado:
            return i  # Retorna el índice de la sucursal
    return -1  # La sucursal no existe

# Función para mostrar inventarios
def mostrar_inventarios(empresa):
    for almacen in empresa:
        nombre_almacen = almacen[0]
        productos = almacen[1]
        
        print(f"\nInventario de {nombre_almacen}:")
        print(f"{'Producto':<10} {'Cantidad':<10} {'Precio':<10}")  
        for producto, (precio, cantidad) in productos.items():
            print(f"{producto:<10} {cantidad:<10} ${precio:.2f}")  

# Función para verificar la longitud del diccionario de productos
def long_dic(diccionario):
    if len(diccionario) >= 8:
        print("El diccionario ya contiene 8 productos. No se pueden agregar más.")
        return False
    return True

def mostrar_sucs():
    for i in range(len(empresa_suc)):
        print(i + 1, ". ", empresa_suc[i][0])

def main():
    while True:
        try:
            option = int(input("Seleccione un rol:\n1. Para Administrativo\n2. Para Vender\n-1. Para finalizar\n").strip())
            if option == -1:
                print("Programa terminado")
                break
            elif option == 1:
                print("\nRol Administrativo")
                Administrativo()
            elif option == 2:
                print("\nRol Venta")
                Vender()
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Error: No ingresaste un número entero. Intenta de nuevo.")

def Administrativo():
    while True:
        try:
            option = int(input("Elija qué operación desea hacer:\n1. Agregar sucursal\n2. Modificar un valor\n0. Volver al inicio\n").strip())
            if option == 1:
                agregar()
            elif option == 2:
                editar()
            elif option == 0:
                print("Volviendo al menú principal...")
                main()
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Error: No ingresaste un número entero. Intenta de nuevo.")

def agregar():
    while True:
        print("\nEn caso de querer volver:\n0. Para volver a Home\n9. Para volver al rol de Administrar\n-1. Para terminar")
        new_suc = input("Ingrese el nombre de la nueva sucursal que desea agregar: ").strip().title()

        if new_suc in ("0", "9", "-1"):
            volver_a_menu(int(new_suc), Administrativo)
        elif busqueda(empresa_suc, new_suc) != -1:
            print("Sucursal repetida")
        else:
            nueva_suc = [new_suc, {}]
            agregar_productos = True

            while agregar_productos:
                producto = input("Ingrese el producto que desea agregar\nEn caso de no agregar más pulse -1: ").strip().title()
                if producto == "-1":
                    agregar_productos = False
                    continue
                if not long_dic(nueva_suc[1]):
                    print("No se puede agregar más productos a esta sucursal.")
                    continue
                try:
                    precio = float(input(f"Ingrese el precio del producto '{producto}': "))
                    stock = int(input(f"Ingrese el stock del producto '{producto}': "))
                except ValueError:
                    print("Error: Ingrese valores numéricos válidos para el precio y el stock.")
                    continue
                if producto in nueva_suc[1]:
                    print(f"El producto '{producto}' ya existe en la sucursal.")
                else:
                    nueva_suc[1][producto] = (precio, stock)
                    print(f"Producto '{producto}' agregado con precio {precio} y stock {stock}.")
            empresa_suc.append(nueva_suc)
            guardar_sucursales(empresa_suc)
            print(f"\nSucursal '{new_suc}' agregada con éxito.")
            mostrar_inventarios(empresa_suc)

# Las demás funciones se mantienen igual...

if __name__ == "__main__":
    main()
