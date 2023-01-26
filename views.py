from django.shortcuts import render, redirect
from .forms import FuncionarioForm, EstoqueForm, VendaForm
from django.contrib import messages
from .models import Funcionario, Estoque, Venda
import locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


def initial(request):
    vendas = Venda.objects.all()
    funcionarios_vendas = [{f'{venda.funcionario}': {'receita': float(venda.produto.preco * int(venda.quantidade)),
                                                     'produto': {venda.produto.produto: int(venda.quantidade), }, }} for venda in vendas]

    ranking = dict()
    # para cada funcionario e suas vendas
    for funcionario_venda in funcionarios_vendas:
            # separando o funcionario de sua venda
        for funcionario, informacoes in funcionario_venda.items():
            # se o funcionario já foi posto no ranking
            if funcionario in ranking:
                ranking[funcionario]['receita'] += informacoes['receita']
                # list(informacoes['produto'].keys())[0] pegando o produto relacionado a venda feita
                # list(informacoes['produto'].values())[0] pegando a quantidade de produto relacionada a venda feita
                # se o produto já foi computado em uma venda anterior, apenas somando a nova quantidade à antiga.
                if list(informacoes['produto'].keys())[0] in list(ranking[funcionario]['produto'].keys()):
                    ranking[funcionario]['produto'][list(informacoes['produto'].keys())[0]] += list(informacoes['produto'].values())[0]
                else:
                    ranking[funcionario]['produto'][list(informacoes['produto'].keys())[0]] = list(informacoes['produto'].values())[0]
            # caso funcionario ainda não esteja no ranking
            else:
                ranking[funcionario] = informacoes

    # adicionando o produto mais vendido
    for funcionario, venda in ranking.items():
        l = [valor for valor in list(venda['produto'].values())]
        maior = max(l)
        for k, v in venda['produto'].items():
            if maior == v:
                ranking[funcionario]['produto_mais_vendido'] = k

    ranking_tupla = [[f, i['receita'], i['produto_mais_vendido']] for f, i in ranking.items()]

    def take_second(elem):
        return elem[1]

    ranking_pronto = sorted(ranking_tupla, key=take_second, reverse=True)

    def formata_ranking(ranking_formatar):
        for k in ranking_formatar:
            k[1] = locale.currency(k[1], grouping=True, symbol=True)
        return ranking_formatar

    ranking_pronto_formatado = formata_ranking(ranking_pronto)

    context = {'ranking_pronto_formatado': ranking_pronto_formatado}

    return render(request, 'index.html', context)


def cadastro_funcionario(request):
    if str(request.method) == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            form = FuncionarioForm()
            messages.success(request, 'Cadastro efetuado com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar funcionário.')
    else:
        form = FuncionarioForm()

    context = {
        'form': form,
    }

    return render(request, 'cadastrar_funcionario.html', context)


def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()

    for funcionario in funcionarios:
        funcionario.remuneracao = locale.currency(float(funcionario.remuneracao), grouping=True, symbol=True)

    context = {'funcionarios': funcionarios}

    return render(request, 'lista_funcionarios.html', context)


def editar_funcionario(request, pk):
    funcionario = Funcionario.objects.get(id=pk)
    form = FuncionarioForm(instance=funcionario)
    nome_funcionario = str(funcionario.nome)
    if str(request.method) == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações editadas com sucesso!')
            return redirect('/lista-funcionarios/')
        else:
            messages.error(request, f'Erro ao editar informações de {nome_funcionario.title()}')

    context = {
        'form': form,
        'nome_funcionario': nome_funcionario,
    }

    return render(request, 'editar_funcionario.html', context)


def deletar_funcionario(request, pk):
    funcionario = Funcionario.objects.get(id=pk)
    nome_full = f'{funcionario.nome} {funcionario.sobrenome}'.title()
    if str(request.method) == 'POST':
        funcionario.delete()
        messages.error(request, f'{nome_full.title()} Deletado com sucesso!')
        return redirect('/lista-funcionarios/')

    context = {
        'funcionario': funcionario,
        'nome_full': nome_full,
    }

    return render(request, 'deletar_funcionario.html', context)


def cadastrar_produto(request):
    if str(request.method) == 'POST':
        form = EstoqueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = EstoqueForm()
            messages.success(request, 'Produto cadastrado com sucesso!')
        else:
            messages.error(request, 'Erro ao cadastrar produto!')
    else:
        form = EstoqueForm()
    context = {
        'form': form,
    }

    return render(request, 'cadastrar_produto.html', context)


