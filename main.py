import json
import re
#----------------LEER JSON---------------------------------------------------------
def leer_archivo(nombre_archivo: str, nombre_variable_json: str):
    #Recibe el nombre del archivo y el nombre del dato como figura en json y devulve una lista
    #Crear una lista vacía para almacenar los datos obtenidos
    # Abre el archivo en modo de lectura utilizando el nombre del archivo indicado
    # Cargar el contenido del archivo JSON en un diccionario utilizando la función json.load()
    #json.load() se utiliza para cargar el contenido de un archivo JSON y convertirlo en un objeto de Python
    #Obtiene la lista de datos del diccionario utilizando el nombre de la variable pasada por parametro

    lista_obtenida = []

    with open(nombre_archivo, "r") as archivo:
        dict = json.load(archivo)
        lista_obtenida = dict[nombre_variable_json]

    return lista_obtenida
#---------------------------GENERALES---------------------------------------------------------
def imprimir_dato(dato:str):
    # recibe un str y lo muestro por consola
    print(dato)

def imprimir_lista(lista:list):
   #recibe una lista y la muestra por consola
   for jugador in lista:
        print(jugador)

def es_entero(numero:int):
   #recibe un numero y verifica que sea un enter
   #retorna True o False
   return bool(re.match(r'^[0-9]*$', str(numero)))

def es_decimal(numero:float):
    #recibe un numero y verifica que sea un float
    #retorna True o False
    patron_decimal = r'^[-+]?[0-9]+\.[0-9]+$'
    if re.match(patron_decimal, str(numero)):
        return True
    else:
        return False

def validador_de_enteros_en_rango(numero:int, min:int, max:int):
    #recibe 3 numeros el primero es el numero a verificar y los otros 2
    #son los rangos a validar
    #retorna True o False
    if es_entero(numero) == True:
        numero=int(numero)
        if numero >= min and numero <= max:
            return numero
        else:
            return None


def solicitar_numero(mensaje:str):
    # Recibe el mensaje a mostrar
    # Retorna el número ingresado casteado a int o float y en caso que
    # no sea un numero el ingresado vuelve a solicitarlo nuevamente
    while True:
        valor = input(mensaje)
        if es_entero(valor):
            return int(valor)
        elif es_decimal(valor):
            return float(valor)
        else:
            print("El valor ingresado no es un número válido. Por favor, intente nuevamente.")

#-------------------------- 1 - Mostrar jugadores -------------------------------------------------------      

def mostrar_todos(lista:list):
    #recibe un lista
    #retorna los nombres y la posicion de todos en la lista

    todos_los_jugadores=[]
    for jugador in lista:
        todos_los_jugadores.append("{0} - {1}".format(jugador['nombre'], jugador['posicion']))
    return todos_los_jugadores

#-------------------------- 2 - LISTAR Y MOSTRAR ESTADISTICAS-----------------------------
def listar_datos(lista:list):
   #recibe una lista
   #con un contador les asigna un numero de manera creciente a cada uno de la lista
   #retorna la lista con el numero y el nombre
   jugadores_enlistados=[]
   contador=0
   for jugador in lista:
      contador+=1
      jugadores_enlistados.append("{0} - {1}".format(contador, jugador['nombre']))

   return jugadores_enlistados  


def seleccionar_jugador(lista_jugadores):
    #recibe una lista
    #muestra la lista con el numero y el nombre asignado por orden
    #solicita el numero del jugador y valida que este en el rango correspondiente
    #encuentra la posicion del jugador y le asigna los valores de las estadisticas
    #itera para generar las lista con las claves y los valores de las estadisticas
    #retorna la lista con clave valor

    lista_estadisticas = []

    print("Indique el número del jugador que desea ver las estadísticas")
    imprimir_lista(listar_datos(lista_jugadores))

    while True:
        numero_jugador = input("Número del jugador seleccionado: ")
        numero_validado = validador_de_enteros_en_rango(numero_jugador, 1, len(lista_jugadores))

        if numero_validado is not None:
            jugador_seleccionado = lista_jugadores[numero_validado - 1]
            estadisticas = jugador_seleccionado["estadisticas"]

            print("Estadísticas del jugador: ")
            estadisticas_dict = {}  
            for clave, valor in estadisticas.items():
                clave_formateada = clave.replace("_", " ").capitalize()
                estadisticas_dict[clave_formateada] = valor  # Agregar estadística al diccionario

            lista_estadisticas.append(estadisticas_dict)  # Agregar diccionario a la lista
            break
        else:
            return print("El número ingresado no es válido. Por favor, intente nuevamente.")

    return lista_estadisticas

