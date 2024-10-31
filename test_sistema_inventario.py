import pytest
from sistema_inventario import busqueda, validar_longitud, long_dic, mostrar_inventarios, cargar_datos, guardar_datos

# Datos de prueba
empresa_suc_test = [
    ["Sucursal Test", {
        "Pan": (100, 50),
        "Leche": (200, 20)
    }],
    ["Sucursal Prueba", {
        "Café": (300, 15),
        "Yerba": (150, 10)
    }]
]

# Pruebas para la función `busqueda`
def test_busqueda_encontrado():
    assert busqueda(empresa_suc_test, "Sucursal Test") == 0

def test_busqueda_no_encontrado():
    assert busqueda(empresa_suc_test, "Sucursal Inexistente") == -1

# Pruebas para la función `validar_longitud`
def test_validar_longitud_valido():
    assert validar_longitud("Nombre Corto") == True

def test_validar_longitud_no_valido():
    assert validar_longitud("EsteNombreEsDemasiadoLargo") == False

# Pruebas para la función `long_dic`
def test_long_dic_valido():
    dic = {"Producto1": (10, 5), "Producto2": (15, 10)}
    assert long_dic(dic) == True

def test_long_dic_no_valido():
    dic = {f"Producto{i}": (10, 5) for i in range(8)}  # Diccionario con 8 productos
    assert long_dic(dic) == False

# Prueba para la función `mostrar_inventarios`
def test_mostrar_inventarios(capsys):
    mostrar_inventarios(empresa_suc_test)
    captured = capsys.readouterr()
    assert "Inventario de Sucursal Test:" in captured.out
    assert "Producto    Cantidad   Precio" in captured.out
    assert "Pan        50         $100.00" in captured.out

# Prueba para la función `guardar_datos` y `cargar_datos`
def test_guardar_y_cargar_datos(tmp_path):
    archivo = tmp_path / "test_inventario.json"
    guardar_datos(empresa_suc_test, archivo)
    datos_cargados = cargar_datos(archivo)
    assert datos_cargados == empresa_suc_test

