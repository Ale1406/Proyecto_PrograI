import tkinter as tk
from tkinter import messagebox, simpledialog
import json

ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

# Funciones para manejar datos
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
    datos = [{"Sucursal": suc[0], "Productos": {prod: list(vals) for prod, vals in suc[1].items()}} for suc in empresa_suc]
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

# Funciones administrativas
def mostrar_inventarios():
    sucursales_list.delete(0, tk.END)
    for sucursal in empresa_suc:
        sucursales_list.insert(tk.END, sucursal[0])

def agregar_sucursal():
    nueva_sucursal = simpledialog.askstring("Agregar Sucursal", "Ingrese el nombre de la nueva sucursal:")
    if not nueva_sucursal or any(suc[0] == nueva_sucursal for suc in empresa_suc):
        messagebox.showerror("Error", "Sucursal inválida o ya existente.")
        return
    empresa_suc.append([nueva_sucursal, {}])
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", f"Sucursal '{nueva_sucursal}' agregada.")
def editar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una sucursal.")
        return

    indice = seleccion[0]
    sucursal = empresa_suc[indice]

    ventana_editar = tk.Toplevel(ventana_administrativa)
    ventana_editar.title(f"Editar {sucursal[0]}")
    ventana_editar.geometry("400x400")

    productos_list = tk.Listbox(ventana_editar, width=50)
    productos_list.pack(pady=10)
    for producto, (precio, stock) in sucursal[1].items():
        productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")

    def agregar_producto():
        nuevo_producto = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
        if not nuevo_producto:
            return

        if nuevo_producto in sucursal[1]:
            messagebox.showerror("Error", "El producto ya existe en la sucursal.")
            return

        try:
            precio = float(simpledialog.askstring("Precio", f"Ingrese el precio de '{nuevo_producto}':"))
            stock = int(simpledialog.askstring("Stock", f"Ingrese el stock de '{nuevo_producto}':"))
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos.")
            return

        sucursal[1][nuevo_producto] = (precio, stock)
        guardar_sucursales(empresa_suc)
        productos_list.insert(tk.END, f"{nuevo_producto} - Precio: ${precio}, Stock: {stock}")
        messagebox.showinfo("Éxito", f"Producto '{nuevo_producto}' agregado correctamente.")
        pass

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
        productos_list.delete(seleccion_producto)
        productos_list.insert(seleccion_producto, f"{producto_seleccionado} - Precio: ${nuevo_precio}, Stock: {nuevo_stock}")
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' actualizado correctamente.")
        pass

    def eliminar_producto():
        seleccion_producto = productos_list.curselection()
        if not seleccion_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        producto_seleccionado = productos_list.get(seleccion_producto).split(" - ")[0]
        del sucursal[1][producto_seleccionado]
        guardar_sucursales(empresa_suc)
        productos_list.delete(seleccion_producto)
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' eliminado correctamente.")
        pass

    tk.Button(ventana_editar, text="Agregar Producto", command=agregar_producto).pack(pady=5)
    tk.Button(ventana_editar, text="Editar Producto", command=editar_producto).pack(pady=5)
    tk.Button(ventana_editar, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)

def eliminar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una sucursal.")
        return
    empresa_suc.pop(seleccion[0])
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", "Sucursal eliminada.")
# Funciones de ventas
def operar_venta(sucursal):
    ventana_venta = tk.Toplevel()
    ventana_venta.title(f"Ventas en {sucursal[0]}")
    ventana_venta.geometry("400x400")

    tk.Label(ventana_venta, text=f"Sucursal: {sucursal[0]}", font=("Arial", 12)).pack(pady=10)
    productos_list = tk.Listbox(ventana_venta, width=50)
    productos_list.pack(pady=10)

    for producto, (precio, stock) in sucursal[1].items():
        productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")

    def vender_producto():
        seleccion = productos_list.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        producto_seleccionado = productos_list.get(seleccion).split(" - ")[0]
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de '{producto_seleccionado}' a vender:")
        if cantidad is None or cantidad <= 0:
            return

        precio, stock = sucursal[1][producto_seleccionado]
        if cantidad > stock:
            messagebox.showerror("Error", "Stock insuficiente.")
            return

        sucursal[1][producto_seleccionado] = (precio, stock - cantidad)
        guardar_sucursales(empresa_suc)
        productos_list.delete(seleccion)
        productos_list.insert(seleccion, f"{producto_seleccionado} - Precio: ${precio}, Stock: {stock - cantidad}")
        messagebox.showinfo("Venta realizada", f"Se vendieron {cantidad} unidades de '{producto_seleccionado}'.")

    tk.Button(ventana_venta, text="Vender Producto", command=vender_producto).pack(pady=10)

