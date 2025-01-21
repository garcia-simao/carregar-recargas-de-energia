
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from core.views import UsuarioViewSet
from core.views import CarregarRecargaViewSet
from core.views import InformacoesClienteViewSet
from core.views import CustomLoginView
from core.views import PasswordRedefinirEnviarEmailViewset
from core.views import NovaPasswordRedefinirViewSet
from core.views import TotalCarregamentosViewSet



router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'carregar-recarga', CarregarRecargaViewSet, basename='carregar-recarga')
router.register(r'informacoes-cliente', InformacoesClienteViewSet)
router.register(r'total-de-carregamentos-usuario', TotalCarregamentosViewSet, basename='total-carregamentos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('email-redefinir-palavra-passe/', PasswordRedefinirEnviarEmailViewset.as_view(), name='palavra-passe'),
    path('repor-password/', NovaPasswordRedefinirViewSet.as_view(), name='palavra-passe-confirmar'),
    path('api-auth',include('rest_framework.urls')),
]