#--------------------------- 3 - GUARDAR ARCHIVOS ----------------------------------------------------------


def guardar_archivo(nombre_archivo:str, contenido:str):
    # Le paso un string y me guarda un archivo
    with open(nombre_archivo, "w") as archivo:
        archivo.write(contenido)

def parser_csv(estadisticas_jugador:list):
    #recibe un lista
    #verifica que no este vacia la lista
    #obtiene el nombre de las columnas
    #itera sobre cada elemento
    # retorna la clave y el valor para generar el csv 

    if len(estadisticas_jugador) == 0:
        return ""
    claves = estadisticas_jugador[0].keys()
    cabecera = ",".join(claves)
    cabecera += "\n"
    datos = ""
    for estadistica in estadisticas_jugador:
        datos += ",".join(str(valor) for valor in estadistica.values())
        datos += "\n"
    return cabecera + datos

#------------------ 4 - Buscar por nombre, mostrar logros----------------------------

def buscar_por_nombre(lista: list): 
    #recibe una lista
    #itera hasta encontrar el el string brindado
    #retorna la lista de los encontrados
    nombre = input("nombre del jugador a buscar")

    lista_encontrados=[]
    for jugador in lista:
        if re.search(nombre, jugador.get("nombre", ""), re.IGNORECASE):
            lista_encontrados.append({"nombre": jugador['nombre']})
    return lista_encontrados

def mostrar_logros(lista: list, nombres_buscados: list):
    #recibe una lista con todos los datos y otra con los datos de los jugadores que queremos mostrar
    #itera 2 veces para encontrar los mismos nombres y obtener los logros
    #imprime los nombres y los logros
    for jugador in lista:
        for nombre_buscado in nombres_buscados:
            if jugador["nombre"] == nombre_buscado["nombre"]:
                print("{0} - {1}".format(jugador["nombre"], jugador["logros"]))

#------------------ 5 - Promedio de puntos, ordenamiento------------------------------

def promedio_totales(lista:list, dato_buscado ):
    #recibe una lista y suma los promedios individuales para generar uno total 
    #y lo divide por la cantidad de jugadores para obtener el promedio del equipo
    promedio = 0
    for jugador in lista:
        promedio += jugador["estadisticas"][dato_buscado]
    return("El promedio total por partido es: {}".format (promedio/len(lista))) 
 
   
def ordenar_por_key(lista:list, dato_ordenamiento:str, mayor_menor:bool):
    # Ordena una lista de objetos por una clave dada, en orden ascendente o descendente
    rango_a = len(lista)
    # Obtiene la longitud de la lista y la asigna a la variable rango_a
    flag_swap = True
    # Establece una bandera para realizar intercambios en el bucle while
    while (flag_swap):
        # Inicia un bucle while que se ejecuta mientras flag_swap sea verdadero
        flag_swap = False
        # Establece flag_swap en falso antes de cada iteración del bucle
        rango_a = rango_a - 1
        # Reduce el rango del bucle en 1 en cada iteración
        for indice_A in range(rango_a):
            # Inicia un bucle for para recorrer la lista desde el índice 0 hasta rango_a - 1
            if mayor_menor == True and lista[indice_A][dato_ordenamiento] > lista[indice_A + 1][dato_ordenamiento] or \
            mayor_menor == False and lista[indice_A][dato_ordenamiento] < lista[indice_A + 1][dato_ordenamiento]:
                # Comprueba si se cumple una de las dos condiciones para intercambiar los elementos de la lista:
                # Si mayor_menor es verdadero y el dato en el índice_A es mayor que el dato en el índice_A + 1
                # O si mayor_menor es falso y el dato en el índice_A es menor que el dato en el índice_A + 1
                lista[indice_A], lista[indice_A + 1] = lista[indice_A + 1], lista[indice_A]
                # Intercambia los elementos de la lista en los índices índice_A y índice_A + 1
                flag_swap = True
                # Establece flag_swap en verdadero para indicar que se realizó un intercambio
    return lista

