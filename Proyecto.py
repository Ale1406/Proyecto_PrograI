"""
Primero necesitamos tener los datos para el almacen. 
El ´plan original es administrar las sucursales de una empresa,
 osea que necesitamos una matriz para cada empresa. 
 Primero necesitamos los nombres de la sucursal, 
 pero primero tenemos que tener 
"""
#1° DEFINIR q quiere hacer el operador esta entre

#Add= agregar una sucursal 
#Select= Elegir la suursal q desea administrar
#AdMs= Administrar los productos de la sucursal elegida
#Edit: Modificar productos de la sucursal elegida
#Vent= Cajero corriente

#No se puede hacer todo ahora porque "no podemosusar archivos como recurso(porahora)"

#Para este proyecto hace falta 2 funciones principales:
#HOME: donde esta el inincio: donde tiene la opcion de administrar o vender
#Esc: Dnde estas al inicio de la opcion q elegiste (administrar o vender)
#



def HOME ():
    print("Seleccione un rol:\n" "A. Para administrar\n""V. Para vender\n""-1. Para finalizar")
    option= str(input())
    while option not in ("A", "V", "-1"):
        print("Opción inválida. Intente nuevamente.")
        option= str(input("Seleccione un rol:\n" "A. Para administrar\n""V. Para vender\n""-1. Para finalizar\n",))
    if option == "A":
        print ("Rol Administrativo")
        administrar ()
    elif option == "V":
        print ("Rol Venta")
        vender ()
    elif option == "-1":
        print ("Programa terminado")

#PRIMER PARTE DEL PROGRAMA
def busqueda (matriz,buscado):
    n= len (matriz) -1
    while n>-1 and (matriz[0][n]!= buscado):
        n_=1
    return n 

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
        HOME()

def agregar():
    print ("En caso de querer volver:\n""H. Para volver a Home\n""Esc. Para volver al rol de Administrar")
    new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", ) #"H" para volver a home y "Esc " para volver a administrar
    pos= busqueda (empresa, new_suc)
    while new_suc not in ("H","Esc"):
        if new_suc == "H":
            #Funcion home
            HOME()
        elif new_suc == "Esc":
            #Funcion Administrar
            administrar ()
        elif pos == -1:
            print("Sucursal repetida")
        else:
            empresa.append (new_suc)
        new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", ) #"H" para volver a home y "Esc " para volver a administrar
        pos= busqueda (empresa, new_suc)


def editar ():
    print ("En caso de querer volver:\n""H. Para volver a Home\n""Esc. Para volver al rol de Administrar")
    option=input("Ingrese que sucursal desea modificar:",)
    pos= busqueda (empresa, option)
    while option not in ("H","Esc"):
        if option == "H":
            #Funcion home
            HOME()
        elif new_suc == "Esc":
            #Funcion Administrar
            administrar ()
        elif pos == -1:
            print("Sucursal no encontrada")
        else:
            editar_2 () #Con pos como la posicion de la matriz
            

def editar_2 ():
    option_2= input("Ingrese que desea modificar\n""N. Nombre\n""P. Producto\n""S. Stock",)
    while option_2 not in ("N","P","S"):
        


def vender ():
    option = str(input("Ingrese la sucursal que desee operar:\n""H. Volver a Home\n""<nombre de sucursal> . Para operar esa sucursal\n",))
    pos= busqueda (matriz, option)
    while option not in ("H") or (pos == -1):
        option= str(input("Ingrese la sucursal que desee operar:\n""H. Volver a Home\n""<nombre de sucursal> . Para operar esa sucursal\n",))
        pos= busqueda (matriz, option)
    if option == "H":
        #funcion home
        HOME()
    else:
        vender_suc(pos,matriz)
        #funcion vender acorde a la sucursal elegida
        #como parametro sera  (matriz, pos) [posicion elegida del sucursal]



def vender_suc (pos,matriz):
    return("Hola")






#AL FINAL
abc=HOME()
empresa_suc=[]



def agregar():
    print ("En caso de querer volver:\n""H. Para volver a Home\n""Esc. Para volver al rol de Administrar")
    new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", ) #"H" para volver a home y "Esc " para volver a administrar
    pos= busqueda (empresa, new_suc)
    while new_suc not in ("H","Esc"):
        if new_suc == "H":
            #Funcion home
            HOME()
        elif new_suc == "Esc":
            #Funcion Administrar
            administrar ()
        elif pos == -1:
            print("Sucursal repetida")
        else:
            empresa.append (new_suc)
        new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", ) #"H" para volver a home y "Esc " para volver a administrar
        pos= busqueda (empresa, new_suc)