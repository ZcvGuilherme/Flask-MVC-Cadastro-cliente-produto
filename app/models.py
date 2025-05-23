import sqlite3

def conectar():
    conexao = sqlite3.connect("cadastro_clientes.db")
    return conexao


def criar_tabela_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome TEXT NOT NULL, 
                idade INTEGER NOT NULL,
                telefone TEXT,
                email TEXT,
                sexo TEXT CHECK (sexo IN ('M', 'F'))
        );
        """)
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
def cadastrar_cliente_tabela(nome,idade,telefone,email,sexo):
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute ("""
                           INSERT INTO clientes (nome, idade, telefone,email,sexo)
                           VALUES (?,?,?,?,?)
                           
                        """,(nome,idade,telefone,email,sexo))
        
        conexao.commit()
        cursor.close()
        conexao.close()

def deletar_cliente(id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_clientes_ordenado(campo='id', busca='', ordem=True):
    """busca=''
    Busca clientes no banco de dados filtrando por nome ou e-mail e ordena os resultados.

    Parâmetros:
        campo (str): Campo pelo qual os resultados serão ordenados.
                     Valores válidos: 'id', 'nome', 'idade', 'sexo', 'email'.
        busca (str): Texto usado para filtrar os resultados nos campos 'nome' ou 'email'.
        ordem (bool): True para ordem crescente (ASC), False para decrescente (DESC).

    Retorna:
        list: Lista de objetos tipo Row (acessível com cliente.id, cliente.nome, etc.)
    """
    conexao = conectar()
    conexao.row_factory = sqlite3.Row 
    cursor = conexao.cursor()
    direcao = 'ASC' if ordem else 'DESC'
    
    campos_validos = ['id', 'nome', 'idade', 'sexo', 'email']
    if campo not in campos_validos:
        campo = 'id'

    query = f"""
        SELECT * FROM clientes 
        WHERE id LIKE ? OR nome LIKE ? OR email LIKE ? 
        ORDER BY {campo} {direcao}
    """
    
    cursor.execute(query, (f'%{busca}%', f'%{busca}%', f'%{busca}%'))
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes

def editar_cliente(id, nome=None, idade=None, telefone=None, email=None, sexo=None):
    conexao = conectar()
    cursor = conexao.cursor()

    campos = []
    valores = []

    if nome:
        campos.append("nome = ?")
        valores.append(nome)

    if idade:
        campos.append("idade = ?")
        valores.append(idade)
    
    if telefone:
        campos.append("telefone = ?")
        valores.append(telefone)

    if email:
        campos.append("email = ?")
        valores.append(email)
    
    if sexo:
        campos.append("sexo = ?")
        valores.append(sexo)
    
    valores.append(id)

    sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id = ?"
    cursor.execute(sql, valores)

    conexao.commit()
    cursor.close()
    conexao.close()

######################################################################################

def conectar_produtos():
    return sqlite3.connect("banco_produtos.db")

def criar_tabela_produtos():
    conexao = conectar_produtos()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            quantidade INTEGER NOT NULL
        );
    """)
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_produtos_ordenado(campo='id', busca='', ordem=True):
    conexao = conectar_produtos()
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    direcao = 'ASC' if ordem else 'DESC'

    campos_validos = ['id', 'nome', 'valor', 'quantidade']
    if campo not in campos_validos:
        campo = 'id'

    # Adicionando os parâmetros de busca de forma segura nas colunas corretas
    query = f"SELECT * FROM produtos WHERE nome LIKE ? OR quantidade LIKE ? OR id LIKE ? ORDER BY {campo} {direcao};"
    busca_param = f"%{busca}%"  # Adiciona os `%` para busca parcial
    cursor.execute(query, (busca_param, busca_param, busca_param))  # Passando os parâmetros de forma segura
    produtos = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    return produtos

def cadastrar_produto(nome, valor, quantidade):
    conexao = conectar_produtos()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, valor, quantidade)
        VALUES (?, ?, ?);
    """, (nome, valor, quantidade))
    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_produto(id):
    conexao = conectar_produtos()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    
def editar_produto(id, nome=None, valor=None, quantidade=None):
    conexao = conectar()
    cursor = conexao.cursor()

    campos = []
    valores = []

    if nome:
        campos.append("nome = ?")
        valores.append(nome)
     
    if valor:
        campos.append("valor = ?")
        valores.append(valor)
    
    if quantidade:
        campos.append("quantidade = ?")
        valores.append(quantidade)
    
    valores.append(id)

    sql = f"UPDATE produtos SET {', '.join(campos)} WHERE id = ?"
    cursor.execute(sql, valores)

    conexao.commit()
    cursor.close()
    conexao.close()