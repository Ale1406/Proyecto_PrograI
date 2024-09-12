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
    print("Seleccione un rol:",/n,"1.Administrar")
    option= input("Elige el rol que desee tomar: "A" Para administrar ; "V" Para vender " ; "-1" para finalizar,)
    while option != ("A" or "V" or "-1"):
        option= input("Elige el rol que desee tomar: "A" Para administrar ; "V" Para vender " ; "-1" para finalizar,)
    if option == "A":
        #funcion de administracion
    elif option == "V":
        #funcion para vender
    elif option == "-1":
        print ("Programa terminado")



def busqueda (matriz,buscado):
    n= len (matriz) -1
    while n>-1 and (matriz[0][n]!= buscado):
        n_=1
    return n 

def administrar ():
    option = input("Elige que operacion quieres hacer: "add" Agregar sucursal ; "edit" Para modificar algun valor de la empresa ; "H" Para volver al inicio", )
    while option != ("add" or "edit" or  "H"):
        option = input("Elige que operacion quieres hacer: "add" Agregar sucursal ; "edit" Para modificar algun valor de la empresa ; "H" Para volver al inicio", )
    if option == "add":
        #funcion agregar sucursal
    elif option == "edit":
        #funcion modificar la empresa
    elif option == "H":
        #funcion Home

def vender ():
    option= input ("Ingrese la sucursal que desee operar: ", )
    pos= busqueda (matriz, option)
    while (pos == "-1") and (option != "H"):
        option= input ("Ingrese la sucursal que desee operar: ", )
        pos= busqueda (matriz, option)
    if option == "H":
        #funcion home
    else:
        #funcion vender acorde a la sucursal elegida
        #como parametro sera  (matriz, pos) [posicion elegida del sucursal]


def agregar (empresa):
    new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", ) #"H" para volver a home y "Esc " para volver a administrar
    pos= busqueda (empresa, new_suc)
    while (pos != "-1") and (new_suc != ("H" or "Esc")):
        new_suc= input("Ingrese el nombre de la nueva sucursal que desea agregar: ", )
        pos= busqueda (empresa, new_suc)
    if new_suc == "H":
        #Funcion home
    elif new_suc == "Esc":
        #Funcion administrar
    else:
        empresa.append (new_suc)
    
                             

abc= HOME()