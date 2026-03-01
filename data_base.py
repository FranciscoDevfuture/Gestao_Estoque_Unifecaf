import sqlite3

# Estabelece a conexão com o arquivo do banco de dados
def conectar():
    # Se o arquivo 'estoque.db' não existir, ele será criado automaticamente
    return sqlite3.connect('estoque.db')

def iniciar_bd():
    """Cria as tabelas iniciais e o usuário administrador padrão."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Cria a tabela de usuários caso ela ainda não exista
    # id: Chave primária autoincrementada
    # login: Único (não permite dois usuários com o mesmo nome)
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                    (id INTEGER PRIMARY KEY, login TEXT UNIQUE, senha TEXT, perfil TEXT)''')
    
    # Cria a tabela de produtos para o controle de estoque
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                    (id INTEGER PRIMARY KEY, nome TEXT, qtd INTEGER, min INTEGER)''')
    
    try:
        # Tenta inserir um usuário administrador padrão para o primeiro acesso
        cursor.execute('INSERT INTO usuarios (login, senha, perfil) VALUES (?, ?, ?)', 
                        ('admin', '1234', 'Administrador'))
        conn.commit() # Salva a inserção no banco
    except sqlite3.IntegrityError:
        # Se o 'admin' já existir, o SQLite lançará um erro de integridade (UNIQUE)
        # O 'pass' ignora o erro para não interromper a execução
        pass
    conn.close() # Fecha a conexão para liberar recursos

def query(sql, params=(), fetch=False):
    """Função genérica para executar comandos SQL (INSERT, UPDATE, DELETE, SELECT)."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Executa o comando SQL usando placeholders (?) para evitar SQL Injection
    cursor.execute(sql, params)
    
    # Se fetch=True, retorna os resultados (usado em SELECT)
    # Caso contrário, retorna None (usado em INSERT/UPDATE/DELETE)
    res = cursor.fetchall() if fetch else None
    
    conn.commit() # Confirma as alterações
    conn.close()
    return res