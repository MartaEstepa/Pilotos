from collections import defaultdict
from datetime import date, datetime
from typing import NamedTuple
import csv

Carrera = NamedTuple("Carrera", 
            [("nombre", str),
             ("escuderia", str),
             ("fecha_carrera", date) ,
             ("temperatura_min", int),
             ("vel_max", float),
             ("duracion",float),
             ("posicion_final", int),
             ("ciudad", str),
             ("top_6_vueltas", list[float]),
             ("tiempo_boxes",float),
             ("nivel_liquido", bool)
            ])


# Fernando Alonso;Aston Martin;21-11-22;25;330.1;30.5;-1;Abu Dhabi;[31.254/ 31.567/ 31.789/ 32.045/ -/ -];15.23;no

def lee_carreras(ruta_csv) -> list[Carrera]:
    with open(ruta_csv, encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)
        res = []
        for nombre,escuderia,fecha_carrera,temperatura_min,vel_max,duracion,posicion_final,ciudad,top_6_vueltas,tiempo_boxes,nivel_liquido in lector:
            nombre = str(nombre)
            escuderia = str(escuderia)
            fecha_carrera = datetime.strptime(fecha_carrera, '%d-%m-%y').date() #como el year es 21 en vez de 2021, se escribe %y en vez de %Y
            temperatura_min = int(temperatura_min)
            vel_max = float(vel_max)
            duracion = float(duracion)
            posicion_final = int(posicion_final)
            ciudad = str(ciudad)
            top_6_vueltas = parsea_top_6_vueltas(top_6_vueltas)
            tiempo_boxes = float(tiempo_boxes)
            if nivel_liquido == 'no':
                nivel_liquido = False
            else:
                nivel_liquido = True
            
            tupla = Carrera(nombre,escuderia,fecha_carrera,temperatura_min,vel_max,duracion,posicion_final,ciudad,top_6_vueltas,tiempo_boxes,nivel_liquido)
            res.append(tupla)
        return res

        
# [31.254/ 31.567/ 31.789/ 32.045/ -/ -]

def parsea_top_6_vueltas(lista_top: str) -> list[float]:
    lista_top = lista_top.replace('[', '').replace(']', '')
    # Otra forma: lista_top = lista_top.strip('[])
    lista_top = lista_top.replace(' ', '')
    res = []
    for trozo in lista_top.split('/'):
        if trozo == '-':
            res.append(0)
        else:
            res.append(float(trozo))
    return res


def media_tiempo_boxes(carreras:list[Carrera], ciudad:str, fecha:date | None =None)->float:
    '''
    recibe una lista de tuplas de tipo Carrera, una ciudad y una fecha (con valor por defecto None), 
    y devuelve la media de tiempo en boxes que los pilotos han pasado en la fecha y ciudad seleccionada. 

    Si la fecha es None se sumarán todos los tiempos de la ciudad sin tener en cuenta la fecha. Por otro 
    lado, si no ha habido carreras en la fecha y ciudad seleccionada, la media debe ser 0.
    '''
    sum = 0
    contador = 0
    for n in carreras:
        if n.ciudad == ciudad:
            if fecha == None or fecha == n.fecha_carrera:
                sum += n.tiempo_boxes
                contador += 1
            else:
                print('Media =', 0)
    return sum/contador


def pilotos_menor_tiempo_medio_vueltas_top(carreras:list[Carrera], n)->list[tuple[str,date]]:
    '''
    recibe una lista de tuplas de tipo Carrera y un número entero n, y devuelve una lista de 
    tuplas (nombre, fecha) con los n nombres y fechas de carrera de los pilotos cuya media de tiempo
    en sus 6 vueltas top sea menor. 
    
    No se tendrán en cuenta aquellos pilotos que han sufrido un 
    accidente y no han podido completar las 6 vueltas.
    '''
    res = []
    for p in carreras:
        sum = 0
        if 0 not in p.top_6_vueltas:
            for m in p.top_6_vueltas:
                sum += m
            media = sum/6
            res.append((p.nombre,media,p.fecha_carrera))

    ordenada =  sorted(res, key = lambda x:x[1])[:n]
    last = []
    for a,b,c in ordenada:
        last.append((a,c))
    return last



def ratio_tiempo_boxes_total(carreras:list[Carrera])->list[tuple[str,date, float]]:
    '''
    recibe una lista de tuplas de tipo Carrera, y devuelve una lista de tuplas (nombre, fecha, ratio)
    con el nombre del piloto, la fecha de la carrera y la ratio entre su tiempo en boxes con respecto 
    al total de tiempo en boxes de todos los pilotos que han participado ese día en la carrera. 
    
    La lista de tuplas resultante deberá estar ordenada de mayor a menor ratio.
    '''
    res = []
    for p in carreras:
        fecha = p.fecha_carrera
        ciudad = p.ciudad
        media_that_day = media_tiempo_boxes(carreras, ciudad, fecha)
        ratio_piloto = p.tiempo_boxes / media_that_day
        res.append((p.nombre, p.fecha_carrera, ratio_piloto))
    return res


def ratio_tiempo_boxes_total(carreras:list[Carrera])->list[tuple[str,date, float]]:
    '''
    recibe una lista de tuplas de tipo Carrera y devuelve un diccionario que asocia 
    cada piloto (claves) con una lista con los puntos totales obtenidos cada año. 

    La lista de puntos estará ordenada por año. 
    
    Para calcular los puntos obtenidos en cada carrera debe tener en cuenta que solamente obtienen puntos aquellos pilotos 
    que queden en las 3 primeras posiciones. Si el puesto es el primero, los puntos 
    serían 50, el segundo puesto son 25 y el tercero 10.
    
    Para esta función tiene que utilizar 
    obligatoriamente una función auxiliar que, dada una carrera, calcule el número de puntos de esa carrera.
    '''
    dic = defaultdict(list)
