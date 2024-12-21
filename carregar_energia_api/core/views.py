from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from rest_framework import status

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

#definição dos campos que serão visiveis após um determinado usuarioS fazer login
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    permission_classes= [AllowAny]

    def get_response(self):
        response = super().get_response()
        if response.status_code == status.HTTP_200_OK:
            user = self.user

            usuario_data = {
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'sobrenome': user.sobrenome,
                'endereco': user.endereco,
                'telefone': user.telefone,
                'nif': user.nif,
                # campos exibidos do usuario que fez login
            }
            response.data['usuario_data'] = usuario_data
        return response