#------------------ 6 - buscar logros-----------------------------

def es_miembro_del_salon_de_la_fama2(lista:list, nombresobtenidos:list):
    #recibe una lista con todos los datos y otra con los datos de los jugadores que queremos mostrar
    #itera 2 veces para encontrar los mismos nombres y asi poder ver quienes tiene el valor que se compara en el if
    #imprime directamente los resultados para ver si pertenecieron

    for jugador in lista:
        for unnombre in nombresobtenidos:
            if jugador["nombre"] == unnombre["nombre"]:
            
                if "Miembro del Salon de la Fama del Baloncesto" in jugador["logros"]:
                    print("{0} pertenece al Salón de la Fama del Baloncesto.".format(unnombre["nombre"]))
                else:
                    print("{0} no pertenece al Salón de la Fama del Baloncesto.".format(unnombre["nombre"]))
    

#----------------- 7-8-9-13-14-19 calcular mayor menor -----------------------------------
def calcular_min(lista:list, dato:str):
    #recibe una lista y un string con el dato que vamos a comparar
    #itera hasta encontra al menor del dato solicitado
    #retorna todos los datos del jugador obtenido

    minimo = None
    jugador_minimo = None
    for jugador in lista:
        valor = jugador['estadisticas'][dato]
        if minimo is None or valor < minimo:
            minimo = valor
            jugador_minimo = jugador
    return jugador_minimo

def calcular_max(lista:list, dato:str):
    #recibe una lista y un string con el dato que vamos a comparar
    #itera hasta encontrar al mayor del dato solicitado
    #generamos listas auxiliares para guardar si hay mas de un maximo
    #imprime el valor y retorna la lista con todos los datos de los jugadores obtenidos

    maximo = None
    jugadores_maximos = []
    nombres_jugadores = []
    for jugador in lista:
        valor = jugador["estadisticas"][dato]
        if maximo is None or valor > maximo:
            maximo = valor
            jugadores_maximos = [jugador]
        elif valor == maximo:
            jugadores_maximos.append(jugador)
    for jugador in jugadores_maximos:
       nombres_jugadores.append(jugador['nombre'])
    print("El/Los jugadores con más {0} con {1} es: {2}".format(dato.replace("_", " "), maximo, " y ".join(nombres_jugadores)))
    return jugadores_maximos

#-------------------- 10-11-12-15-18-20 mayor que el promedio-------------------------------------

def mayores_que_el_promedio(lista: list, numero: int, dato: str):
    #recibe una lista, un numero para verificar si hay mayores que ese numero
    # y un string que es la clave donde vamos a verificar los valores
    #todos los valores que cumplen esa condicion son cargados en una lista
    #en caso que ninguno cumpla la condicion retorna none
    #si alguno la cumplio retorna la lista con los datos

    encontrado = False
    lista_mayores_promedio = []
    for jugador in lista:
        if jugador['estadisticas'][dato] > numero:
            lista_mayores_promedio.append(jugador)
            encontrado = True
    
    if not encontrado:
        return None
       
    return lista_mayores_promedio

def mostrar_datos_requeridos(lista:str, dato1:str ,dato2=None):
    #recibe una listay 2 parametros str que son los que vamos a mostrar 
    #se incia uno con none en caso de que solo se desee mostrar un solo dato ademas del nombre
    #se genera la condicion para dependiendo de los parametros ingresados
    #imprime el msj 
    if dato2 is None:
        for jugador in lista:
            print("{0}: {1}".format(jugador["nombre"], jugador["estadisticas"][dato1]))
    
    else:
        for jugador in lista:
            print("{0} ({1}): {2}".format(jugador["nombre"], jugador[dato2],jugador["estadisticas"][dato1]))

