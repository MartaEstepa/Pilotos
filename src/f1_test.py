from f1 import *


def lee_carreras_test(ruta_csv:str):
    datos = lee_carreras(ruta_csv)
    return datos


def media_tiempo_boxes_test(carreras:list[Carrera], ciudad:str, fecha:date | None =None):
    datos = media_tiempo_boxes(carreras, ciudad, fecha)
    return datos

def pilotos_menor_tiempo_medio_vueltas_top_test(carreras:list[Carrera], n):
    datos = pilotos_menor_tiempo_medio_vueltas_top(carreras, n)
    return datos

def ratio_tiempo_boxes_total_test(carreras:list[Carrera]):
    datos = ratio_tiempo_boxes_total(carreras)
    return(datos)



if __name__  == '__main__':
    registro = lee_carreras_test('data/f1.csv')
    print(registro)
    print('Media en boxes =', media_tiempo_boxes_test(registro, 'Abu Dhabi'))
    print(f'Pilotos con menor tiempo medio de vueltas top son {pilotos_menor_tiempo_medio_vueltas_top_test( registro, 4)}')
    print('Los ratios de los pilotos por carrera son:', ratio_tiempo_boxes_total_test(registro))