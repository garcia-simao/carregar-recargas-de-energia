from rest_framework import serializers
from .models import Usuario
from .models import CarregarRecarga
from .models import InformacoesCliente




class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 
                  'nome', 
                  'sobrenome', 
                  'telefone', 
                  'nif', 
                  'email', 
                  'endereco',
                  'password', 
                  'numero_de_conta',
                  'numero_do_contador',
                  'data_criacao']

class CarregarRecargaSerializer(serializers.ModelSerializer):
    id_do_usuario_dados = serializers.SerializerMethodField()
    id_do_usuario = serializers.PrimaryKeyRelatedField(queryset = Usuario.objects.all() ) 

    class Meta:
        model = CarregarRecarga
        fields = ['id', 
                  'id_do_usuario',
                  'id_do_usuario_dados', 
                  'codigo_da_recarga', 
                  'data_criacao']
    
    
    def get_id_do_usuario_dados(self, obj):

        return{
            'id': obj.id_do_usuario.id,
            'nome': obj.id_do_usuario.nome,
            'sobrenome': obj.id_do_usuario.sobrenome,
            'telefone': obj.id_do_usuario.telefone,
            'nif': obj.id_do_usuario.nif,
            'email': obj.id_do_usuario.email,
            'endereco': obj.id_do_usuario.endereco,
            'numero_de_conta': obj.id_do_usuario.numero_de_conta,
            'numero_do_contador': obj.id_do_usuario.numero_do_contador,
        }
    

class InformacoesClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformacoesCliente
        fields = ['id', 
                  'id_do_usuario', 
                  'status_debito_directo',
                  'iban',
                  'limite_de_carregamento_mensal', 
                  'data_criacao']