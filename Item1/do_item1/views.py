from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *
# Create your views here.
class StudentVS(viewsets.ModelViewSet):
    serializer_class = Studentser
    queryset = Student.objects.all()
