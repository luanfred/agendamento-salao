
def get_usuario_ativo(request):
    usuario = request.user if request.user.is_authenticated else None
    return {
        'usuario_ativo': usuario
    }