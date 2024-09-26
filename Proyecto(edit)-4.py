almacenes = [
    [
        "Almacén Avellaneda",  
        {  
            "Pan": (50, 10.99), 
            "Manteca": (30, 5.49),
            "Leche": (20, 15.00),
            "Huevos": (10, 7.25)
        }
    ],
    [
        "Almacén Palermo",  
        {  
            "Harina": (15, 12.00),
            "Avena": (25, 6.75),
            "Palta": (5, 20.00),
            "Banana": (40, 3.50)
        }
    ],
    [
        "Almacén Barracas",  
        {  
            "Manzana": (15, 12.00),
            "Naranja": (25, 6.75),
            "Uva": (5, 20.00),
            "Mandarina": (40, 3.50)
        }
    ]
]


def ingresar_valor(tipo):
    valor = -1
    while valor <= 0:
        valor = input(f"Ingrese el {tipo} : ")
        if valor.replace('.', '', 1).isdigit():
            valor = float(valor)
            if valor <= 0:
                print(f"El {tipo} es invalido")
        else:
            print("ingrese un número valido")
            valor = -1
    return valor


def ingresar_entero_positivo(tipo):
    valor = -1
    while valor <= 0:
        valor = input(f"Ingrese la {tipo} : ")
        if valor.isdigit():
            valor = int(valor)
            if valor <= 0:
                print(f"La {tipo} es invalido")
        else:
            print("ingrese un número entero valido")
            valor = -1
    return valor


def mostrar_productos(almacen):
    productos = list(almacen[1].items())
    print(f"Productos en {almacen[0]}:")
    for i in range(len(productos)):
        producto = productos[i]
        nombre, (stock, precio) = producto
        print(f"{i + 1}. {nombre} (Stock: {stock}, Precio: ${precio:.2f})")
    return productos


def buscar_almacen(numero):
    if 1 <= numero <= len(almacenes):
        return almacenes[numero - 1]
    else:
        return None


def modificar_precio(numero_almacen):
    almacen = buscar_almacen(numero_almacen)
    if almacen:
        productos = mostrar_productos(almacen)
        numero_producto = input("Ingrese producto que desea modificar el precio: ")
        if numero_producto.isdigit():
            numero_producto = int(numero_producto)
            if 1 <= numero_producto <= len(productos):
                producto_seleccionado = productos[numero_producto - 1]
                nombre_producto = producto_seleccionado[0]

                
                nuevo_precio = ingresar_valor("Ingrese nuevo precio")
                
                
                stock_actual = producto_seleccionado[1][0]
                almacen[1][nombre_producto] = (stock_actual, nuevo_precio)
                print(f"El precio de '{nombre_producto}' se ha modificado en {almacen[0]}.")
            else:
                print("Número de producto invalido")
        else:
            print("Numero invalido, ingrese el numero de un poducto")
    else:
        print("Numero de almacen invalido.")


def agregar_producto(numero_almacen):
    almacen = buscar_almacen(numero_almacen)
    if almacen:
        productos = mostrar_productos(almacen)  
        
        producto = input("Ingrese el nombre del nuevo producto: ")
        if producto in almacen[1]:
            print("El producto ya existe")
        else:
            precio = ingresar_valor("Precio")
            stock = ingresar_entero_positivo("Cantidad en stock")
            almacen[1][producto] = (stock, precio)
            print(f"El producto '{producto}'Fue agregado al {almacen[0]}")
    else:
        print("Numero de alamacen inexistente, ingrese de nuevo un almacen")


