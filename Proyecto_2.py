def main ():
    print("Seleccione un rol:\n" "A. Para administrar\n""V. Para vender\n""-1. Para finalizar")
    option= str(input())
    while option not in ("A", "V", "-1"):
        print("Opción inválida. Intente nuevamente.")
        option= str(input("Seleccione un rol:\n" "A. Para administrar\n""V. Para vender\n""-1. Para finalizar\n",))
    if option == "A":
        print ("\n","Rol Administrativo")
        administrar ()
    elif option == "V":
        print ("\n","Rol Venta")
        vender ()
    elif option == "-1":
        print ("Programa terminado")

#FUNCION VERDADERA
def busqueda(empresa_suc, buscado):
    if buscado in empresa_suc:
        return True
    else:
        return False  # La sucursal no existe

def administrar ():
    option= str(input("Eliga que operacion desea hacer:\n""add. Agregar sucursal\n""edit. Para modificar algun valor de la empresa\n""H.Para volver al inicio\n",))
    while option not in ("add","edit","H"):
         print("Opción inválida. Intente nuevamente.")
         option= str(input("Eliga que operacion desea hacer:\n""add. Agregar sucursal\n""edit. Para modificar algun valor de la empresa\n""H.Para volver al inicio\n",))
    if option == "add":
        #funcion agregar sucursal
        agregar ()
    elif option == "edit":
        #funcion modificar la empresa
        editar ()
    elif option == "H":
        #funcion Home
        main()


#NECESITA PARAMETROS
def agregar():
    print("En caso de querer volver:\n""H. Para volver a Home\n""Esc. Para volver al rol de Administrar")
    new_suc = input("Ingrese el nombre de la nueva sucursal que desea agregar: ")
    
    if new_suc == "H":
        main()
    elif new_suc == "Esc":
        administrar()
    elif new_suc in empresa_suc:
        print("Sucursal repetida")
    else:
        empresa_suc[new_suc] = {"productos": [], "precios": []}  # Inicializar nueva sucursal con productos y precios vacíos
        print(f"Sucursal '{new_suc}' agregada.")

#NECESITA PARAMETRO
def editar():
    print("En caso de querer volver:\nH. Para volver a Home\nEsc. Para volver al rol de Administrar")
    option = input("Ingrese qué sucursal desea modificar: ")
    while option != "H" and option != "Esc" and option not in empresa_suc:
        print("Sucursal no encontrada. Intente nuevamente.")
        option = input("Ingrese qué sucursal desea modificar: ")
    if option == "H":
        HOME()  # Volver a Home
    elif option == "Esc":
        administrar()  # Volver a Administrar
    elif option in empresa_suc:
        editar_2(option)  # Editar la sucursal seleccionada

            
#NECESITA PARAMETRO
def editar_2(sucursal):
    option_2 = input("Ingrese qué desea modificar\nN. Nombre\nP. Producto\nS. Stock\n")
    
    while option_2 not in ("N", "P", "S"):
        print("Opción inválida. Intente nuevamente.")
        option_2 = input("Ingrese qué desea modificar\nN. Nombre\nP. Producto\nS. Stock\n")

    if option_2 == "N":
        nuevo_nombre = input("Ingrese el nuevo nombre: ")
        
        # Asegurarse de que el nuevo nombre no esté ya en uso
        while nuevo_nombre in empresa_suc:
            print(f"El nombre '{nuevo_nombre}' ya existe. Intente con otro nombre.")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
        
        empresa_suc[nuevo_nombre] = empresa_suc.pop(sucursal)  # Renombrar la sucursal
        print(f"Nombre de la sucursal cambiado a {nuevo_nombre}.")
        
    elif option_2 == "P":
        producto = input("Ingrese el producto a agregar: ")
        precio = float(input("Ingrese el precio del producto: "))
        
        while producto in empresa_suc[sucursal]["productos"]:
            print(f"El producto '{producto}' ya existe en la sucursal.")
            producto = input("Ingrese un nuevo producto a agregar: ")
        
        empresa_suc[sucursal]["productos"].append(producto)
        empresa_suc[sucursal]["precios"].append(precio)
        print(f"Producto '{producto}' agregado con precio {precio}.")
        
    elif option_2 == "S":
        producto = input("Ingrese el producto para modificar su stock: ")
        
        while producto not in empresa_suc[sucursal]["productos"]:
            print(f"Producto '{producto}' no encontrado. Intente nuevamente.")
            producto = input("Ingrese el producto para modificar su stock: ")
        
        indice = empresa_suc[sucursal]["productos"].index(producto)
        nuevo_precio = float(input(f"Ingrese el nuevo precio para '{producto}': "))
        empresa_suc[sucursal]["precios"][indice] = nuevo_precio
        print(f"Precio de '{producto}' actualizado a {nuevo_precio}.")

def vender ():
    option = str(input("Ingrese la sucursal que desee operar:\n""H. Volver a Home\n""<nombre de sucursal> . Para operar esa sucursal\n",))
    pos= busqueda (matriz, option)
    while option not in ("H") or (pos == -1):
        option= str(input("Ingrese la sucursal que desee operar:\n""H. Volver a Home\n""<nombre de sucursal> . Para operar esa sucursal\n",))
        pos= busqueda (matriz, option)
    if option == "H":
        #funcion home
        main()
    else:
        vender_suc(pos,matriz)
        #funcion vender acorde a la sucursal elegida
        #como parametro sera  (matriz, pos) [posicion elegida del sucursal]



if __name__ == "__main__":
    main()


