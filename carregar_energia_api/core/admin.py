from django.contrib import admin
from .models import Usuario
from .models import CarregarRecarga
from .models import InformacoesCliente

admin.site.register(Usuario)
admin.site.register(CarregarRecarga)
admin.site.register(InformacoesCliente)