from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from pizza.models import Order
from pizza.serializers import *
from rest_framework import generics
from rest_framework.exceptions import APIException
from pizza.permissions import IsOwnerOrReadOnly, IsOrderAuthor


class ListOrderApi(generics.ListAPIView):
    model = Order
    #queryset=Order.objects.all();
    serializer_class = RetrieveOrderSerializer
    permission_classes = []

    def get_queryset(self):
        filter_status = self.request.GET.get('status', None)
        filter_customer = self.request.GET.get('customer', None)
        if filter_status is not None and filter_customer is not None:
            queryset = Order.objects.filter(status__icontains=filter_status, customer_name__icontains=filter_customer).order_by("-created")
            return queryset
        elif filter_status is not None:
            queryset = Order.objects.filter(status__icontains=filter_status).order_by("-created")
            return queryset
        elif filter_customer is not None:
            queryset = Order.objects.filter(customer_name__icontains=filter_customer).order_by('-created')
            return queryset
        else:
            queryset = Order.objects.all().order_by("-created")
            return queryset

    # def get_permissions(self):
    #     """Переопределяем метод"""
    #     if self.action in ['create', 'myposts']:
    #         permissions = [IsAuthenticated, ]
    #     elif self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsAuthenticated, IsPostAuthor]
    #     else:
    #         permissions = []
    #     return [permission() for permission in permissions]


class CreateOrderApi(generics.CreateAPIView):
    Model = Order
    serializer_class = CreateOrderSerializer
    permission_class = [IsAuthenticated, ]


# Retrieve Single Object GET REQUEST
class RetrieveOrderApi(generics.RetrieveAPIView):
    model = Order
    queryset = Order.objects.all()
    serializer_class = RetrieveOrderSerializer
    permission_class = [IsAuthenticated, IsOrderAuthor, ]
    lookup_field = 'pk'


class UpdateOrderApi(generics.RetrieveUpdateAPIView):
    model = Order
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer
    permission_class = [IsAuthenticated, IsOrderAuthor, ]
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        obj=self.get_object()
        if obj.status in ["canceled", "delivered"]:
            raise APIException("Canceled order Or Delivered Order Can't Be Updated")
        return self.update(request, *args, **kwargs)


class DeleteOrderApi(generics.RetrieveDestroyAPIView):
    model = Order
    queryset = Order.objects.all()
    permission_class = [IsAuthenticated, IsOrderAuthor, ]
    lookup_field = 'pk'
    serializer_class = RetrieveOrderSerializer
