
def get_usuario_ativo(request):
    user = request.user if request.user.is_authenticated else None
    is_funcionario = user.usuario.funcionario if user and hasattr(user, 'usuario') else False
    print(f"Usuario ativo: {user}, Funcionario: {is_funcionario}")
    return {
        'usuario_ativo': user,
        'is_funcionario': is_funcionario
    }