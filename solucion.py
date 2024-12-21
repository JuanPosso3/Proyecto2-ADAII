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

archivoEntrada = "entrada.txt" 
datos = leerArchivo(archivoEntrada)
#print(datos)


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

ruta_salida = "salida.txt" 
ganancia_sin_nuevas = 120
ganancia_con_nuevas = 240
ubicaciones_establecidas = [(6, 8), (8, 4), (10, 10)]
nuevas_ubicaciones = [(2, 3), (5, 5), (12, 1), (13, 15)]

escribirArchivo(ruta_salida, ganancia_sin_nuevas, ganancia_con_nuevas, ubicaciones_establecidas, nuevas_ubicaciones)


