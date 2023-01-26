from django.db import models


class Funcionario(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    sobrenome = models.CharField(max_length=30, null=False, blank=False)
    cpf = models.CharField(max_length=14, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    remuneracao = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.CharField(max_length=60, null=False, blank=False)
    imagem_produto = models.ImageField(null=False, blank=False, upload_to='erp/static/img/produtos/')
    preco = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    quantidade = models.CharField(max_length=10485759, null=False, blank=False)
    descricao = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.produto


class Venda(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    produto = models.ForeignKey('Estoque', on_delete=models.CASCADE)
    valor_venda = models.CharField(max_length=10485759, null=False, blank=False)
    quantidade = models.CharField(max_length=10485759, null=False, blank=False)
    descricao = models.TextField(max_length=255, null=False, blank=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.funcionario} {self.produto}'

