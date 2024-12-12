
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from core.views import UsuarioViewSet
from core.views import CarregarRecargaViewSet
from core.views import InformacoesClienteViewSet



router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'carregar-recarga', CarregarRecargaViewSet)
router.register(r'informacoes-cliente', InformacoesClienteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth',include('rest_framework.urls')),
]
