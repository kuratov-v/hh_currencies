from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from main_app import services


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def currencies_view(request):
    if request.method == 'GET':
        params = request.query_params.dict()
        if not params:
            currencies = services.get_currencies()
            return Response({"currencies": currencies})
        try:
            response = services.get_difference(params['date1'], params['date2'], params['char_code'])
            return Response({"success": response})
        except KeyError as e:
            return Response({"error": f'Missing params: {e.args[0]}'})


