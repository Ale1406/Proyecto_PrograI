# Matriz inicial
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


# Función para volver al menú o ejecutar una función específica
def volver_a_menu(accion, func):
    if accion == "H":
        print ("\nHome")
        main()
    elif accion == "ESC":
        print("\nRol ",func)  # Ejecuta la función pasada como argumento
        func()
    else:
        print("Programa Terminado")

# Función para buscar una sucursal
def busqueda(empresa_suc, buscado):
    for i, sucursal in enumerate(empresa_suc):
        if sucursal[0] == buscado:
            return i  # Retorna el índice de la sucursal
    return -1  # La sucursal no existe

def mostrar_inventarios(empresa):
    for almacen in empresa:
        nombre_almacen = almacen[0]
        productos = almacen[1]
        
        print(f"\nInventario de {nombre_almacen}:")
        print(f"{'Producto':<10} {'Cantidad':<10} {'Precio':<10}")  
        for producto, (precio, cantidad) in productos.items():
            print(f"{producto:<10} {cantidad:<10} ${precio:.2f}")  

#Perfecto
def main():
    print("Seleccione un rol:\nA. Para Administrativo\nV. Para Vender\nE. Para finalizar")
    option = input().strip().upper()
    
    while option not in ("A", "V", "-1"):
        print("Opción inválida. Intente nuevamente.")
        option = input("Seleccione un rol:\nA. Para Administrativo\nV. Para Vender\nE. Para finalizar\n").strip().upper()
    
    if option == "A":
        print("\nRol Administrativo")
        Administrativo()
    elif option == "V":
        print("\nRol Venta")
        Vender()
    elif option == "E":
        print("Programa terminado")



#Perfecto

def Administrativo():
    option = input("Elija qué operación desea hacer:\nadd. Agregar sucursal\nedit. Para modificar un valor\nH. Para volver al inicio\n").strip().upper()
    
    while option not in ("ADD", "EDIT", "H","E"):
        print("Opción inválida. Intente nuevamente.")
        option = input("Elija qué operación desea hacer:\nadd. Agregar sucursal\nedit. Para modificar un valor\nH. Para volver al inicio\n").strip().upper()
    
    if option == "ADD":
        agregar()
    elif option == "EDIT":
        editar()
    else:
        volver_a_menu(option, main)
        
#Falta agregar sucursal, luego 

def agregar():
    while True:
        print("\nEn caso de querer volver:\nH. Para volver a Home\nEsc. Para volver al rol de Administrar")
        new_suc = input("Ingrese el nombre de la nueva sucursal que desea agregar: ").strip().upper()

        if new_suc in ("H", "ESC"):
            volver_a_menu(new_suc, Administrativo)
        elif busqueda(empresa_suc, new_suc) != -1:
            print("Sucursal repetida")
        else:
            empresa_suc.append([new_suc, {}])  # Inicializar nueva sucursal con productos vacíos
            print(f"Sucursal '{new_suc}' agregada.")
            opcion= input("\nDesea mirar todas las sucursales:\n").upper()
            if opcion in ("S","SI"):
                mostrar_inventarios(empresa_suc)


#Perfecto

def editar():
    print("\nEn caso de querer volver:\nH. Para volver a Home\nEsc. Para volver al rol de Administrar")
    option = input("Ingrese el nombre de la sucursal a modificar: ").strip()

    pos = busqueda(empresa_suc, option)

    while option.upper() not in ("H", "ESC") and pos == -1:
        print("Sucursal no encontrada. Intente nuevamente.")
        option = input("Ingrese el nombre de la sucursal a modificar: ").strip()
        pos = busqueda(empresa_suc, option)

    if option.upper() in ("H", "ESC"):
        volver_a_menu(option, Administrativo)
    else:
        editar_2(pos) # Editar la sucursal seleccionada

