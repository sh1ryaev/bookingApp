from rest_framework import routers,serializers,viewsets

from main.models import OrderList


class OrderListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderList
        fields = ['id', 'id_renter', 'id_rent_num', 'id_rent_obj', 'start_date', 'finish_date', 'summ']