from main.models import OrderList
from django.template.loader import render_to_string
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from main.serializers import OrderListSerializer


@csrf_exempt
def OrderList_detail(request):
    if (request.method == 'GET'):
        # получаем все заказы
        ordlist = OrderList.objects.all()
        # сериализируем их
        serializer = OrderListSerializer(ordlist, many=True)
        # return a Json
        return JsonResponse(serializer.data, safe=False)