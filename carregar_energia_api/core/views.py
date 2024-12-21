from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from dj_rest_auth.views import LoginView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.response import Response
from django.utils.encoding import force_str
from rest_framework import viewsets, status, generics


from .models import Usuario
from .serializers import UsuarioSerializer
from .models import CarregarRecarga
from .serializers import CarregarRecargaSerializer
from .models import InformacoesCliente
from .serializers import InformacoesClienteSerializer
from .serializers import CustomLoginSerializer
from .serializers import PasswordRedefinirEmailSerializer
from .serializers import PasswordRedefinirConfirmarSerializer


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
    
Usuario = get_user_model()
#Enviar email ao usuario para redefinir a password
#quando tiver dominio a url deve ser http://duty.ao/#/repor-password/?uid=MQ&token=cie39l-9c04b635f59b03a24d0ef5ba3b5409cb
#enquanto não tiver dominio: http://localhost:8000/repor-password/?uid=MQ&token=cie39l-9c04b635f59b03a24d0ef5ba3b5409cb
class PasswordRedefinirEnviarEmailViewset(GenericAPIView):
    serializer_class = PasswordRedefinirEmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_active:
            self.send_resetpassword_email(request, user)
            return Response({"message": "E-mail de redefinição de senha enviado"}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "Usuário não está ativo"}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_resetpassword_email(self, request, user):
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        application_url = 'http://localhost:8000'
        
        absurl = f'{application_url}/repor-password/?uid={uid}&token={token}'
        subject = 'Altere a sua password'
        message = f'Olá {user.nome} {user.sobrenome},\n\nRecebemos o seu pedido de alteração da senha. Use o link abaixo para redefinir a sua senha:\n\n{absurl}\n\nSe você não solicitou a alteração, por favor ignore este e-mail.\n\nObrigado!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        
        send_mail(subject, message, email_from, recipient_list)

#para redifinir a nova password
class NovaPasswordRedefinirViewSet(generics.GenericAPIView):
    serializer_class = PasswordRedefinirConfirmarSerializer
    permission_classes = (AllowAny,)

    
 
    def put(self, request):
        try:
            uid = force_str(urlsafe_base64_decode(request.data.get("uidb64")))
            user = Usuario.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
            user = None
 
        if user is not None and default_token_generator.check_token(user, request.data.get("token")):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                #não precisa encriptar mais pois ja esta encriptada para não dar conflitos.
                user.password = serializer.validated_data.get("password1")
                user.save()
                print(user.password)
                return Response({"message": "Palavra passe redefinida com sucesso."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Falha ao redefinir a palavra passe"}, status=status.HTTP_400_BAD_REQUEST)     
