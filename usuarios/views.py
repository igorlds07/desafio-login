from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
import re


def cadastro(request):
    
    # Exibe o formulário de cadatro
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        
        # Recupera os dados enviado pelo o formulário.
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        Usermodel = get_user_model()
        
        # Verifica se o email já foi cadastrado.
        if Usermodel.objects.filter(email=email).exists():
            messages.error(request, f'O email "{email}" já está cadastrado !')
            return redirect('cadastro')
        
        # Verifica se os campos do formulário não foram preenchidos.
        if not usuario or not email or not senha or not confirmar_senha:
            messages.error(request, "Preencha todos os campos necessários")
            return redirect('cadastro')
        
        # Condição para verificar se o nome inserido no formulário é composto
        # somente por letras.
        if not re.match(r'^[A-Za-zÀ-ÿ ]+$', usuario):
            messages.error(
                request, "O nome de usuário deve conter apenas letras!")
            return redirect('cadastro')
        
        # Condição para verificar se o formato do email é válido.
        if "@" not in email:
            messages.error(request, "Email inválido !")
            return redirect("cadastro")
        
        # Condição para verificar se as senhas passadas no formulário coicidem.
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coicidem!")
            return redirect('cadastro')
        
        # Validação da complexidade da senha 
        # (mínimo 8 caracteres, 1 letra maiúscula, 1 número e 1 caractere especial)
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])(.{8,})$', senha):
            messages.error(request, "A senha deve ter pelo menos 8 caracteres, 1 letra maiúscula, 1 número e 1 caractere especial.")
            return redirect('cadastro')
        
        # Cria um novo usuário conferme os dados passado no formulário.
        user = Usermodel.objects.create_user(
            username=usuario, email=email, password=senha
            )
        user.save()
        
        # Envia um email de confirmação
        send_mail(
            'Cadastro Realizado com Sucesso',
            'Você foi registrado no desafio técnico da Fidelity.',
            'fidelity@carreiras.com',
            [user.email],
            fail_silently=False,)
        
        # Menssagem de sucesso
        messages.success(request, f"Usuário {usuario} cadastrado com sucesso")
        return redirect('cadastro')
    

def login_view(request):
    
    # Verifica se o o metódo  da requisição é POST.
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Condição para verificar se o os campos do formulário foram
        # preenchidos.
        if not email or not senha:
            messages.error(request, "Preencha os campos necessários!")
            return redirect('login')

        # Tratamento de erro e exceção
        try:
            # Tenta buscar o usuário pelo email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            
            # Se não encontrar, é passado uma mensagem de erro.
            messages.error(request, "E-mail inexistente!")
            return redirect('login')

        # Verifica a senha do usuário
        user = authenticate(request, username=user.username, password=senha)
        if user is not None:
            
            # Se o login for bem-sucedido o usuário é redirecionado.
            login(request, user)
            return redirect('menu')
        else:
            
            # Se a senha estiver errada exibe uma menssagem de erro
            messages.error(request, "Senha inválida!")
            return redirect('login')

    return render(request, 'login.html')


def menu(request):
    
    # Verifica se o usuário esttá autenticado
    if request.user.is_authenticated:
        return render(request, 'menu.html')
    else:
        
        # Se não foi autenticado, retorna a página de login.
        return redirect('login')
