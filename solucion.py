"""
Juan Miguel Posso -2259610
Jhon Alejandro Martinez -2259565
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from minizinc import Instance, Model, Solver

# Funciones de procesamiento existentes
def leerArchivo(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()

    # Elimina espacios en blanco y caracteres de nueva línea
    lineas = [linea.strip() for linea in lineas]
    # Parsear el número de ubicaciones de programas existentes
    num_ubicaciones_existentes = int(lineas[0])
    # Parsear las coordenadas de las ubicaciones existentes
    ubicaciones_existentes = []
    for i in range(1, num_ubicaciones_existentes + 1):
        x, y = map(int, lineas[i].split())
        ubicaciones_existentes.append((x, y))
    # Parsear el tamaño de las matrices
    tamano_matriz = int(lineas[num_ubicaciones_existentes + 1])
    # Parsear la matriz de segmentos poblacionales
    matriz_poblacion = []
    idx_inicio = num_ubicaciones_existentes + 2
    for i in range(idx_inicio, idx_inicio + tamano_matriz):
        fila = list(map(int, lineas[i].split()))
        matriz_poblacion.append(fila)
    # Parsear la matriz del entorno de negocios
    matriz_negocios = []
    idx_inicio += tamano_matriz
    for i in range(idx_inicio, idx_inicio + tamano_matriz):
        fila = list(map(int, lineas[i].split()))
        matriz_negocios.append(fila)
    # Parsear el número de nuevos programas a ubicar
    num_nuevos_programas = int(lineas[idx_inicio + tamano_matriz])

    return {
        "num_ubicaciones_existentes": num_ubicaciones_existentes,
        "ubicaciones_existentes": ubicaciones_existentes,
        "tamano_matriz": tamano_matriz,
        "matriz_poblacion": matriz_poblacion,
        "matriz_negocios": matriz_negocios,
        "num_nuevos_programas": num_nuevos_programas
    }

def escribir_data_dzn(datos, archivo_salida):
    with open(archivo_salida, 'w') as file:
        # Escribir el número de ubicaciones existentes
        file.write(f"num_existing_locations = {datos['num_ubicaciones_existentes']};\n")

        # Escribir las ubicaciones existentes
        existing_locations_flat = ", ".join(
            f"{x}, {y}" for x, y in datos['ubicaciones_existentes']
        )
        file.write(
            f"existing_locations = array2d(0..{datos['num_ubicaciones_existentes'] - 1}, 0..1, [{existing_locations_flat}]);\n"
        )

        # Escribir el tamaño de la matriz
        file.write(f"matrix_size = {datos['tamano_matriz']};\n")

        # Escribir la matriz de población
        tamano = datos['tamano_matriz']
        population_flat = ", ".join(map(str, sum(datos['matriz_poblacion'], [])))
        file.write(
            f"population_matrix = array2d(0..{tamano - 1}, 0..{tamano - 1}, [{population_flat}]);\n"
        )

        # Escribir la matriz de entorno empresarial
        business_flat = ", ".join(map(str, sum(datos['matriz_negocios'], [])))
        file.write(
            f"business_matrix = array2d(0..{tamano - 1}, 0..{tamano - 1}, [{business_flat}]);\n"
        )

        # Escribir el número de nuevos programas
        file.write(f"num_new_programs = {datos['num_nuevos_programas']};\n")

def procesar_resultado(result):
    output = str(result)
    lines = output.strip().split("\n")
    # Extraer la ganancia inicial
    ganancia_inicial = int(lines[0].split(":")[1].strip())
    # Extraer las nuevas ubicaciones
    ubicaciones_nuevas = [
        tuple(map(int, line.split())) for line in lines[2:-1]
    ]
    # Extraer la ganancia total
    ganancia_total = int(lines[-1].split(":")[1].strip())
    return ganancia_inicial, ubicaciones_nuevas, ganancia_total

def escribirArchivo(file_path, ganancia_sin_nuevas, ganancia_con_nuevas, ubicaciones_establecidas, nuevas_ubicaciones):
    with open(file_path, 'w') as file:
        # Escribir las ganancias
        file.write(f"{ganancia_sin_nuevas}\n")
        file.write(f"{ganancia_con_nuevas}\n")

        # Escribir las ubicaciones establecidas, ordenadas por el primer valor
        for ubicacion in sorted(ubicaciones_establecidas):
            file.write(f"{ubicacion[0]} {ubicacion[1]}\n")

        # Escribir las nuevas ubicaciones, ordenadas por el primer valor
        for ubicacion in sorted(nuevas_ubicaciones):
            file.write(f"{ubicacion[0]} {ubicacion[1]}\n")


# Variables globales
ruta_archivo_entrada = None
valor_selector = "gecode"

# Funciones de la interfaz
def cargar_archivo():
    global ruta_archivo_entrada
    ruta_archivo_entrada = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo_entrada:
        messagebox.showinfo("Archivo cargado", f"Archivo seleccionado: {ruta_archivo_entrada}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")

def cambiar_selector(valor):
    global valor_selector
    valor_selector = valor
    messagebox.showinfo("Selector cambiado", f"Solver seleccionado: {valor}")

def ejecutar_proceso():
    if not ruta_archivo_entrada:
        messagebox.showwarning("Advertencia", "Primero debes cargar un archivo de entrada.")
        return

    try:
        # Leer los datos
        datos = leerArchivo(ruta_archivo_entrada)

        # Crear el archivo .dzn
        archivo_dzn = "data.dzn"
        escribir_data_dzn(datos, archivo_dzn)

        # Configurar el modelo de MiniZinc
        modelo = Model("modeloMinizinc.mzn")
        solver = Solver.lookup(valor_selector)
        instancia = Instance(solver, modelo)

        # Resolver el modelo
        resultado = instancia.solve()

        # Procesar el resultado
        ganancia_inicial, nuevas_ubicaciones, ganancia_total = procesar_resultado(resultado)

        # Generar el archivo de salida
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo_salida:
            escribirArchivo(archivo_salida, ganancia_inicial, ganancia_total, datos["ubicaciones_existentes"], nuevas_ubicaciones)
            messagebox.showinfo("Éxito", f"Resultados guardados en: {archivo_salida}")
        else:
            messagebox.showwarning("Advertencia", "No se guardó ningún archivo de salida.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Interfaz gráfica
def main():
    root = tk.Tk()
    root.title("Interfaz MiniZinc")

    # Botón para cargar archivo
    btn_cargar = tk.Button(root, text="Cargar archivo de entrada", command=cargar_archivo)
    btn_cargar.pack(pady=10)

    # Menú desplegable para seleccionar el solver
    tk.Label(root, text="Selecciona un solver:").pack()
    opciones = ["gecode", "chuffed", "cp-sat"]
    selector_solver = tk.StringVar(value="gecode")
    menu_selector = tk.OptionMenu(root, selector_solver, *opciones, command=cambiar_selector)
    menu_selector.pack(pady=10)

    # Botón para ejecutar el proceso
    btn_ejecutar = tk.Button(root, text="Ejecutar modelo", command=ejecutar_proceso)
    btn_ejecutar.pack(pady=10)

    # Ejecutar la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()
