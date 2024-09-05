def crear_almacen(nombre):
    almacenes.append([nombre, []])  # El segundo elemento de la lista es una lista vacía para los productos

def agregar_producto(almacen, producto):
    for alm in almacenes:
        if alm[0] == almacen:
            alm[1].append(producto)
            return
    print("Almacén no encontrado")

# Lista principal de almacenes
almacenes = []

# Ejemplo de uso
crear_almacen("Almacen Central")
agregar_producto("Almacen Central", "Manzanas")
agregar_producto("Almacen Central", "Bananas")

def consultar_stock(almacen, producto):
    for alm in almacenes:
        if alm[0] == almacen:
            for prod in alm[1]:
                if prod == producto:
                    return True  # Producto encontrado
    return False

def eliminar_producto(almacen, producto):
    for alm in almacenes:
        if alm[0] == almacen:
            alm[1].remove(producto)
            return
    print("Almacén o producto no encontrado")

def mostrar_inventario(almacen):
    for alm in almacenes:
        if alm[0] == almacen:
            print("Inventario de", almacen)
            for prod in alm[1]:
                print(prod)

def registrar_movimiento(almacen, producto, cantidad, tipo):
    for alm in almacenes:
        if alm[0] == almacen:
            for i, prod in enumerate(alm[1]):
                if prod[0] == producto:
                    alm[1][i] = (prod[0], prod[1] + cantidad if tipo == "entrada" else prod[1] - cantidad)
                    alm[1].append((fecha_actual(), cantidad, tipo))  # Agregar el movimiento al historial