def filtrar_y_mostra_datos(lista:list,numero:int,dato1:str,dato2=None):
    #Recibe una lista, un numero para verificar si hay mayores que ese numero,
    #un string que es la clave donde vamos a verificar los valores, y 2 parametros que son los que vamos a mostrar
    #del retorno de esa lista verificamos la condicion y mostramos los datos que se indicaron por parametro

    lista_filtrada=mayores_que_el_promedio(lista,numero,dato1)
    if lista_filtrada == None:
        print("El valor {} supera el promedio de todos los jugadores".format(numero))

    else:    
        mostrar_datos_requeridos(lista_filtrada,dato1,dato2)

   
#---------------------15- promedio sin el menor-----------------------------------------------

def promedio_puntos_sin_el_menor(lista_jugadores: list):
    # Recibe una lista
    # Calcula el jugador con menor valor
    # Carga en la lista todos los que no sea el jugador minimo
    # Calcula el promedio de puntos por partido del equipo sin el menor
    # Retorna el promedio obtenido

    jugador_minimo = calcular_min(lista_jugadores, "promedio_puntos_por_partido")

    lista_sin_minimo = []
    for jugador in lista_jugadores:
        if jugador != jugador_minimo:
            lista_sin_minimo.append(jugador)

    total_puntos = 0
    cantidad_jugadores = 0

    for jugador in lista_sin_minimo:
        total_puntos += jugador["estadisticas"]["promedio_puntos_por_partido"]
        cantidad_jugadores += 1

    promedio_equipo = total_puntos / cantidad_jugadores

    print("El promedio de puntos del equipo sin el jugador con menos puntos es: {0}".format(promedio_equipo))
    return lista_sin_minimo

#-----------------17 - maximo logros ------------------------------------------------       

def calcular_maximo_logros(lista: list):
    # Recibe una lista de jugadores
    # Compara la cantidad máxima de logros entre los jugadores
    # imprime el/los jugadores que tienen la mayor cantidad de logros
    # retorna los jugadores con mas logros
    maximo = None
    jugadores_maximos = []
    
    for jugador in lista:
        valor = len(jugador['logros'])
        if maximo is None or valor > maximo:
            maximo = valor
            jugadores_maximos = [jugador]
        elif valor == maximo:
            jugadores_maximos.append(jugador)
    
    nombres_jugadores = [jugador['nombre'] for jugador in jugadores_maximos]
    
    print("El/los jugadores con más logros son {1} con {0}".format(maximo, "y ".join(nombres_jugadores)))
    return jugadores_maximos


#----------------------MAIN------------------------------------------------------------

lista_jugadores=leer_archivo("D:\Documentos\programacion.prueba\PrimerParcial\dt.json","jugadores")

