import customtkinter as ctk
from customtkinter import CTk, CTkToplevel, CTkOptionMenu
from tkinter import simpledialog, messagebox
import json

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")  # Opciones: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")

ARCHIVO_JSON = "sucursales.json"
USUARIOS_JSON = "usuarios.json"

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

def mostrar_inventarios():
    # Limpiar la lista
    sucursales_list.set("") 
    sucursales_list.set(values=empresa_suc)  # Setea los valores directamenteef mostrar_inventarios():
    sucursales_list.delete(0, "end")
    for sucursal in empresa_suc:
        sucursales_list.insert("end", sucursal[0])

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
    seleccion = sucursales_var.get()  # Obtener la sucursal seleccionada
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una sucursal.")
        return

    indice = int(seleccion)
    sucursal = empresa_suc[indice]

    ventana_editar = ctk.CTkToplevel(ventana_administrativa)
    ventana_editar.title(f"Editar {sucursal[0]}")
    ventana_editar.geometry("400x400")

    productos_var = tk.StringVar(value=None)  # Variable para los botones de radio

    def actualizar_productos():
        for widget in frame_productos.winfo_children():
            widget.destroy()
        
        for producto, (precio, stock) in sucursal[1].items():
            ctk.CTkRadioButton(
                frame_productos,
                text=f"{producto} - Precio: ${precio}, Stock: {stock}",
                variable=productos_var,
                value=producto
            ).pack(anchor="w", pady=2)

    frame_productos = ctk.CTkFrame(ventana_editar)
    frame_productos.pack(fill="both", expand=True, padx=10, pady=10)
    actualizar_productos()

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
        actualizar_productos()
        messagebox.showinfo("Éxito", f"Producto '{nuevo_producto}' agregado correctamente.")

    def editar_producto():
        producto_seleccionado = productos_var.get()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        try:
            nuevo_precio = float(simpledialog.askstring("Precio", f"Ingrese el nuevo precio de '{producto_seleccionado}':"))
            nuevo_stock = int(simpledialog.askstring("Stock", f"Ingrese el nuevo stock de '{producto_seleccionado}':"))
        except ValueError:
            messagebox.showerror("Error", "Valores inválidos.")
            return

        sucursal[1][producto_seleccionado] = (nuevo_precio, nuevo_stock)
        guardar_sucursales(empresa_suc)
        actualizar_productos()
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' actualizado correctamente.")

    def eliminar_producto():
        producto_seleccionado = productos_var.get()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        del sucursal[1][producto_seleccionado]
        guardar_sucursales(empresa_suc)
        actualizar_productos()
        messagebox.showinfo("Éxito", f"Producto '{producto_seleccionado}' eliminado correctamente.")

    ctk.CTkButton(ventana_editar, text="Agregar Producto", command=agregar_producto).pack(pady=5)
    ctk.CTkButton(ventana_editar, text="Editar Producto", command=editar_producto).pack(pady=5)
    ctk.CTkButton(ventana_editar, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)

def eliminar_sucursal():
    seleccion = sucursales_var()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione una sucursal.")
        return
    empresa_suc.pop(seleccion[0])
    guardar_sucursales(empresa_suc)
    mostrar_inventarios()
    messagebox.showinfo("Éxito", "Sucursal eliminada.")

def operar_venta(sucursal):
    boleta = []
    ventana_venta = ctk.CTkToplevel()
    ventana_venta.title(f"Ventas en {sucursal[0]}")
    ventana_venta.geometry("400x400")

    ctk.CTkLabel(ventana_venta, text=f"Sucursal: {sucursal[0]}", font=("Arial", 12)).pack(pady=10)

    productos_var = tk.StringVar(value=None)  # Variable para los botones de radio

    def actualizar_productos():
        for widget in frame_productos.winfo_children():
            widget.destroy()

        for producto, (precio, stock) in sucursal[1].items():
            ctk.CTkRadioButton(
                frame_productos,
                text=f"{producto} - Precio: ${precio}, Stock: {stock}",
                variable=productos_var,
                value=producto
            ).pack(anchor="w", pady=2)

    frame_productos = ctk.CTkFrame(ventana_venta)
    frame_productos.pack(fill="both", expand=True, padx=10, pady=10)
    actualizar_productos()

    def vender_producto():
        producto_seleccionado = productos_var.get()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de '{producto_seleccionado}' a vender:")
        if cantidad is None or cantidad <= 0:
            return

        precio, stock = sucursal[1][producto_seleccionado]
        if cantidad > stock:
            messagebox.showerror("Error", "Stock insuficiente.")
            return

        sucursal[1][producto_seleccionado] = (precio, stock - cantidad)
        guardar_sucursales(empresa_suc)
        actualizar_productos()

        # Agregar producto vendido a la boleta
        boleta.append((producto_seleccionado, cantidad, precio * cantidad))
        messagebox.showinfo("Venta realizada", f"Se vendieron {cantidad} unidades de '{producto_seleccionado}'.")

    def finalizar_venta():
        if not boleta:
            messagebox.showinfo("Boleta", "No hay productos vendidos.")
            return

        # Mostrar el resumen de la venta
        resumen = "\n".join([f"{prod} x{cant} - ${total:.2f}" for prod, cant, total in boleta])
        total_final = sum(total for _, _, total in boleta)
        messagebox.showinfo("Boleta", f"Resumen de la venta:\n\n{resumen}\n\nTotal: ${total_final:.2f}")

        # Reiniciar la boleta para la próxima venta
        boleta.clear()

    ctk.CTkButton(ventana_venta, text="Vender Producto", command=vender_producto).pack(pady=10)
    ctk.CTkButton(ventana_venta, text="Finalizar Venta", command=finalizar_venta).pack(pady=10)

