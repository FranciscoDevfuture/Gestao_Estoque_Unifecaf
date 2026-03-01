import tkinter as tk # Biblioteca tkinter
from tkinter import messagebox, ttk
import data_base  # Importa  arquivo database.py
import auth      # Importa arquivo auth.py

class SistemaEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema Unifecaf - Gestão de Estoque - Versao 1.0')
        self.root.geometry('900x600')
        # Armazenam quem está logado e o que ele pode fazer
        self.usuario_atual = None
        self.perfil_atual = None
        self.tela_login() # Começa sempre pela tela de acesso
        
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- TELAS DE ACESSO ---
    def tela_login(self):
        self.limpar_tela()
        tk.Label(self.root, text="Controle de Estoque", font=("Arial", 25, "bold")).pack(pady=50)
        
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Usuário:").pack()
        self.ent_user = tk.Entry(frame, font=("Arial", 12))
        self.ent_user.pack(pady=5)

        tk.Label(frame, text="Senha:").pack()
        self.ent_pass = tk.Entry(frame, show="*", font=("Arial", 12))
        self.ent_pass.pack(pady=5)

        tk.Button(self.root, text="Entrar", command=self.autenticar, 
                  bg="#2196F3", fg="white", width=15, font=("Arial", 10, "bold")).pack(pady=20)

    def autenticar(self):
        user = self.ent_user.get()
        senha = self.ent_pass.get()
        
        # Chamando o módulo de autenticação
        perfil = auth.validar_login(user, senha)
        
        if perfil:
            self.usuario_atual, self.perfil_atual = user, perfil
            self.painel_principal()
        else:
            messagebox.showerror('Erro', 'Dados inválidos!')
            
        #Dashboard principal. Aqui acontece o controle de permissões.
    def painel_principal(self):
        self.limpar_tela()
        
        # Header
        header = tk.Frame(self.root, bg="#eeeeee", height=40)
        header.pack(fill="x", side="top")
        tk.Label(header, text=f"Logado como: {self.usuario_atual} ({self.perfil_atual})", bg="#eeeeee").pack(side="left", padx=10)
        tk.Button(header, text="Sair", command=self.tela_login).pack(side="right", padx=10)

        # Barra de Ações
        frame_acoes = tk.Frame(self.root)
        frame_acoes.pack(pady=20)

        # Botões Comuns
        tk.Button(frame_acoes, text="🔄 Atualizar", command=self.listar_produtos, width=12).grid(row=0, column=0, padx=5)
        tk.Button(frame_acoes, text="📦 Movimentar", command=self.tela_movimentar, bg="#9C27B0", fg="white", width=12).grid(row=0, column=1, padx=5)

        # Botões de Administrador
        if self.perfil_atual == 'Administrador':
            tk.Button(frame_acoes, text="➕ Novo Prod.", command=self.tela_cadastro_produto, bg="#4CAF50", fg="white", width=12).grid(row=0, column=2, padx=5)
            tk.Button(frame_acoes, text="📝 Editar Qtd", command=self.tela_editar_direto, bg="#2196F3", fg="white", width=12).grid(row=0, column=3, padx=5)
            tk.Button(frame_acoes, text="🗑️ Excluir", command=self.deletar_produto, bg="#f44336", fg="white", width=12).grid(row=0, column=4, padx=5)
            tk.Button(frame_acoes, text="👥 Usuários", command=self.tela_gerenciar_usuarios, bg="#607D8B", fg="white", width=12).grid(row=0, column=5, padx=5)

        # Tabela de Produtos
        cols = ('ID', 'Produto', 'Quantidade', 'Mínimo')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.listar_produtos()

    # --- GESTÃO DE PRODUTOS ---
    def listar_produtos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        # Usando a função genérica do database.py
        produtos = data_base.query('SELECT * FROM produtos', fetch=True)
        
        for item in produtos:
            tag = 'baixo' if item[2] < item[3] else 'normal'
            self.tree.insert('', 'end', values=item, tags=(tag,))
        self.tree.tag_configure('baixo', background='#FFCDD2')

    def tela_cadastro_produto(self):
        top = tk.Toplevel(self.root); top.title("Novo Produto"); top.geometry("250x250"); top.grab_set()
        tk.Label(top, text="Nome:").pack(); ent_n = tk.Entry(top); ent_n.pack()
        tk.Label(top, text="Qtd:").pack(); ent_q = tk.Entry(top); ent_q.pack()
        tk.Label(top, text="Mínimo:").pack(); ent_m = tk.Entry(top); ent_m.pack()
        
        def salvar():
            try:
                data_base.query("INSERT INTO produtos (nome, qtd, min) VALUES (?,?,?)", 
                               (ent_n.get(), int(ent_q.get()), int(ent_m.get())))
                top.destroy()
                self.listar_produtos()
            except: 
                messagebox.showerror("Erro", "Verifique os dados!")
        
        tk.Button(top, text="Salvar", command=salvar, bg="green", fg="white").pack(pady=10)

    def tela_editar_direto(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        valores = self.tree.item(selecionado)['values']
        id_p, nome_p = valores[0], valores[1]

        top = tk.Toplevel(self.root); top.geometry("300x200"); top.grab_set()
        tk.Label(top, text=f"Editando: {nome_p}", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(top, text="Nova Quantidade Absoluta:").pack()
        ent_nova_qtd = tk.Entry(top); ent_nova_qtd.pack()

        def salvar_edicao():
            try:
                nova_qtd = int(ent_nova_qtd.get())
                data_base.query("UPDATE produtos SET qtd = ? WHERE id = ?", (nova_qtd, id_p))
                top.destroy()
                self.listar_produtos()
            except: 
                messagebox.showerror("Erro", "Valor inválido!")

        tk.Button(top, text="Salvar", command=salvar_edicao, bg="#2196F3", fg="white").pack(pady=15)

    def tela_movimentar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        valores = self.tree.item(selecionado)['values']
        id_p, nome_p, qtd_p = valores[0], valores[1], valores[2]

        top = tk.Toplevel(self.root); top.title("Entrada/Saída"); top.geometry("300x250"); top.grab_set()
        tk.Label(top, text=f"Produto: {nome_p}", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(top, text="Quantidade da movimentação:").pack()
        ent_qtd = tk.Entry(top); ent_qtd.pack(pady=5)

        def atualizar(op):
            try:
                val = int(ent_qtd.get())
                n_qtd = (qtd_p + val) if op == "add" else (qtd_p - val)
                if n_qtd < 0: 
                    messagebox.showerror("Erro", "Estoque insuficiente!")
                    return
                data_base.query("UPDATE produtos SET qtd = ? WHERE id = ?", (n_qtd, id_p))
                top.destroy()
                self.listar_produtos()
            except: 
                messagebox.showerror("Erro", "Digite um número válido!")

        btn_f = tk.Frame(top); btn_f.pack(pady=20)
        tk.Button(btn_f, text="➕ Entrada", bg="green", fg="white", command=lambda: atualizar("add")).pack(side="left", padx=5)
        tk.Button(btn_f, text="➖ Saída", bg="red", fg="white", command=lambda: atualizar("sub")).pack(side="left", padx=5)

    def deletar_produto(self):
        item = self.tree.selection()
        if not item: return
        if messagebox.askyesno("Confirmar", "Excluir produto definitivamente?"):
            id_p = self.tree.item(item)['values'][0]
            data_base.query("DELETE FROM produtos WHERE id=?", (id_p,))
            self.listar_produtos()

    def tela_gerenciar_usuarios(self):
        top = tk.Toplevel(self.root)
        top.title("Gerenciar Usuários")
        top.geometry("500x450")
        top.grab_set()

        tk.Label(top, text="Usuários do Sistema", font=("Arial", 12, "bold")).pack(pady=10)

        cols = ('ID', 'Login', 'Perfil')
        tree_users = ttk.Treeview(top, columns=cols, show='headings', height=10)
        for col in cols:
            tree_users.heading(col, text=col)
            tree_users.column(col, anchor="center")
        tree_users.pack(fill="both", expand=True, padx=10)

        def carregar_usuarios():
            for i in tree_users.get_children(): tree_users.delete(i)
            usuarios = data_base.query('SELECT id, login, perfil FROM usuarios', fetch=True)
            for user in usuarios:
                tree_users.insert('', 'end', values=user)

        def deletar_usuario():
            selecionado = tree_users.selection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um usuário!")
                return
            
            id_u, login_u = tree_users.item(selecionado)['values'][0], tree_users.item(selecionado)['values'][1]

            if login_u == self.usuario_atual:
                messagebox.showerror("Erro", "Você não pode excluir sua própria conta logada!")
                return

            if messagebox.askyesno("Confirmar", f"Excluir usuário '{login_u}'?"):
                data_base.query("DELETE FROM usuarios WHERE id=?", (id_u,))
                carregar_usuarios()

        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="➕ Novo Usuário", command=lambda: self.tela_cadastro_usuario(carregar_usuarios), 
                  bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Excluir", command=deletar_usuario, bg="#f44336", fg="white", width=15).pack(side="left", padx=5)

        carregar_usuarios()

    def tela_cadastro_usuario(self, callback_atualizacao=None):
        top = tk.Toplevel(self.root); top.title("Cadastrar Usuário"); top.geometry("300x320"); top.grab_set()
        
        tk.Label(top, text="Login:").pack(pady=5)
        ent_u = tk.Entry(top); ent_u.pack()
        
        tk.Label(top, text="Senha:").pack(pady=5)
        ent_s = tk.Entry(top, show="*"); ent_s.pack()
        
        tk.Label(top, text="Perfil:").pack(pady=5)
        cb = ttk.Combobox(top, values=['Administrador', 'Comum'], state="readonly")
        cb.set('Comum'); cb.pack()
        
        def salvar():
            u, s, p = ent_u.get().strip(), ent_s.get().strip(), cb.get()
            if not u or not s:
                messagebox.showerror("Erro", "Preencha tudo!"); return
            try:
                data_base.query("INSERT INTO usuarios (login, senha, perfil) VALUES (?,?,?)", (u, s, p))
                messagebox.showinfo("Sucesso", "Usuário cadastrado!")
                if callback_atualizacao: callback_atualizacao()
                top.destroy()
            except: 
                messagebox.showerror("Erro", "Login já existe!")

        tk.Button(top, text="Salvar", command=salvar, bg="#2196F3", fg="white", width=15).pack(pady=20)
# Bloco de inicialização do programa
if __name__ == "__main__":
    data_base.iniciar_bd()
    root = tk.Tk()
    app = SistemaEstoque(root)
    root.mainloop()