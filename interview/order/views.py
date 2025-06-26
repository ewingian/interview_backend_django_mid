from datetime import datetime

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderSetInactiveView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_queryset(id=kwargs["id"])
        # I dont see this in the model; im not sure if this is the correct flag
        instance.is_active = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderListEmbargoDateView(APIView):
    """ Get a list of orders specified by a start date and an embargo data """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self, start_date: str, embargo_date: str) -> Response:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            embargo_date = datetime.strptime(embargo_date, "%Y-%m-%d").date()
            serializer = self.serializer_class(
                self.queryset.filter(start_date__range=[start_date, embargo_date]), many=True)
            return Response(serializer.data, status=200)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

