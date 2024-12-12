from django.shortcuts import render
from rest_framework import viewsets

from .models import Usuario
from .serializers import UsuarioSerializer
from .models import CarregarRecarga
from .serializers import CarregarRecargaSerializer
from .models import InformacoesCliente
from .serializers import InformacoesClienteSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer 


class CarregarRecargaViewSet(viewsets.ModelViewSet):
    queryset = CarregarRecarga.objects.all()
    serializer_class = CarregarRecargaSerializer 

class InformacoesClienteViewSet(viewsets.ModelViewSet):
    queryset = InformacoesCliente.objects.all()
    serializer_class = InformacoesClienteSerializer 

