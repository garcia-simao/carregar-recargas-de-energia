from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import firestore





class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    nif = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    endereco = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    numero_de_conta = models.IntegerField()
    numero_do_contador = models.IntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    
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
