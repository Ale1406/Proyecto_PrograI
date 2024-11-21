##UNITEST
import unittest
from unittest.mock import patch
from main import vender_suc, empresa_suc, volver_a_menu

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

def volver_a_menu_test(accion, func):
    if accion == 0:
        return "Home"
    elif accion == 9:
        func()
        return "Func ejecutada"
    else:
        return "Programa Terminado"

# Prueba 1: Acción "Home"
assert volver_a_menu_test(0, lambda: None) == "Home"

# Prueba 2: Acción "Func ejecutada"
def mock_func():
    global func_called
    func_called = True

func_called = False
assert volver_a_menu_test(9, mock_func) == "Func ejecutada"
assert func_called == True  # Verifica que se ejecutó la función

# Prueba 3: Programa terminado
assert volver_a_menu_test(1, lambda: None) == "Programa Terminado"

def validar_longitud(nombre):
    if len(nombre) > 15:
        print(f"El nombre '{nombre}' es demasiado largo. Debe ser menor a 15 caracteres.")
        return False
    return True

def mostrar_inventarios(empresa):
    for almacen in empresa:
        nombre_almacen = almacen[0]
        productos = almacen[1]
        
        print(f"\nInventario de {nombre_almacen}:")
        print(f"{'Producto':<10} {'Cantidad':<10} {'Precio':<10}")  
        for producto, (precio, cantidad) in productos.items():
            print(f"{producto:<10} {cantidad:<10} ${precio:.2f}")  

#Fucion con longitud de diccionario
def long_dic(diccionario):
    if len(diccionario) >= 8:
        print("El diccionario ya contiene 8 productos. No se pueden agregar más.")
        return False
    return True

def mostrar_sucs ():
    for i in range (len(empresa_suc)):
        print (i+1,". ", empresa_suc[i][0])

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
 

 def editar():
    while True:
        print("\nEn caso de querer volver:\nH. Para volver a Home\nEsc. Para volver al rol de Administrar")
        mostrar_sucs()

        try:
            option = int(input("Ingrese el número de la sucursal a modificar o una opción para volver: "))
        except ValueError:
            print("Error: Debe ingresar un número válido o una opción correcta (H o Esc).")
            continue  
        if option in (0,9,-1):
            volver_a_menu(option, main)

        if 1 <= option <= len(empresa_suc):  
            pos = option - 1 
            editar_2(pos)  
        else:
            print("Número de sucursal no válido. Intente nuevamente.")

class TestEditar(unittest.TestCase):

    @patch('builtins.input', side_effect=[1, 2, 'H'])
    def test_editar(self, mock_input):
        # Simula las entradas para la prueba
        with patch('builtins.print') as mock_print:  # Simula la función print
            # Caso 1: opción válida para editar una sucursal
            editar()
            # Verificamos que se haya llamado a la función 'editar_2' con la posición correcta
            mock_print.assert_any_call("Número de sucursal no válido. Intente nuevamente.")  # Verificación en caso de error

            # Caso 2: opción de volver al menú
            mock_input.assert_any_call("Ingrese el número de la sucursal a modificar o una opción para volver: ")

def agregar():
    while True:
        print("\nEn caso de querer volver:\n0. Para volver a Home\n9. Para volver al rol de Administrar\n-1. Para terminar")
        new_suc = input("Ingrese el nombre de la nueva sucursal que desea agregar: ").strip().title()

        if new_suc in ("0", "9", "-1"):
            volver_a_menu(int(new_suc), Administrativo)
        elif busqueda(empresa_suc, new_suc) != -1:
            print("Sucursal repetida")
        else:
            # COPIA DE LA MATRIZ ACTUAL
            copia_emp = empresa_suc.copy()
            # Lista nueva para agregar
            nueva_suc = [new_suc, {}]
            agregar_productos = True

            while agregar_productos:
                producto = input("Ingrese el producto que desea agregar\nEn caso de no agregar más pulse -1: ").strip().title()

                if producto == "-1":
                    agregar_productos = False  
                    continue 

                if not long_dic(nueva_suc[1]):  # Cambia el límite aquí
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

            print(f"\nSucursal '{new_suc}' agregada con éxito.")

            print("\nInventario de la nueva sucursal agregada:")
            print(empresa_suc[-1])  # Mostrar solo la nueva sucursal

            opcion = input("\n¿Desea mirar todas las sucursales (S/N)? ").strip().upper()
            if opcion in ("S", "SI"):
                print("\nInventario de todas las sucursales ANTES:")
                mostrar_inventarios(copia_emp)  # Mostrar todas las sucursales ANTES
                print("\nInventario de todas las sucursales AHORA:")
                mostrar_inventarios(empresa_suc)  # Mostrar todas las sucursales AHORA

