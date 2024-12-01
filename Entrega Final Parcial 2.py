import tkinter as tk
from tkinter import messagebox, simpledialog
import json

ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

# Funciones de manejo de JSON
def cargar_sucursales():
    try:
        with open(ARCHIVO_JSON, "r") as archivo:
            datos = json.load(archivo)
            for sucursal in datos:
                for producto, valores in sucursal["Productos"].items():
                    sucursal["Productos"][producto] = tuple(valores)
            return [[suc["Sucursal"], suc["Productos"]] for suc in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_sucursales(empresa_suc):
    datos = []
    for sucursal in empresa_suc:
        datos.append({
            "Sucursal": sucursal[0],
            "Productos": {producto: list(valores) for producto, valores in sucursal[1].items()}
        })
    with open(ARCHIVO_JSON, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_usuarios():
    try:
        with open(USUARIOS_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

empresa_suc = cargar_sucursales()

# Funciones de la ventana administrativa
def mostrar_inventarios():
    sucursales_list.delete(0, tk.END)
    for sucursal in empresa_suc:
        sucursales_list.insert(tk.END, sucursal[0])

def agregar_sucursal():
    nueva_sucursal = simpledialog.askstring("Agregar Sucursal", "Ingrese el nombre de la nueva sucursal:")
    if not nueva_sucursal:
        return
    if any(suc[0] == nueva_sucursal for suc in empresa_suc):
        messagebox.showerror("Error", "La sucursal ya existe.")
        return
    empresa_suc.append([nueva_sucursal, {}])
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", f"Sucursal '{nueva_sucursal}' agregada correctamente.")

def eliminar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una sucursal.")
        return
    indice = seleccion[0]
    sucursal_eliminada = empresa_suc.pop(indice)
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", f"Sucursal '{sucursal_eliminada[0]}' eliminada correctamente.")

def realizar_venta_desde_administrativa():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una sucursal.")
        return
    indice = seleccion[0]
    sucursal = empresa_suc[indice]

    ventana_venta = tk.Toplevel(ventana_administrativa)
    ventana_venta.title(f"Venta - {sucursal[0]}")
    ventana_venta.geometry("400x400")

    productos_list = tk.Listbox(ventana_venta, width=50)
    productos_list.pack(pady=10)

    for producto, (precio, stock) in sucursal[1].items():
        productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")

    def realizar_venta():
        seleccion_producto = productos_list.curselection()
        if not seleccion_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto para vender.")
            return
        producto_seleccionado = productos_list.get(seleccion_producto).split(" - ")[0]
        cantidad_str = simpledialog.askstring("Venta", f"Ingrese la cantidad a vender de '{producto_seleccionado}':")
        if not cantidad_str:
            return
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return
        precio, stock = sucursal[1][producto_seleccionado]
        if cantidad > stock:
            messagebox.showerror("Error", "Stock insuficiente para realizar la venta.")
            return
        sucursal[1][producto_seleccionado] = (precio, stock - cantidad)
        guardar_sucursales(empresa_suc)
        productos_list.delete(0, tk.END)
        for producto, (precio, stock) in sucursal[1].items():
            productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")
        messagebox.showinfo("Éxito", f"Venta realizada: {cantidad} unidades de '{producto_seleccionado}'.")

    tk.Button(ventana_venta, text="Realizar Venta", command=realizar_venta).pack(pady=10)

def editar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una sucursal.")
        return
    indice = seleccion[0]
    sucursal = empresa_suc[indice]

    ventana_editar = tk.Toplevel(ventana_administrativa)
    ventana_editar.title(f"Editar {sucursal[0]}")
    ventana_editar.geometry("400x400")

    productos_list = tk.Listbox(ventana_editar, width=50)
    productos_list.pack(pady=10)

    def actualizar_productos_list():
        productos_list.delete(0, tk.END)
        for producto, (precio, stock) in sucursal[1].items():
            productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")

    def agregar_producto():
        nuevo_producto = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
        if not nuevo_producto:
            return
        if nuevo_producto in sucursal[1]:
            messagebox.showerror("Error", "El producto ya existe.")
            return
        try:
            precio = float(simpledialog.askstring("Precio", f"Ingrese el precio de '{nuevo_producto}':"))
            stock = int(simpledialog.askstring("Stock", f"Ingrese el stock de '{nuevo_producto}':"))
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos.")
            return
        sucursal[1][nuevo_producto] = (precio, stock)
        guardar_sucursales(empresa_suc)
        actualizar_productos_list()
        messagebox.showinfo("Éxito", f"Producto '{nuevo_producto}' agregado correctamente.")

    def editar_producto():
        seleccion_producto = productos_list.curselection()
        if not seleccion_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return
        producto_seleccionado = productos_list.get(seleccion_producto).split(" - ")[0]
        try:
            nuevo_precio = float(simpledialog.askstring("Precio", f"Ingrese el nuevo precio de '{producto_seleccionado}':"))
            nuevo_stock = int(simpledialog.askstring("Stock", f"Ingrese el nuevo stock de '{producto_seleccionado}':"))
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos.")
            return
        sucursal[1][producto_seleccionado] = (nuevo_precio, nuevo_stock)
        guardar_sucursales(empresa_suc)
        actualizar_productos_list()
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' actualizado correctamente.")

    def eliminar_producto():
        seleccion_producto = productos_list.curselection()
        if not seleccion_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return
        producto_seleccionado = productos_list.get(seleccion_producto).split(" - ")[0]
        del sucursal[1][producto_seleccionado]
        guardar_sucursales(empresa_suc)
        actualizar_productos_list()
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' eliminado correctamente.")

    tk.Button(ventana_editar, text="Agregar Producto", command=agregar_producto).pack(pady=5)
    tk.Button(ventana_editar, text="Editar Producto", command=editar_producto).pack(pady=5)
    tk.Button(ventana_editar, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)
    actualizar_productos_list()

# Funciones de usuarios
def crear_cuenta():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    if not nombre or not apellido or not dni:
        messagebox.showerror("Error", "Por favor complete todos los campos.")
        return
    usuarios = cargar_usuarios()
    if any(usuario["dni"] == dni for usuario in usuarios):
        messagebox.showerror("Error", "Ya existe un usuario con este DNI.")
        return
    usuarios.append({"nombre": nombre, "apellido": apellido, "dni": dni})
    guardar_usuarios(usuarios)
    messagebox.showinfo("Éxito", "Usuario creado con éxito.")

def borrar_usuario():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    usuarios = cargar_usuarios()
    usuario_a_borrar = next((usuario for usuario in usuarios if usuario["nombre"] == nombre and usuario["apellido"] == apellido and usuario["dni"] == dni), None)
    if not usuario_a_borrar:
        messagebox.showerror("Error", "No se encontró un usuario con esos datos.")
        return
    usuarios.remove(usuario_a_borrar)
    guardar_usuarios(usuarios)
    messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")

def iniciar_sesion():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    usuarios = cargar_usuarios()
    if any(usuario["nombre"] == nombre and usuario["apellido"] == apellido and usuario["dni"] == dni for usuario in usuarios):
        ventana_login.withdraw()
        ventana_administrativa.deiconify()
        mostrar_inventarios()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

# Interfaz gráfica
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("400x400")

tk.Label(ventana_login, text="Nombre:").pack(pady=5)
nombre_entry = tk.Entry(ventana_login)
nombre_entry.pack(pady=5)

tk.Label(ventana_login, text="Apellido:").pack(pady=5)
apellido_entry = tk.Entry(ventana_login)
apellido_entry.pack(pady=5)

tk.Label(ventana_login, text="DNI:").pack(pady=5)
dni_entry = tk.Entry(ventana_login)
dni_entry.pack(pady=5)

tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
tk.Button(ventana_login, text="Crear Cuenta", command=crear_cuenta).pack(pady=5)
tk.Button(ventana_login, text="Borrar Usuario", command=borrar_usuario).pack(pady=5)

ventana_administrativa = tk.Toplevel(ventana_login)
ventana_administrativa.title("Administración")
ventana_administrativa.geometry("500x400")
ventana_administrativa.withdraw()

sucursales_list = tk.Listbox(ventana_administrativa, width=50)
sucursales_list.pack(pady=10)

tk.Button(ventana_administrativa, text="Agregar Sucursal", command=agregar_sucursal).pack(pady=5)
tk.Button(ventana_administrativa, text="Editar Sucursal", command=editar_sucursal).pack(pady=5)
tk.Button(ventana_administrativa, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5)
tk.Button(ventana_administrativa, text="Vender", command=realizar_venta_desde_administrativa).pack(pady=5)

ventana_login.mainloop()