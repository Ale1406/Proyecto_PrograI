import tkinter as tk
from tkinter import messagebox, simpledialog
import json

ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

# Cargar datos desde JSON al inicio del programa
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

# Cargar usuarios desde JSON
def cargar_usuarios():
    try:
        with open(USUARIOS_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guardar usuarios en JSON
def guardar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

# Inicializar las sucursales
empresa_suc = cargar_sucursales()

# Función para mostrar inventarios
def mostrar_inventarios():
    sucursales_list.delete(0, tk.END)
    for sucursal in empresa_suc:
        sucursales_list.insert(tk.END, sucursal[0])

# Función para agregar nueva sucursal
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

# Función para editar sucursal
def editar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una sucursal.")
        return

    indice = seleccion[0]
    sucursal = empresa_suc[indice]

    # Crear ventana para editar productos
    ventana_editar = tk.Toplevel(ventana_login)  # Cambiar root por ventana_login
    ventana_editar.title(f"Editar {sucursal[0]}")
    ventana_editar.geometry("400x400")

    productos_list = tk.Listbox(ventana_editar, width=50)
    productos_list.pack(pady=10)

    # Cargar los productos de la sucursal en el Listbox
    for producto, (precio, stock) in sucursal[1].items():
        productos_list.insert(tk.END, f"{producto} - Precio: ${precio}, Stock: {stock}")

    def actualizar_productos_list():
        productos_list.delete(0, tk.END)
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

    # Botones para agregar, editar, y eliminar productos
    agregar_producto_btn = tk.Button(ventana_editar, text="Agregar Producto", command=agregar_producto)
    agregar_producto_btn.pack(pady=5)

    editar_producto_btn = tk.Button(ventana_editar, text="Editar Producto", command=editar_producto)
    editar_producto_btn.pack(pady=5)

    eliminar_producto_btn = tk.Button(ventana_editar, text="Eliminar Producto", command=eliminar_producto)
    eliminar_producto_btn.pack(pady=5)

# Función para eliminar sucursal
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

# Función de inicio de sesión
def iniciar_sesion():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()

    usuarios = cargar_usuarios()

    for usuario in usuarios:
        if usuario["nombre"] == nombre and usuario["apellido"] == apellido and usuario["dni"] == dni:
            global usuario_logueado
            usuario_logueado = usuario
            ventana_login.withdraw()  # Ocultar la ventana de inicio de sesión
            ventana_administrativa.deiconify()  # Mostrar ventana administrativa
            return

    messagebox.showerror("Error", "Datos incorrectos. Intente nuevamente.")

# Función para crear cuenta
def crear_cuenta():
    nombre = nombre_entry.get()
    apellido = apellido_entry.get()
    dni = dni_entry.get()

    if not nombre or not apellido or not dni:
        messagebox.showerror("Error", "Por favor ingrese todos los campos.")
        return

    usuarios = cargar_usuarios()
    for usuario in usuarios:
        if usuario["dni"] == dni:
            messagebox.showerror("Error", "Ya existe una cuenta con ese DNI.")
            return

    nuevo_usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni
    }
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    messagebox.showinfo("Éxito", "Cuenta creada con éxito.")
    ventana_login.withdraw()  # Ocultar la ventana de login
    ventana_administrativa.deiconify()  # Mostrar ventana administrativa

# Crear la ventana de login
ventana_login = tk.Tk()
ventana_login.title("Iniciar sesión")
ventana_login.geometry("300x250")

nombre_label = tk.Label(ventana_login, text="Nombre:")
nombre_label.pack(pady=5)
nombre_entry = tk.Entry(ventana_login)
nombre_entry.pack(pady=5)

apellido_label = tk.Label(ventana_login, text="Apellido:")
apellido_label.pack(pady=5)
apellido_entry = tk.Entry(ventana_login)
apellido_entry.pack(pady=5)

dni_label = tk.Label(ventana_login, text="DNI:")
dni_label.pack(pady=5)
dni_entry = tk.Entry(ventana_login)
dni_entry.pack(pady=5)

btn_login = tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion)
btn_login.pack(pady=10)

btn_crear_cuenta = tk.Button(ventana_login, text="Crear cuenta", command=crear_cuenta)
btn_crear_cuenta.pack(pady=10)

# Crear la ventana administrativa
ventana_administrativa = tk.Toplevel(ventana_login)
ventana_administrativa.title("Área Administrativa")
ventana_administrativa.geometry("400x400")
ventana_administrativa.withdraw()  # Ocultar la ventana administrativa inicialmente

sucursales_list = tk.Listbox(ventana_administrativa, width=50)
sucursales_list.pack(pady=10)

btn_agregar_sucursal = tk.Button(ventana_administrativa, text="Agregar Sucursal", command=agregar_sucursal)
btn_agregar_sucursal.pack(pady=5)

btn_editar_sucursal = tk.Button(ventana_administrativa, text="Editar Sucursal", command=editar_sucursal)
btn_editar_sucursal.pack(pady=5)

btn_eliminar_sucursal = tk.Button(ventana_administrativa, text="Eliminar Sucursal", command=eliminar_sucursal)
btn_eliminar_sucursal.pack(pady=5)

mostrar_inventarios()

ventana_login.mainloop()