class TestAgregarSucursal(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        'Nueva Sucursal',  # Nombre de la nueva sucursal
        'Producto 1',       # Producto
        '10.50',            # Precio
        '20',               # Stock
        '-1',               # Terminar productos
        'S'                 # ¿Mirar todas las sucursales?
    ])
    @patch('builtins.print')
    def test_agregar_sucursal(self, mock_print, mock_input):
        # Inicializamos el estado de empresa_suc antes de ejecutar la prueba
        empresa_suc.clear()

        # Simulamos el comportamiento de la función agregar
        agregar()

        # Verificamos que la sucursal se haya agregado correctamente
        self.assertEqual(len(empresa_suc), 1)
        self.assertEqual(empresa_suc[0][0], 'Nueva Sucursal')  # Verificamos que el nombre de la sucursal sea correcto
        self.assertIn('Producto 1', empresa_suc[0][1])  # Verificamos que el producto se haya agregado

        # Verificamos que los mensajes correctos fueron impresos
        mock_print.assert_any_call("Sucursal 'Nueva Sucursal' agregada con éxito.")
        mock_print.assert_any_call("Producto 'Producto 1' agregado con precio 10.5 y stock 20.")
        mock_print.assert_any_call("Inventario de la nueva sucursal agregada:")

    @patch('builtins.input', side_effect=[
        'Sucursal Existente',  # Nombre de sucursal repetida
        'Producto 1',           # Producto
        '10.50',                # Precio
        '20',                   # Stock
        '-1'                    # Terminar productos
    ])
    @patch('builtins.print')
    def test_sucursal_repetida(self, mock_print, mock_input):
        # Inicializamos el estado de empresa_suc antes de ejecutar la prueba
        empresa_suc.clear()
        empresa_suc.append(['Sucursal Existente', {}])  # Agregamos una sucursal existente

        # Intentamos agregar una sucursal con el mismo nombre
        agregar()

        # Verificamos que no se haya agregado una sucursal repetida
        self.assertEqual(len(empresa_suc), 1)  # La cantidad de sucursales sigue siendo 1
        mock_print.assert_any_call("Sucursal repetida")


def editar_2(pos):
    while True:
        print(f"\nSucursal seleccionada: {empresa_suc[pos][0]}")
        print("En caso de querer volver:\n0. Para volver a Home\n9. Para volver al rol de Administrar\n-1. Para terminar")

        try:
            option_2 = int(input("Ingrese qué desea modificar:\n1. Nombre\n2. Producto\n3. Stock\n").strip())
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            continue  

        # Comprobar si la opción es volver
        if option_2 in (0, 9, -1):
            volver_a_menu(option_2, Administrativo)

        while option_2 not in (1, 2, 3):
            print("Opción inválida. Intente nuevamente.")
            try:
                option_2 = int(input("Ingrese qué desea modificar:\n1. Nombre\n2. Producto\n3. Stock\n").strip())
            except ValueError:
                print("Error: Debe ingresar un número válido.")

        sucursal = empresa_suc[pos]

        if option_2 == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            
            while busqueda(empresa_suc, nuevo_nombre) != -1:
                print(f"El nombre '{nuevo_nombre}' ya existe. Intente con otro nombre.")
                nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()

            sucursal[0] = nuevo_nombre 
            print(f"Nombre de la sucursal cambiado a {nuevo_nombre}.")

        elif option_2 == 2:
            producto = input("Ingrese el producto a agregar: ").strip()
            if not long_dic(sucursal): 
                print("No se puede agregar más productos a esta sucursal.")
                continue  

            try:
                precio = float(input(f"Ingrese el precio del producto '{producto}': "))
                stock = int(input(f"Ingrese el stock del producto '{producto}': "))
            except ValueError:
                print("Error: Ingrese valores numéricos válidos para el precio y el stock.")
                continue

            if producto in sucursal[1]:
                print(f"El producto '{producto}' ya existe en la sucursal.")
            else:
                sucursal[1][producto] = (precio, stock)  
                print(f"Producto '{producto}' agregado con precio {precio} y stock {stock}.")
            
            opcion = input("\n¿Desea mirar todas las sucursales? (S/N): ").upper()
            if opcion in ("S", "SI"):
                mostrar_inventarios(empresa_suc)

        elif option_2 == 3:
            producto = input("Ingrese el producto para modificar su stock: ").strip()

            if producto not in sucursal[1]:
                print(f"Producto '{producto}' no encontrado.")
            else:
                try:
                    nuevo_precio = float(input(f"Ingrese el nuevo precio para '{producto}': "))
                    nuevo_stock = int(input(f"Ingrese el nuevo stock para '{producto}': "))
                except ValueError:
                    print("Error: Ingrese valores numéricos válidos para el precio y el stock.")
                    continue

                sucursal[1][producto] = (nuevo_precio, nuevo_stock) 
                print(f"Producto '{producto}' actualizado con precio {nuevo_precio} y stock {nuevo_stock}.")

            opcion = input("\n¿Desea mirar todas las sucursales? 1.Si, 0.No : ")
            if opcion == "1":
                mostrar_inventarios(empresa_suc)


