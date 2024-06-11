from main.models import Carrito_Detalle

def carrito_unidades(request):
    contador_unidades_carrito = 0  # Inicializa el contador
    if request.user.is_authenticated:
        qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
    else:
        qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)
    if qsCarrito.count() > 0:
        for carrito_id in qsCarrito:
            contador_unidades_carrito += carrito_id.unidades
    return {'contador_unidades_carrito': contador_unidades_carrito}
