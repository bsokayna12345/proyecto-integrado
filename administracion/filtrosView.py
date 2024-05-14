


import json
from django.http import JsonResponse

from main.models import SubCategoria


def filtro_subcategoria_categoria(request):
    """ filtrar las sub categoria de una categoria """    
    data = dict()
    try:
        id_filter = request.POST['filter_value']
        if id_filter:
            qsSubCategoria = SubCategoria.objects.filter(categoria_id__id=id_filter).all()
            print('sub_categorias', qsSubCategoria)
            resultado_list = list()
            for item in  qsSubCategoria:
                nombre = f"{item.nombre}"
                resultado_list.append({'id':item.id, 'texto':nombre})
            list_json = json.dumps(resultado_list)
            data = dict(
                status=200,
                statusText="ok",
                content=list_json
            )
    except Exception as err:
        data = dict(
            status=500,
            statusText=err,
            content="None",
        )
    return JsonResponse(data)


