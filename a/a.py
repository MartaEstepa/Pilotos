from typing import NamedTuple
from datetime import date

Pedido = NamedTuple('Pedido', [('fecha', date), ('producto', str), ('cantidad', int)])

def producto_pedido_mayor(pedidos: list[Pedido], fecha_min: date) -> str:
    mas_unidades = None
    for n in pedidos:
        if n.fecha > fecha_min or fecha_min == None:
            if mas_unidades.cantidad < n.cantidad or mas_unidades == None:
                mas_unidades = n
    return mas_unidades.producto


Pedido = [((2020,11,5), 'manzanas', 10), ((2019,3,7), 'camiseta', 30), ((2020,9,20), 'libros', 22)]




producto_pedido_mayor(Pedido, None)
