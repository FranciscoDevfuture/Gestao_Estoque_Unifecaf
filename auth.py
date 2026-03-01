import data_base # Importa o arquivo anterior (onde estão as funções de conexão e query)

# Define a regra de negócio para autenticação de usuários
def validar_login(usuario, senha):
    """
    Verifica se o login e a senha existem no banco.
    Retorna o 'perfil' do usuário se encontrado, ou None se os dados estiverem incorretos.
    """
    
    # Executa a busca no banco de dados
    # O uso de '?' evita ataques de SQL Injection (segurança)
    res = data_base.query(
        'SELECT perfil FROM usuarios WHERE login=? AND senha=?', 
        (usuario, senha), # Parâmetros passados como tupla
        fetch=True        # Ativa o fetch para buscar o resultado da consulta
    )
    
    # Lógica de retorno:
    # Se 'res' tiver dados, acessa a primeira linha [0] e a primeira coluna [0] (o perfil)
    # Se 'res' estiver vazio (usuário/senha errados), retorna None
    return res[0][0] if res else None