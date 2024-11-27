import tkinter as tk
from tkinter import messagebox, simpledialog
import json

# Archivos JSON
ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

# Función para cargar usuarios
def cargar_usuarios():
    try:
        with open(USUARIOS_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Función para guardar usuarios
def guardar_usuarios(usuarios):
    with open(USUARIOS_JSON, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

# Crear usuario
def crear_usuario():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()

    if not (nombre and apellido and dni):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if dni in usuarios:
        messagebox.showerror("Error", "El usuario con este DNI ya existe.")
        return

    usuarios[dni] = {"nombre": nombre, "apellido": apellido}
    guardar_usuarios(usuarios)
    messagebox.showinfo("Éxito", "Usuario creado correctamente.")
    limpiar_campos()

# Iniciar sesión
def iniciar_sesion():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()

    if not (nombre and apellido and dni):
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if dni in usuarios and usuarios[dni]["nombre"] == nombre and usuarios[dni]["apellido"] == apellido:
        messagebox.showinfo("Éxito", f"Bienvenido {nombre} {apellido}!")
        abrir_menu_principal()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")
        limpiar_campos()

# Abrir menú principal
def abrir_menu_principal():
    ventana_inicio.withdraw()  # Ocultar ventana de inicio
    ventana_principal.deiconify()  # Mostrar ventana principal

# Función para cerrar sesión
def cerrar_sesion():
    ventana_principal.withdraw()
    limpiar_campos()
    ventana_inicio.deiconify()

# Limpiar campos de entrada
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)

# Configurar la ventana principal
def configurar_ventana_principal():
    tk.Label(ventana_principal, text="Bienvenido al Sistema", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana_principal, text="Área Administrativa", command=mostrar_ventana_administrativa, width=20).pack(pady=10)
    tk.Button(ventana_principal, text="Ventas", command=mostrar_ventana_ventas, width=20).pack(pady=10)
    tk.Button(ventana_principal, text="Cerrar Sesión", command=cerrar_sesion, width=20).pack(pady=10)

# Función para mostrar la ventana administrativa
def mostrar_ventana_administrativa():
    ventana_principal.withdraw()
    root.deiconify()

# Función para mostrar la ventana de ventas
def mostrar_ventana_ventas():
    ventana_principal.withdraw()
    # Aquí puedes implementar la lógica para ventas
    messagebox.showinfo("Información", "Módulo de ventas aún no implementado.")

# Inicializar usuarios
usuarios = cargar_usuarios()

# Crear ventana de inicio
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de Sesión")
ventana_inicio.geometry("400x300")

# Etiquetas y campos de entrada
tk.Label(ventana_inicio, text="Nombre:", font=("Arial", 12)).pack(pady=5)
entry_nombre = tk.Entry(ventana_inicio, width=30)
entry_nombre.pack()

tk.Label(ventana_inicio, text="Apellido:", font=("Arial", 12)).pack(pady=5)
entry_apellido = tk.Entry(ventana_inicio, width=30)
entry_apellido.pack()

tk.Label(ventana_inicio, text="DNI:", font=("Arial", 12)).pack(pady=5)
entry_dni = tk.Entry(ventana_inicio, width=30)
entry_dni.pack()

# Botones
tk.Button(ventana_inicio, text="Aceptar Ingreso", command=iniciar_sesion, width=20).pack(pady=10)
tk.Button(ventana_inicio, text="Crear Cuenta", command=crear_usuario, width=20).pack(pady=5)

# Crear ventana principal oculta al inicio
ventana_principal = tk.Toplevel(ventana_inicio)
ventana_principal.title("Sistema Principal")
ventana_principal.geometry("400x300")
ventana_principal.withdraw()  # Ocultar al inicio
configurar_ventana_principal()

# Crear ventana administrativa oculta al inicio
root = tk.Toplevel(ventana_inicio)
root.title("Área Administrativa")
root.geometry("400x300")
root.withdraw()  # Ocultar al inicio

# Aquí puedes agregar lógica para la ventana administrativa

ventana_inicio.mainloop()
