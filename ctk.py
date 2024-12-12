import tkinter as tk
import customtkinter as ctk
from customtkinter import CTk, CTkToplevel, CTkRadioButton, CTkFrame, CTkButton, CTkLabel
from tkinter import simpledialog, messagebox
import json

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")  # Opciones: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")

ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

# Funciones para cargar y guardar JSON
def cargar_sucursales():
    try:
        with open(ARCHIVO_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_sucursales(empresa_suc):
    with open(ARCHIVO_JSON, "w") as archivo:
        json.dump(empresa_suc, archivo, indent=4)

def cargar_usuarios():
    try:
        with open(USUARIOS_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

# Variables globales
empresa_suc = cargar_sucursales()

# Mostrar inventarios usando RadioButtons en lugar de ListBox
def mostrar_inventarios():
    # Eliminar elementos existentes
    for widget in frame_sucursales.winfo_children():
        widget.destroy()

    for idx, sucursal in enumerate(empresa_suc):
        CTkRadioButton(
            frame_sucursales, 
            text=sucursal["Sucursal"],
            variable=sucursales_var,
            value=idx
        ).pack(anchor="w", pady=2)

def agregar_sucursal():
    nueva_sucursal = simpledialog.askstring("Agregar Sucursal", "Ingrese el nombre de la nueva sucursal:")
    if not nueva_sucursal or any(suc["Sucursal"] == nueva_sucursal for suc in empresa_suc):
        messagebox.showerror("Error", "Sucursal inválida o ya existente.")
        return

    empresa_suc.append({"Sucursal": nueva_sucursal, "Productos": {}})
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", f"Sucursal '{nueva_sucursal}' agregada.")

def eliminar_sucursal():
    seleccion = sucursales_var.get()
    if seleccion == "":
        messagebox.showerror("Error", "Seleccione una sucursal.")
        return

    empresa_suc.pop(int(seleccion))
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", "Sucursal eliminada correctamente.")

def editar_sucursal():
    seleccion = sucursales_var.get()
    if seleccion == "":
        messagebox.showerror("Error", "Seleccione una sucursal para editar.")
        return

    idx = int(seleccion)
    sucursal = empresa_suc[idx]

    ventana_editar = CTkToplevel(ventana_administrativa)
    ventana_editar.title(f"Editar {sucursal['Sucursal']}")
    ventana_editar.geometry("400x400")

    productos_frame = CTkFrame(ventana_editar)
    productos_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_productos():
        for widget in productos_frame.winfo_children():
            widget.destroy()
        for producto, datos in sucursal["Productos"].items():
            CTkLabel(productos_frame, text=f"{producto} - Precio: ${datos[0]}, Stock: {datos[1]}").pack(anchor="w")

    def agregar_producto():
        nombre_producto = simpledialog.askstring("Nuevo Producto", "Nombre del producto:")
        if not nombre_producto:
            return
        try:
            precio = float(simpledialog.askstring("Precio", "Precio del producto:"))
            stock = int(simpledialog.askstring("Stock", "Stock disponible:"))
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")
            return
        sucursal["Productos"][nombre_producto] = (precio, stock)
        guardar_sucursales(empresa_suc)
        actualizar_productos()

    CTkButton(ventana_editar, text="Agregar Producto", command=agregar_producto).pack(pady=5)
    actualizar_productos()

def ventana_seleccion():
    ventana_login.withdraw()
    ventana_administrativa.deiconify()

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

# Ventana de inicio de sesión
ventana_login = CTk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("400x300")

CTkLabel(ventana_login, text="Nombre:").pack(pady=5)
nombre_entry = CTkFrame(ventana_login)
nombre_entry = tk.Entry(ventana_login)
nombre_entry.pack()

CTkLabel(ventana_login, text="Apellido:").pack(pady=5)
apellido_entry = tk.Entry(ventana_login)
apellido_entry.pack()

CTkLabel(ventana_login, text="DNI:").pack(pady=5)
dni_entry = tk.Entry(ventana_login)
dni_entry.pack()

CTkButton(ventana_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=5)
CTkButton(ventana_login, text="Crear Cuenta", command=crear_cuenta).pack(pady=5)

# Ventana administrativa
ventana_administrativa = CTkToplevel(ventana_login)
ventana_administrativa.title("Administración de Sucursales")
ventana_administrativa.geometry("400x400")
ventana_administrativa.withdraw()

sucursales_var = tk.StringVar(value="")
frame_sucursales = CTkFrame(ventana_administrativa)
frame_sucursales.pack(fill="both", expand=True, padx=10, pady=10)

CTkButton(ventana_administrativa, text="Agregar Sucursal", command=agregar_sucursal).pack(pady=5)
CTkButton(ventana_administrativa, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5)
CTkButton(ventana_administrativa, text="Editar Sucursal", command=editar_sucursal).pack(pady=5)

mostrar_inventarios()
ventana_login.mainloop()