def ventana_seleccion():
    ventana_login.withdraw()

    ventana_seleccion = ctk.CTkToplevel()
    ventana_seleccion.title("Seleccionar Acción")
    ventana_seleccion.geometry("300x200")

    ctk.CTkLabel(ventana_seleccion, text="¿Qué acción desea realizar?", font=("Arial", 14)).pack(pady=20)

    frame_botones = ctk.CTkFrame(ventana_seleccion)
    frame_botones.pack(pady=10)

    ctk.CTkButton(
        frame_botones,
        text="Administrar",
        command=lambda: [ventana_seleccion.withdraw(), ventana_administrativa.deiconify()],
        width=120
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        frame_botones,
        text="Vender",
        command=lambda: [ventana_seleccion.withdraw(), ventana_vender()],
        width=120
    ).pack(side="left", padx=10)

def ventana_vender():
    def seleccionar_sucursal_venta():
        sucursal_seleccionada = sucursal_var.get()
        if not sucursal_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una sucursal.")
            return

        for sucursal in empresa_suc:
            if sucursal[0] == sucursal_seleccionada:
                operar_venta(sucursal)
                break

    ventana_ventas = ctk.CTkToplevel()
    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("400x400")

    ctk.CTkLabel(ventana_ventas, text="Seleccione una Sucursal para Vender:", font=("Arial", 12)).pack(pady=10)

    frame_sucursales = ctk.CTkFrame(ventana_ventas)
    frame_sucursales.pack(pady=10, fill="x", padx=10)

    sucursal_var = tk.StringVar(value=None)

    for sucursal in empresa_suc:
        ctk.CTkRadioButton(
            frame_sucursales,
            text=sucursal[0],
            variable=sucursal_var,
            value=sucursal[0]
        ).pack(anchor="w", pady=2)

    ctk.CTkButton(
        ventana_ventas,
        text="Seleccionar",
        command=seleccionar_sucursal_venta
    ).pack(pady=10)

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
ventana_login = ctk.CTk()
ventana_login.title("Iniciar sesión")
ventana_login.geometry("400x500")

ctk.CTkLabel(ventana_login, text="Nombre:").pack(pady=5)
nombre_entry = ctk.CTkEntry(ventana_login)
nombre_entry.pack(pady=5)
ctk.CTkLabel(ventana_login, text="Apellido:").pack(pady=5)
apellido_entry = ctk.CTkEntry(ventana_login)
apellido_entry.pack(pady=5)
ctk.CTkLabel(ventana_login, text="DNI:").pack(pady=5)
dni_entry = ctk.CTkEntry(ventana_login)
dni_entry.pack(pady=5)

ctk.CTkButton(ventana_login, text="Iniciar sesión", command=iniciar_sesion).pack(pady=10)
ctk.CTkButton(ventana_login, text="Crear cuenta", command=crear_cuenta).pack(pady=10)

ventana_administrativa = CTkToplevel(ventana_login)
ventana_administrativa.title("Área Administrativa")
ventana_administrativa.geometry("400x400")
ventana_administrativa.withdraw()

sucursales_list = ctk.CTkRadioButton(ventana_administrativa, width=50)
sucursales_list.pack(pady=10)
ctk.CTkButton(ventana_administrativa, text="Agregar Sucursal", command=agregar_sucursal).pack(pady=5)
ctk.CTkButton(ventana_administrativa, text="Editar Sucursal", command=editar_sucursal).pack(pady=5)
ctk.CTkButton(ventana_administrativa, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5)

mostrar_inventarios()
ventana_login.mainloop()