class TestEditarSucursal(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '1',  # Opción para cambiar el nombre
        'Sucursal Modificada',  # Nuevo nombre
        '0'  # Opción para no mirar todas las sucursales
    ])
    @patch('builtins.print')
    def test_editar_nombre_sucursal(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal para realizar la prueba
        empresa_suc.clear()
        empresa_suc.append(['Sucursal Original', {}])  # Sucursal a modificar

        # Ejecutamos la función editar_2 con la primera sucursal (índice 0)
        editar_2(0)

        # Verificamos que el nombre de la sucursal haya sido modificado
        self.assertEqual(empresa_suc[0][0], 'Sucursal Modificada')

        # Verificamos que el mensaje correcto fue impreso
        mock_print.assert_any_call("Nombre de la sucursal cambiado a Sucursal Modificada.")

    @patch('builtins.input', side_effect=[
        '2',  # Opción para agregar un producto
        'Producto Nuevo',  # Producto a agregar
        '15.50',  # Precio
        '30',  # Stock
        '0'  # Opción para no mirar todas las sucursales
    ])
    @patch('builtins.print')
    def test_agregar_producto(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal vacía
        empresa_suc.clear()
        empresa_suc.append(['Sucursal para Agregar Producto', {}])  # Sucursal para agregar productos

        # Ejecutamos la función editar_2 con la primera sucursal (índice 0)
        editar_2(0)

        # Verificamos que el producto haya sido agregado correctamente
        self.assertIn('Producto Nuevo', empresa_suc[0][1])  # Verificamos que el producto esté en la sucursal
        self.assertEqual(empresa_suc[0][1]['Producto Nuevo'], (15.50, 30))  # Verificamos que el precio y stock sean correctos

        # Verificamos que el mensaje de producto agregado haya sido impreso
        mock_print.assert_any_call("Producto 'Producto Nuevo' agregado con precio 15.5 y stock 30.")

    @patch('builtins.input', side_effect=[
        '3',  # Opción para modificar el stock
        'Producto Nuevo',  # Producto para modificar
        '20.50',  # Nuevo precio
        '40',  # Nuevo stock
        '1'  # Opción para mirar todas las sucursales
    ])
    @patch('builtins.print')
    def test_modificar_stock_producto(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y un producto para modificar
        empresa_suc.clear()
        empresa_suc.append(['Sucursal con Producto', {'Producto Nuevo': (15.50, 30)}])  # Sucursal con un producto

        # Ejecutamos la función editar_2 con la primera sucursal (índice 0)
        editar_2(0)

        # Verificamos que el precio y stock del producto se hayan modificado correctamente
        self.assertEqual(empresa_suc[0][1]['Producto Nuevo'], (20.50, 40))  # Verificamos que el nuevo precio y stock sean correctos

        # Verificamos que el mensaje de actualización del producto haya sido impreso
        mock_print.assert_any_call("Producto 'Producto Nuevo' actualizado con precio 20.5 y stock 40.")

    @patch('builtins.input', side_effect=[
        '2',  # Opción para agregar un producto
        'Producto Existente',  # Producto a agregar
        '10.50',  # Precio
        '20',  # Stock
        '0'  # Opción para no mirar todas las sucursales
    ])
    @patch('builtins.print')
    def test_producto_existente(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y un producto
        empresa_suc.clear()
        empresa_suc.append(['Sucursal con Producto', {'Producto Existente': (10.50, 20)}])  # Sucursal con un producto

        # Ejecutamos la función editar_2 con la primera sucursal (índice 0)
        editar_2(0)

        # Verificamos que no se haya agregado un producto existente
        self.assertEqual(len(empresa_suc[0][1]), 1)  # Solo debería haber un producto

        # Verificamos que el mensaje de producto existente haya sido impreso
        mock_print.assert_any_call("El producto 'Producto Existente' ya existe en la sucursal.")


def Vender():
    while True:
        print("\nIngrese el número de la sucursal que desee operar:\n0. Volver a Home")
        mostrar_sucs()

        try:
            option = int(input("Ingrese el número de la sucursal a operar o una opción para volver: "))
        except ValueError:
            print("Error: Debe ingresar un número válido o una opción correcta (H o Esc).")
            continue  
        if option in (0,-1):
            volver_a_menu(option,main)
        if 1 <= option <= len(empresa_suc):  
            pos = option - 1  
            vender_suc(pos)  
        else:
            print("Número de sucursal no válido. Intente nuevamente.")


def vender_suc(pos):
    carrito = {} 
    sucursal = empresa_suc[pos][0] 
    productos = empresa_suc[pos][1] 
    contador = 0

    while True:
        if contador == 0:
            print(f"\nOperando en {sucursal}")
        else:
            print("\nSiguiente compra")
 
        try:
            precio_minimo = float(input("Ingrese el precio mínimo para los productos a mostrar (ejemplo: 50): "))
        except ValueError:
            print("Error: Debe ingresar un número válido para el precio.")
            continue

        productos_filtrados = dict(filter(lambda item: item[1][0] >= precio_minimo, productos.items()))

        if not productos_filtrados:
            print(f"No hay productos disponibles con un precio mayor o igual a ${precio_minimo}.")
            continuar = input("¿Desea continuar con otro precio? (S/N): ").strip().upper()
            if continuar == "N":
                break
            else:
                continue

        print("Productos disponibles:")
        for producto, (precio, stock) in productos_filtrados.items():
            print(f"{producto} - Precio: ${precio}, Stock disponible: {stock}")

        producto = input("\nSeleccione un producto o escriba '0' para volver al Home, '9' para volver a selección de sucursal: ").strip()
        
        if producto in ("0","9","-1"):
            volver_a_menu(int(producto), Vender)
            break
        
        if producto not in productos_filtrados:
            print(f"El producto '{producto}' no está disponible o no cumple con el criterio de precio. Intente nuevamente.")
            continue

        stock_disponible = productos_filtrados[producto][1]
        try:
            cantidad = int(input(f"Ingrese la cantidad de '{producto}' que desea comprar (stock disponible: {stock_disponible}): "))
        except ValueError:
            print("Error: Debe ingresar un número válido para la cantidad.")
            continue

        while cantidad > stock_disponible or cantidad <= 0:
            print(f"La cantidad ingresada es inválida. El stock disponible es {stock_disponible}.")
            try:
                cantidad = int(input(f"Ingrese una cantidad válida para '{producto}': "))
            except ValueError:
                print("Error: Debe ingresar un número válido.")
                continue

        if producto in carrito:
            carrito[producto]['cantidad'] += cantidad
        else:
            carrito[producto] = {
                'precio': productos_filtrados[producto][0],
                'cantidad': cantidad 
            }

        productos[producto] = (productos[producto][0], stock_disponible - cantidad)

        continuar = input("¿Desea seguir comprando? (S/N): ").strip().upper()
        if continuar == "N":
            try:
                descuento = float(input("Ingrese el porcentaje de descuento (por ejemplo, 10 para 10%): "))
            except ValueError:
                print("Error: Debe ingresar un valor numérico para el descuento.")
                descuento = 0.0  

            descuento_factor = (100 - descuento) / 100  

            carrito_descuento = list(map(lambda item: (item[0], {'precio': item[1]['precio'] * descuento_factor, 'cantidad': item[1]['cantidad']}), carrito.items()))

            print(f"\nInventario de \"{sucursal}\":")
            print(f"{'Producto':<12} {'Cantidad':<10} {'Precio original':<15} {'Precio con descuento':<20}")
            print('-' * 55) 

            total = 0
            for producto, datos in carrito_descuento:
                precio_total_producto = datos['precio'] * datos['cantidad']
                print(f"{producto:<12} {datos['cantidad']:<10} ${carrito[producto]['precio']:<15.2f} ${datos['precio']:<20.2f}")
                total += precio_total_producto

            print('-' * 55) 
            print(f"Total a pagar (con descuento): ${total:.2f}")  
            contador += 1




class TestVenderSucursal(unittest.TestCase):

    @patch('builtins.input', side_effect=[
        '50',  # Precio mínimo
        'Producto A',  # Producto seleccionado
        '2',  # Cantidad
        'N',  # No seguir comprando
        '10'  # Descuento 10%
    ])
    @patch('builtins.print')
    def test_vender_producto(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y productos
        empresa_suc.clear()
        empresa_suc.append(['Sucursal 1', {
            'Producto A': (60, 10),  # Producto A con precio 60 y stock 10
            'Producto B': (40, 20),  # Producto B con precio 40 y stock 20
        }])  

        # Ejecutamos la función vender_suc con la primera sucursal (índice 0)
        vender_suc(0)

        # Verificamos que el producto fue agregado al carrito
        self.assertIn('Producto A', empresa_suc[0][1])
        self.assertEqual(empresa_suc[0][1]['Producto A'], (60, 8))  # El stock debería haber disminuido en 2

        # Verificamos que el mensaje de carrito y descuento se haya impreso
        mock_print.assert_any_call("Total a pagar (con descuento): $108.00")  # Total con descuento (2 * 60 * 0.9)

    @patch('builtins.input', side_effect=[
        '50',  # Precio mínimo
        'Producto A',  # Producto seleccionado
        '11',  # Intentar comprar más cantidad que el stock disponible
        'N',  # No seguir comprando
        '10'  # Descuento 10%
    ])
    @patch('builtins.print')
    def test_vender_cantidad_invalida(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y productos
        empresa_suc.clear()
        empresa_suc.append(['Sucursal 1', {
            'Producto A': (60, 10),  # Producto A con precio 60 y stock 10
            'Producto B': (40, 20),  # Producto B con precio 40 y stock 20
        }])  

        # Ejecutamos la función vender_suc con la primera sucursal (índice 0)
        vender_suc(0)

        # Verificamos que el producto no fue agregado al carrito debido a la cantidad inválida
        self.assertNotIn('Producto A', empresa_suc[0][1])

        # Verificamos que el mensaje de error de cantidad inválida se haya impreso
        mock_print.assert_any_call("La cantidad ingresada es inválida. El stock disponible es 10.")

    @patch('builtins.input', side_effect=[
        '50',  # Precio mínimo
        'Producto A',  # Producto seleccionado
        '5',  # Cantidad válida
        'S',  # Seguir comprando
        'Producto B',  # Segundo producto
        '5',  # Cantidad del segundo producto
        'N',  # No seguir comprando
        '20'  # Descuento 20%
    ])
    @patch('builtins.print')
    def test_vender_varios_productos(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y productos
        empresa_suc.clear()
        empresa_suc.append(['Sucursal 1', {
            'Producto A': (60, 10),  # Producto A con precio 60 y stock 10
            'Producto B': (40, 20),  # Producto B con precio 40 y stock 20
        }])  

        # Ejecutamos la función vender_suc con la primera sucursal (índice 0)
        vender_suc(0)

        # Verificamos que los productos fueron agregados al carrito
        self.assertIn('Producto A', empresa_suc[0][1])
        self.assertIn('Producto B', empresa_suc[0][1])

        # Verificamos que el inventario se haya actualizado
        self.assertEqual(empresa_suc[0][1]['Producto A'], (60, 5))  # El stock de Producto A debería haber disminuido en 5
        self.assertEqual(empresa_suc[0][1]['Producto B'], (40, 15))  # El stock de Producto B debería haber disminuido en 5

        # Verificamos que el mensaje del total con descuento se haya impreso correctamente
        mock_print.assert_any_call("Total a pagar (con descuento): $162.00")  # Total con descuento (5 * 60 + 5 * 40) * 0.8

    @patch('builtins.input', side_effect=[
        '50',  # Precio mínimo
        'Producto C',  # Producto no disponible
        '0'  # Volver al home
    ])
    @patch('builtins.print')
    def test_producto_no_disponible(self, mock_print, mock_input):
        # Inicializamos empresa_suc con una sucursal y productos
        empresa_suc.clear()
        empresa_suc.append(['Sucursal 1', {
            'Producto A': (60, 10),  # Producto A con precio 60 y stock 10
            'Producto B': (40, 20),  # Producto B con precio 40 y stock 20
        }])  

        # Ejecutamos la función vender_suc con la primera sucursal (índice 0)
        vender_suc(0)

        # Verificamos que el mensaje de producto no disponible se haya impreso
        mock_print.assert_any_call("El producto 'Producto C' no está disponible o no cumple con el criterio de precio. Intente nuevamente.")

if __name__ == '__main__':
    unittest.main()