def lista_produtos(request):
    produtos = Estoque.objects.all()

    def separa_milhar(valor, separador='.'):
        return valor if len(valor) <= 3 else separa_milhar(valor[:-3], separador) + separador + valor[-3:]

    for produto in produtos:
        produto.preco = locale.currency(float(produto.preco), grouping=True, symbol=True)
        produto.quantidade = separa_milhar(produto.quantidade)

    context = {
        'produtos': produtos,
    }

    return render(request, 'lista_produtos.html', context)


def editar_produto(request, pk):
    produto = Estoque.objects.get(id=pk)
    form = EstoqueForm(instance=produto)
    nome_produto = str(produto.produto).title()
    if str(request.method) == 'POST':
        form = EstoqueForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações editadas com sucesso!')
            return redirect('/lista-produtos')
        else:
            messages.error(request, 'Erro ao editar informações')

    context = {
        'form': form,
        'nome_produto': nome_produto,
    }
    return render(request, 'editar_produto.html', context)


def deletar_produto(request, pk):
    estoque = Estoque.objects.get(id=pk)
    nome_produto = str(estoque.produto).title()
    if str(request.method) == 'POST':
        estoque.delete()
        messages.success(request, f'{nome_produto} deletado com sucesso!')
        return redirect('/lista-produtos')

    context = {
        'estoque': estoque,
    }

    return render(request, 'deletar_produto.html', context)


def alterar_quantidade(request, quantidade_subtrair, produto_selecionado):
    produto_venda_get = Estoque.objects.get(produto=produto_selecionado)
    quantidade_produto_get = int(produto_venda_get.quantidade)
    if quantidade_subtrair > quantidade_produto_get:
        messages.error(request, f'Não há estoque para esse produto! Máximo é {quantidade_produto_get}')
    else:
        quantidade_final = quantidade_produto_get - quantidade_subtrair
        quantidade_produto_get = quantidade_final
        return quantidade_produto_get


def cadastrar_venda(request):
    if str(request.method) == 'POST':
        form = VendaForm(request.POST)

        # pegando o produto escolhido
        produto_selecionado = request.POST.get('produto')
        # selecionando o produto no estoque
        produto_selecionado_get = Estoque.objects.get(id=produto_selecionado)

        # pegando a quantidade escolhida
        quantidade_selecionada = int(request.POST.get('quantidade'))
        quantidade_estoque = int(produto_selecionado_get.quantidade)

        # pegando o funcionário escolhido (só um plus para a mensagem bootstrap)
        funcionario_selecionado = request.POST.get('funcionario')
        funcionario = str(Funcionario.objects.get(id=funcionario_selecionado)).title()

        if quantidade_estoque < quantidade_selecionada:
            messages.error(request, f'Quantidade deseja é superior ao estoque. Máximo {quantidade_estoque}')
            form = VendaForm(request.POST)
        else:
            produto_selecionado_get.quantidade = quantidade_estoque - quantidade_selecionada
            if form.is_valid():
                form.save()
                produto_selecionado_get.save()
                messages.success(request, f'Venda cadastrada com sucesso para {funcionario}!')
                return redirect('/cadastrar-venda/')
            else:
                messages.error(request, f'Erro ao cadastrar venda. {messages.error}')
    else:
        form = VendaForm()

    context = {
        'form': form,
    }

    return render(request, 'cadastrar_venda.html', context)


def lista_vendas(request):
    vendas = Venda.objects.all()

    for venda in vendas:
        venda.valor_venda = float(venda.produto.preco) * int(venda.quantidade)
        venda.valor_venda = locale.currency(venda.valor_venda, grouping=True, symbol=True)
        venda.produto.preco = locale.currency(float(venda.produto.preco), grouping=True, symbol=True)

    context = {
        'vendas': vendas,
    }

    return render(request, 'lista_vendas.html', context)


def busca_produto(request):
    if str(request.method) == 'POST':
        searched = request.POST['searched']
        estoque = Estoque.objects.all()

        for prod in estoque:
            prod.produto = prod.produto.lower()
            prod.save()
        estoque_filtrado = Estoque.objects.filter(produto__contains=searched)

        for produto in estoque_filtrado:
            produto.preco = locale.currency(float(produto.preco), grouping=True, symbol=True)
        context = {
            'searched': searched,
            'estoque_filtrado': estoque_filtrado,
        }
        return render(request, 'busca_produto.html', context)
    else:
        context = {
        }
        return render(request, 'busca_produto.html', context)

