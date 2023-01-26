from django import forms
from .models import Funcionario, Venda, Estoque


class FuncionarioForm(forms.ModelForm):
    required_css_class = 'required'  # mostra os campos obrigatórios

    class Meta:
        model = Funcionario
        fields = ['nome', 'sobrenome', 'email', 'cpf', 'remuneracao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'remuneracao': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }


class EstoqueForm(forms.ModelForm):
    required_css_class = 'required'  # mostra os campos obrigatórios

    class Meta:
        model = Estoque
        fields = ['produto', 'preco', 'quantidade', 'descricao', 'imagem_produto']
        widgets = {
            'produto': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', "cols": "20", "rows": "5"})
        }


class VendaForm(forms.ModelForm):
    required_css_class = 'required'  # mostra os campos obrigatórios

    class Meta:
        model = Venda
        fields = ['funcionario', 'produto', 'quantidade', 'descricao']
        widgets = {
            'funcionario': forms.Select(attrs={'class': 'form-control', 'placeholder': '- Selecione -'}),
            'produto': forms.Select(attrs={'class': 'form-control', 'placeholder': '- Selecione -'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BuscaProdutoForm(forms.Form):
    required_css_class = 'required'  # mostra os campos obrigatórios

    nome_produto = forms.TextInput()

    class Meta:
        widgets = {
            'nome_produto': forms.TextInput(attrs={'class': 'form-control'}),
        }