def agregar_stock(numero_almacen):
    almacen = buscar_almacen(numero_almacen)
    if almacen:
        productos = mostrar_productos(almacen)
        numero_producto = input("Ingrese el numero del producto al que desea agregar stock: ")
        if numero_producto.isdigit():
            numero_producto = int(numero_producto)
            if 1 <= numero_producto <= len(productos):
                producto_seleccionado = productos[numero_producto - 1]
                nombre_producto = producto_seleccionado[0]
                stock_actual = producto_seleccionado[1][0]

                
                cantidad_agregar = ingresar_entero_positivo("cantidad a agregar")
                nuevo_stock = stock_actual + cantidad_agregar
                precio_actual = producto_seleccionado[1][1]

                
                almacen[1][nombre_producto] = (nuevo_stock, precio_actual)
                print(f"El stock de '{nombre_producto}' ahora es {nuevo_stock} en el {almacen[0]}")
            else:
                print("Número de producto invalido")
        else:
            print("Numero invalido, ingresar de nuevo")
    else:
        print("Numero de alamacen inexistente, ingrese de nuevo un almacen")


def realizar_venta(numero_almacen):
    almacen = buscar_almacen(numero_almacen)
    if almacen:
        productos = mostrar_productos(almacen)
        numero_producto = input("Ingrese el numero del producto que se vendio: ")
        if numero_producto.isdigit():
            numero_producto = int(numero_producto)
            if 1 <= numero_producto <= len(productos):
                producto_seleccionado = productos[numero_producto - 1]
                nombre_producto = producto_seleccionado[0]
                stock_actual, precio = producto_seleccionado[1]
                
                
                cantidad = ingresar_entero_positivo("cantidad de venta")
                if cantidad <= stock_actual:
                    nuevo_stock = stock_actual - cantidad
                    almacen[1][nombre_producto] = (nuevo_stock, precio)
                    total_venta = cantidad * precio
                    print(f"La venta fue realizada Total: ${total_venta:.2f}")
                    print(f"Stock restante de '{nombre_producto}': {nuevo_stock}")
                else:
                    print("Stock insuficiente para realizar la venta")
            else:
                print("Numero de producto invalido")
        else:
            print("Numero invalido, ingresar de nuevo")
    else:
        print("Numero de alamacen inexistente, ingrese de nuevo un almacen")


def administrar():
    mostrar_almacenes()
    numero_almacen = input("Ingrese el numero del almacen que desea administrar: ")
    if numero_almacen.isdigit():
        numero_almacen = int(numero_almacen)
        almacen = buscar_almacen(numero_almacen)
        
        if almacen:
            opcion = input("¿Que desea hacer?\n1. Agregar producto\n2. Modificar precio\n3. Agregar stock\n4. Realizar venta\n")
            if opcion == "1":
                agregar_producto(numero_almacen)
            elif opcion == "2":
                modificar_precio(numero_almacen)
            elif opcion == "3":
                agregar_stock(numero_almacen)
            elif opcion == "4":
                realizar_venta(numero_almacen)
            else:
                print("Opcion invalida")
        else:
            print("Numero de almacen inexistente")
    else:
        print("Numero invalido, ingrese un numero valido")


def mostrar_almacenes():
    print("Almacenes disponibles:")
    for i in range(len(almacenes)):
        almacen = almacenes[i]
        print(f"{i + 1}. {almacen[0]}")

    
def ver_productos():
    mostrar_almacenes()
    numero_almacen = int(input("Seleccione el numero del almacen que desea ver: "))
    almacen = buscar_almacen(numero_almacen)
    
    if almacen:
        mostrar_productos(almacen)
    else:
        print("Numero de almacen invalido")

def HOME():
    while True:
        print("Seleccione una opcion:")
        print("1. Ver productos de un almacen")
        print("2. Administrar almacenes")
        print("3. Realizar ventas")
        print("-1. Finalizar carga")
        option = int(input())
        if option == 1:
            ver_productos()
        elif option == 2:
            print("Rol Administrativo")
            administrar()
        elif option == 3:
            mostrar_almacenes()
            numero_almacen = int(input("Ingrese el numero del almacen para realizar una venta: "))
            realizar_venta(numero_almacen)
        elif option == -1:
            print("Programa terminado.")
            return  
        else:
            print("Opción invalida, intetelo nuevamente")


HOME()


