from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import firestore
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo de e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    nif = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    endereco = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    numero_de_conta = models.IntegerField()
    numero_do_contador = models.IntegerField()
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects= UsuarioManager()

    def __str__(self):
        return self.nome
    
    def get_by_natural_key(self, email):
        return self.__class__.objects.get(email=email)
    

    #função que encripta a palavra passe para que todo o usuario criado seja superusuario
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    
#função que gera o token para qualquer usuario criado    
@receiver(post_save, sender=Usuario)
def report_uploaded(sender, instance, created, **kwards):
    if created:
        Token.objects.get_or_create(user=instance)



class CarregarRecarga(models.Model):
    id_do_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    codigo_da_recarga = models.IntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Código de recarga : {self.codigo_da_recarga} - Usuário: {self.id_do_usuario.nome} "
    

class InformacoesCliente(models.Model):
    id_do_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    status_debito_directo = models.BooleanField()
    iban = models.CharField(max_length=40)
    limite_de_carregamento_mensal = models.IntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Iban : {self.iban} - Usuário: {self.id_do_usuario.nome} "


#enviar registos para firebase
@receiver(post_save, sender=CarregarRecarga)
def enviar_para_firebase(sender, instance, created, **kwargs):
    if created:
        # Conectar ao Firestore
        db = firestore.client()

        # Formatar os dados
        dados = {
            "id": instance.id,
            "id_do_usuario": instance.id_do_usuario.id,
            "id_do_usuario_dados": {
                "id": instance.id_do_usuario.id,
                "nome": instance.id_do_usuario.nome,
                "sobrenome": instance.id_do_usuario.sobrenome,
                "telefone": instance.id_do_usuario.telefone,
                "nif": instance.id_do_usuario.nif,
                "email": instance.id_do_usuario.email,
                "endereco": instance.id_do_usuario.endereco,
                "numero_de_conta": instance.id_do_usuario.numero_de_conta,
                "numero_do_contador": instance.id_do_usuario.numero_do_contador,
            },
            "codigo_da_recarga": instance.codigo_da_recarga,
            "data_criacao": instance.data_criacao.isoformat(),
        }

        # Enviar os dados para o Firestore na coleção `CarregarRecarga`
        db.collection("CarregarRecarga").document(str(instance.id)).set(dados)