# Ventanas principales
def ventana_seleccion():
    ventana_login.withdraw()

    ventana_seleccion = tk.Toplevel()
    ventana_seleccion.title("Seleccionar Acción")
    ventana_seleccion.geometry("300x200")

    tk.Label(ventana_seleccion, text="¿Qué acción desea realizar?", font=("Arial", 14)).pack(pady=20)

    tk.Button(ventana_seleccion, text="Administrar", command=lambda: [ventana_seleccion.withdraw(), ventana_administrativa.deiconify()]).pack(pady=10)
    tk.Button(ventana_seleccion, text="Vender", command=lambda: [ventana_seleccion.withdraw(), ventana_vender()]).pack(pady=10)

def ventana_vender():
    def seleccionar_sucursal_venta():
        seleccion = sucursales_list_venta.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar una sucursal.")
            return

        indice = seleccion[0]
        sucursal = empresa_suc[indice]
        operar_venta(sucursal)

    ventana_ventas = tk.Toplevel()
    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("400x400")

    tk.Label(ventana_ventas, text="Seleccione una Sucursal para Vender:", font=("Arial", 12)).pack(pady=10)
    sucursales_list_venta = tk.Listbox(ventana_ventas, width=50)
    sucursales_list_venta.pack(pady=10)

    for sucursal in empresa_suc:
        sucursales_list_venta.insert(tk.END, sucursal[0])

    tk.Button(ventana_ventas, text="Seleccionar", command=seleccionar_sucursal_venta).pack(pady=10)

# Inicio de sesión
def iniciar_sesion():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    usuarios = cargar_usuarios()
    if any(user for user in usuarios if user["nombre"] == nombre and user["apellido"] == apellido and user["dni"] == dni):
        ventana_seleccion()
    else:
        messagebox.showerror("Error", "Datos incorrectos.")

def crear_cuenta():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()
    if not nombre or not apellido or not dni:
        messagebox.showerror("Error", "Complete todos los campos.")
        return
    usuarios = cargar_usuarios()
    if any(user["dni"] == dni for user in usuarios):
        messagebox.showerror("Error", "DNI ya registrado.")
        return
    usuarios.append({"nombre": nombre, "apellido": apellido, "dni": dni})
    guardar_usuarios(usuarios)
    messagebox.showinfo("Éxito", "Cuenta creada.")

# Configuración de la ventana principal
ventana_login = tk.Tk()
ventana_login.title("Iniciar sesión")
ventana_login.geometry("300x250")

tk.Label(ventana_login, text="Nombre:").pack(pady=5)
nombre_entry = tk.Entry(ventana_login)
nombre_entry.pack(pady=5)
tk.Label(ventana_login, text="Apellido:").pack(pady=5)
apellido_entry = tk.Entry(ventana_login)
apellido_entry.pack(pady=5)
tk.Label(ventana_login, text="DNI:").pack(pady=5)
dni_entry = tk.Entry(ventana_login)
dni_entry.pack(pady=5)

tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion).pack(pady=10)
tk.Button(ventana_login, text="Crear cuenta", command=crear_cuenta).pack(pady=10)

ventana_administrativa = tk.Toplevel(ventana_login)
ventana_administrativa.title("Área Administrativa")
ventana_administrativa.geometry("400x400")
ventana_administrativa.withdraw()

sucursales_list = tk.Listbox(ventana_administrativa, width=50)
sucursales_list.pack(pady=10)
tk.Button(ventana_administrativa, text="Agregar Sucursal", command=agregar_sucursal).pack(pady=5)
tk.Button(ventana_administrativa, text="Editar Sucursal", command=editar_sucursal).pack(pady=5)
tk.Button(ventana_administrativa, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5)

mostrar_inventarios()
ventana_login.mainloop()
