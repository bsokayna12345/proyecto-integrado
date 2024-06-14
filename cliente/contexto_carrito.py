from main.models import Carrito_Detalle

# def carrito_unidades(request):
#     contador_unidades_carrito = 0  # Inicializa el contador

#     # Obtén el carrito de la sesión
#     carrito = request.session.get('carrito', {})

#     # Recorre los productos en el carrito y suma las unidades
#     for item in carrito.values():
#         contador_unidades_carrito += item['unidades']

#     return {'contador_unidades_carrito': contador_unidades_carrito}