while True:
    # Mostrar menú de opciones
    print("Menú de opciones:")
    print("1. Lista de todo los jugadores")
    print("2. indque de que jugador quiere ver las estadisticas")
    print("3. Guardar estadisticas en CSV")
    print("4. Mostrar logros de un jugador")
    print("5. Promedio de puntos por partido ordenado por nombre de manera ascendente")
    print("6. Buscar jugador en los miembro del salon de la fama")
    print("7. Jugador con la mayor cantidad de rebotes totales")
    print("8. Jugador con el mayor porcentaje de tiros de campo.")
    print("9. Jugador con la mayor cantidad de asistencias totales.")
    print("10. Jugadores que han promediado más puntos por partido que el valor indicado.")
    print("11. Jugadores que han promediado más rebotes por partido que el valor indicado. ")
    print("12. Jugadores que han promediado más asistencias por partido que el valor indicado.")
    print("13. Jugador con la mayor cantidad de robos totales.")
    print("14. Jugador con la mayor cantidad de bloqueos totales.")
    print("15. Jugadores que hayan tenido un porcentaje de tiros libres que el valor indicado.")
    print("16. Promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido.")
    print("17. Jugador con la mayor cantidad de logros obtenidos")
    print("18. Jugadores que hayan tenido un porcentaje de tiros triples que el valor indicado.")
    print("19. jugador con la mayor cantidad de temporadas jugadas")
    print("20. jugadores ordenados por posicion que tenga un porcentaje de tiros de campo superior al valor indicado")


    print("0. Salir del programa")
    opcion = input("\nIngrese la opción deseada: ")

    # Opcion 1: 
    if opcion == "1":
       nombre_y_posicion=mostrar_todos(lista_jugadores)
       imprimir_lista(nombre_y_posicion)

   # Opción 2: 
    elif opcion == "2":
       estadisticas_jugador=seleccionar_jugador(lista_jugadores)
       imprimir_dato(estadisticas_jugador)     

    # Opción 3:
    elif opcion == "3":
        contenido = parser_csv(estadisticas_jugador)   
        guardar_archivo("estadisticas_jugador.csv", contenido)

    elif opcion == "4":
        jugadores_buscados = buscar_por_nombre(lista_jugadores)
        if jugadores_buscados:
            mostrar_logros(lista_jugadores,jugadores_buscados)
        else:
            print("No se encontró ningún jugador")

    # Opción 5:
    elif opcion == "5":
        resultado_promedio=promedio_totales(lista_jugadores,"promedio_puntos_por_partido")
        imprimir_dato(resultado_promedio)
        lista_ordenada_nombre=ordenar_por_key(lista_jugadores,"nombre",True)
        mostrar_datos_requeridos(lista_jugadores,"promedio_puntos_por_partido")
        
    # Opción 6: 
    elif opcion == "6":
        jugadores_buscados = buscar_por_nombre(lista_jugadores)
        if jugadores_buscados:
            es_miembro_del_salon_de_la_fama2(lista_jugadores, jugadores_buscados)
        else:
            print("No se encontró ningún jugador")
    
    #opcion 7: 
    elif opcion == "7":
       calcular_max(lista_jugadores,"rebotes_totales")   
      
    # Opcion 8: 
    elif opcion == "8":
       calcular_max(lista_jugadores,"porcentaje_tiros_de_campo")

    # Opcion 9: 
    elif opcion == "9":
        calcular_max(lista_jugadores,"promedio_asistencias_por_partido")      
    
    # Opcion 10: 
    elif opcion == "10":
        numero_ingresado=solicitar_numero("ingrese un numero: ")
        filtrar_y_mostra_datos(lista_jugadores,numero_ingresado,"promedio_puntos_por_partido")

    # Opcion 11: 
    elif opcion == "11":
       numero_ingresado=solicitar_numero("ingrese un numero: ")
       filtrar_y_mostra_datos(lista_jugadores,numero_ingresado,"promedio_rebotes_por_partido")     

    # Opcion 12: 
    elif opcion == "12":
       numero_ingresado=solicitar_numero("ingrese un numero: ")
       filtrar_y_mostra_datos(lista_jugadores,numero_ingresado,"promedio_asistencias_por_partido")
       
    # Opcion 13: 
    elif opcion == "13":  
        calcular_max(lista_jugadores,"robos_totales")

    # Opcion 14: 
    elif opcion == "14":  
        calcular_max(lista_jugadores,"bloqueos_totales")
    
    # Opcion 15: 
    elif opcion == "15":
        numero_ingresado=solicitar_numero("ingrese un numero: ")
        filtrar_y_mostra_datos(lista_jugadores,numero_ingresado,"porcentaje_tiros_libres")
    
    # Opcion 16: 
    elif opcion == "16":
        promedio_puntos_sin_el_menor(lista_jugadores)
        
    # Opcion 17: 
    elif opcion == "17":
        jugador_max_logros=calcular_maximo_logros(lista_jugadores)
        
    # Opcion 18: 
    elif opcion == "18":
        numero_ingresado=solicitar_numero("ingrese un numero: ")
        filtrar_y_mostra_datos(lista_jugadores,numero_ingresado,"porcentaje_tiros_triples")

    # Opcion 19: 
    elif opcion == "19":
        calcular_max(lista_jugadores,"temporadas")
               
    # Opcion 20: 
    elif opcion == "20":
        numero_ingresado=solicitar_numero("ingrese un numero: ")
        lista_ordenada_por_posicion=ordenar_por_key(lista_jugadores,"posicion", True)
        filtrar_y_mostra_datos(lista_ordenada_por_posicion,numero_ingresado,"porcentaje_tiros_de_campo","posicion")

    # Opcion 0: Salir
    elif opcion == "0":
        pass

    else:
     print("Opción inválida. Intente de nuevo.")

     