#Perfecto
#fALTA MOSTRAR MATRIZ FINAL
def editar_2(pos):
    while True:
        print("\n",empresa_suc[pos][0])
        print("En caso de querer volver:\nH. Para volver a Home\nEsc. Para volver al rol de Administrar")
        option_2 = input("Ingrese qué desea modificar\nN. Nombre\nP. Producto\nS. Stock\n").strip().upper()
    
        if option_2 in("H","ESC"):
            volver_a_menu(option_2, Administrativo)

        while option_2 not in ("N", "P", "S", "H", "ESC"):
            print("Opción inválida. Intente nuevamente.")
            option_2 = input("Ingrese qué desea modificar\nN. Nombre\nP. Producto\nS. Stock\nH. Volver a Home\nEsc. Volver a Ventas\n").strip().upper()
    
        sucursal = empresa_suc[pos]  # Obtener la sucursal seleccionada
    
        if option_2 == "N":
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
        
            while busqueda(empresa_suc, nuevo_nombre) != -1:
                print(f"El nombre '{nuevo_nombre}' ya existe. Intente con otro nombre.")
                nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
        
            sucursal[0] = nuevo_nombre  # Cambiar el nombre de la sucursal
            print(f"Nombre de la sucursal cambiado a {nuevo_nombre}.")
        
        elif option_2 == "P":
            producto = input("Ingrese el producto a agregar: ").strip()
            precio = float(input("Ingrese el precio del producto: "))
            stock = int(input("Ingrese el stock del producto: "))
        
            if producto in sucursal[1]:
                print(f"El producto '{producto}' ya existe en la sucursal.")
            else:
                sucursal[1][producto] = (precio, stock)  # Agregar el nuevo producto con precio y stock
                print(f"Producto '{producto}' agregado con precio {precio} y stock {stock}.")
            opcion= input("\nDesea mirar todas las sucursales:\n").upper()
            if opcion in ("S","SI"):
                mostrar_inventarios(empresa_suc)
        
        elif option_2 == "S":
            producto = input("Ingrese el producto para modificar su stock: ").strip()
        
            if producto not in sucursal[1]:
                print(f"Producto '{producto}' no encontrado.")
            else:
                nuevo_precio = float(input(f"Ingrese el nuevo precio para '{producto}': "))
                nuevo_stock = int(input(f"Ingrese el nuevo stock para '{producto}': "))
                sucursal[1][producto] = (nuevo_precio, nuevo_stock)  # Actualizar el precio y el stock del producto
                print(f"Producto '{producto}' actualizado con precio {nuevo_precio} y stock {nuevo_stock}.")
            opcion= input("\nDesea mirar todas las sucursales:\n").upper()
            if opcion in ("S","SI"):
                mostrar_inventarios(empresa_suc)


def Vender():
    option = input("Ingrese la sucursal que desee operar:\nH. Volver a Home\n<nombre de sucursal> para operar esa sucursal\n").strip()
    pos = busqueda(empresa_suc, option)
    
    while option.upper() not in ("H","E") and pos == -1:
        print("Sucursal no encontrada. Intente nuevamente.")
        option = input("Ingrese la sucursal que desee operar:\nH. Volver a Home\n<nombre de sucursal> para operar esa sucursal\n").strip()
        pos = busqueda(empresa_suc, option)
    
    if pos != -1:
        vender_suc(pos)
    else:
        volver_a_menu(option,main)

def vender_suc(pos):
    carrito = {}  # Carrito donde se almacenan los productos y cantidades
    sucursal = empresa_suc[pos][0]  # Nombre de la sucursal
    productos = empresa_suc[pos][1]  # Diccionario de productos de la sucursal
    contador = 0

    while True:
        if contador == 0:
            print(f"\nOperando en {sucursal}. Para salir, escriba 'H' o 'Esc'.")
        else:
            print ("\n Siguiente compra")
        print("Productos disponibles:")
        for producto, (precio, stock) in productos.items():
            print(f"{producto} - Precio: ${precio}, Stock disponible: {stock}")

        producto = input("\nSeleccione un producto o escriba 'H' para volver a Home, 'Esc' para volver a selección de sucursal: ").strip()
        
        if producto in ("H", "Esc"):
            volver_a_menu(producto, vender)
            return

        if producto not in productos:
            print(f"El producto '{producto}' no está disponible. Intente nuevamente.")
            continue

        # Obtener la cantidad de stock a comprar
        stock_disponible = productos[producto][1]
        cantidad = int(input(f"Ingrese la cantidad de '{producto}' que desea comprar (stock disponible: {stock_disponible}): "))

        while cantidad > stock_disponible or cantidad <= 0:
            print(f"La cantidad ingresada es inválida. El stock disponible es {stock_disponible}.")
            cantidad = int(input(f"Ingrese una cantidad válida para '{producto}': "))

        # Actualizar el carrito con el producto seleccionado
        if producto in carrito:
            carrito[producto]['cantidad'] += cantidad
        else:
            carrito[producto] = {
                'precio': productos[producto][0],  # Precio del producto
                'cantidad': cantidad  # Cantidad seleccionada
            }

        # Restar el stock disponible
        productos[producto] = (productos[producto][0], stock_disponible - cantidad)

        # Preguntar si quiere seguir comprando o finalizar
        continuar = input("¿Desea seguir comprando? (S/N): ").strip().upper()
        if continuar == "N":
            # Mostrar el comprobante al finalizar la compra
            print(f"\nInventario de \"{sucursal}\":")
            print(f"{'Producto':<12} {'Cantidad':<10} {'Precio':<10}")
            print('-' * 35)  # Línea separadora

            total = 0
            for producto, datos in carrito.items():
                precio_total_producto = datos['precio'] * datos['cantidad']
                print(f"{producto:<12} {datos['cantidad']:<10} ${datos['precio']:<10.2f}")  # Formato con dos decimales
                total += precio_total_producto

            print('-' * 35)  # Línea separadora
            print(f"Total a pagar: ${total:.2f}")  # Total con dos decimales
            contador+= 1




if __name__ == "__main__":
    main()
