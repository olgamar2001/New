from django.shortcuts import render
from rest_framework import viewsets
from .models import Product, Lesson, UserBalance
from .serializers import ProductSerializer, LessonSerializer, UserBalanceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from random import choice

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        user = request.user
        product = self.get_object()
        
        balance = UserBalance.objects.get(user=user)
        if balance.balance < product.price:
            return Response({"detail": "Not enough balance."}, status=400)

        balance.balance -= product.price
        balance.save()
        
        
        user.courses.add(product)

        
        group_number = choice(range(1, 11))

        return Response({"detail": "Purchase successful."})

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class UserBalanceViewSet(viewsets.ModelViewSet):
    queryset = UserBalance.objects.all()
    serializer_class = UserBalanceSerializer
    
from django.shortcuts import render
from .models import Course  

from django.http import HttpResponse
  
def index(request):
    return HttpResponse("courses")