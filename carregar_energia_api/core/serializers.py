from rest_framework import serializers
from .models import Usuario
from .models import CarregarRecarga
from .models import InformacoesCliente
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate, get_user_model



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
    
    def create(self, validated_data):
        # Cria o usuário
        usuario = Usuario.objects.create(**validated_data)
        
        return usuario

class CustomLoginSerializer(LoginSerializer):
    username=None
    
    class Meta:
        model = Usuario
        fields = ['id',
                  'nome',
                  'email',
                  'sobrenome',
                  'endereco',
                  'telefone',
                  'nif',
                  ]


    def validate(self, data):
        email = data.get('email')
        senha = data.get('password')

        # Verifica se o e-mail e senha são fornecidos
        if email and senha:
            # Autentica o usuário
            user = authenticate(request=self.context.get('request'), username=email, password=senha)

            # Se a autenticação falhar, levante a exceção personalizada
            if user is None:
                if not self.user_exists(email):
                    raise serializers.ValidationError({'email': 'E-mail incorreto.'})
                else:
                    raise serializers.ValidationError({'senha': 'Senha incorreta.'})

            # Se o usuário estiver inativo, levante a exceção personalizada
            if not user.is_active:
                raise serializers.ValidationError('Esta conta está inativa.')

        else:
            raise serializers.ValidationError('E-mail e senha são necessários para fazer login.')

        data['user'] = user
        return data

    def user_exists(self, email):
        return self.get_user(email) is not None

    def get_user(self, email):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(email=email)
        except UserModel.DoesNotExist:
            return None

User = get_user_model()
class PasswordRedefinirEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(("Este email não está registrado no banco de dados."))
        return value
    
class PasswordRedefinirConfirmarSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Verifica se password1 e password2 são iguais.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("As palavras-passe não coincidem.")
        return data

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