import tkinter as tk
from tkinter import messagebox, simpledialog
import json

ARCHIVO_JSON = "sucursales.json"

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

# Inicializar las sucursales
empresa_suc = cargar_sucursales()

# Funciones para la interfaz
def mostrar_inventarios():
    sucursales_list.delete(0, tk.END)
    for sucursal in empresa_suc:
        sucursales_list.insert(tk.END, sucursal[0])

def ventana_administrativo():
    ventana_inicio.withdraw()  # Ocultar ventana inicial
    root.deiconify()  # Mostrar ventana administrativa


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

def editar_sucursal():
    seleccion = sucursales_list.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una sucursal.")
        return

    indice = seleccion[0]
    sucursal = empresa_suc[indice]

    # Crear ventana para editar productos
    ventana_editar = tk.Toplevel(root)
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

    agregar_producto_btn = tk.Button(ventana_editar, text="Agregar Producto", command=agregar_producto)
    agregar_producto_btn.pack(pady=5)

    editar_producto_btn = tk.Button(ventana_editar, text="Editar Producto", command=editar_producto)
    editar_producto_btn.pack(pady=5)

    eliminar_producto_btn = tk.Button(ventana_editar, text="Eliminar Producto", command=eliminar_producto)
    eliminar_producto_btn.pack(pady=5)

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


def ventana_vender():
    ventana_inicio.withdraw()  # Ocultar ventana inicial

    def seleccionar_sucursal_venta():
        seleccion = sucursales_list_venta.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar una sucursal.")
            return

        indice = seleccion[0]
        sucursal = empresa_suc[indice]
        operar_venta(sucursal)

    # Crear ventana de ventas
    ventana_ventas = tk.Toplevel(ventana_inicio)
    ventana_ventas.title("Ventas")
    ventana_ventas.geometry("400x400")

    tk.Label(ventana_ventas, text="Seleccione una Sucursal para Vender:", font=("Arial", 12)).pack(pady=10)
    sucursales_list_venta = tk.Listbox(ventana_ventas, width=50)
    sucursales_list_venta.pack(pady=10)

    for sucursal in empresa_suc:
        sucursales_list_venta.insert(tk.END, sucursal[0])

    tk.Button(ventana_ventas, text="Seleccionar", command=seleccionar_sucursal_venta).pack(pady=10)

def operar_venta(sucursal):
    ventana_venta = tk.Toplevel(root)
    ventana_venta.title(f"Venta - {sucursal[0]}")
    ventana_venta.geometry("400x400")

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
        try:
            cantidad = int(simpledialog.askstring("Venta", f"Ingrese la cantidad a vender de '{producto_seleccionado}':"))
            if cantidad <= 0 or cantidad > sucursal[1][producto_seleccionado][1]:
                messagebox.showerror("Error", "Cantidad inválida o insuficiente en stock.")
                return
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        # Actualizar stock
        precio, stock_actual = sucursal[1][producto_seleccionado]
        nuevo_stock = stock_actual - cantidad
        sucursal[1][producto_seleccionado] = (precio, nuevo_stock)
        guardar_sucursales(empresa_suc)

        # Actualizar lista
        productos_list.delete(seleccion)
        productos_list.insert(seleccion, f"{producto_seleccionado} - Precio: ${precio}, Stock: {nuevo_stock}")
        messagebox.showinfo("Éxito", f"Venta de {cantidad} unidades de '{producto_seleccionado}' realizada correctamente.")

    tk.Button(ventana_venta, text="Vender Producto", command=vender_producto).pack(pady=5)

# Crear la ventana inicial
ventana_inicio = tk.Tk()
ventana_inicio.title("Gestión de Sucursales")
ventana_inicio.geometry("400x200")

tk.Label(ventana_inicio, text="Seleccione una opción:", font=("Arial", 14)).pack(pady=20)
tk.Button(ventana_inicio, text="Administrativo", command=ventana_administrativo, width=20).pack(pady=10)
tk.Button(ventana_inicio, text="Vender", command=ventana_vender, width=20).pack(pady=10)

# Crear la ventana principal administrativa oculta al inicio
root = tk.Toplevel(ventana_inicio)
root.title("Área Administrativa")
root.geometry("500x400")
root.withdraw()  # Ocultar al inicio

tk.Label(root, text="Sucursales:", font=("Arial", 14)).pack(pady=10)
sucursales_list = tk.Listbox(root, width=50)
sucursales_list.pack(pady=10)

mostrar_inventarios()

tk.Button(root, text="Agregar Sucursal", command=agregar_sucursal).pack(pady=5)
tk.Button(root, text="Editar Sucursal", command=editar_sucursal).pack(pady=5)
tk.Button(root, text="Eliminar Sucursal", command=eliminar_sucursal).pack(pady=5)

ventana_inicio.mainloop()
