from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (initial, cadastro_funcionario, lista_funcionarios,
                    editar_funcionario, deletar_funcionario, cadastrar_produto, lista_produtos,
                    editar_produto, deletar_produto, cadastrar_venda, lista_vendas, busca_produto)


urlpatterns = [
    path('', initial, name='initial'),
    path('cadastro-funcionario/', cadastro_funcionario, name='cadastro-funcionario'),
    path('lista-funcionarios/', lista_funcionarios, name='lista-funcionarios'),
    path('editar-funcionario/<str:pk>/', editar_funcionario, name='editar-funcionario'),
    path('deletar-funcionario/<str:pk>/', deletar_funcionario, name='deletar-funcionario'),
    path('cadastrar-produto', cadastrar_produto, name='cadastrar-produto'),
    path('lista-produtos', lista_produtos, name='lista-produtos'),
    path('editar-produto/<str:pk>/', editar_produto, name='editar-produto'),
    path('deletar-produto/<str:pk>/', deletar_produto, name='deletar-produto'),
    path('cadastrar-venda/', cadastrar_venda, name='cadastrar-venda'),
    path('lista-vendas/', lista_vendas, name='lista-vendas'),
    path('busca-produto/', busca_produto, name='busca-produto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
