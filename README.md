

---

# 📦 Sistema de Controle de Estoque - UniFECAF

Este projeto consiste em uma aplicação desktop para **Gestão de Inventário**, desenvolvida como parte integrante do desafio acadêmico da **UniFECAF**. O sistema foca em segurança, integridade de dados e usabilidade, utilizando níveis de acesso distintos para Administradores e Usuários Comuns.

## 🚀 Funcionalidades

O sistema foi projetado para cobrir o ciclo básico de gestão de mercadorias com as seguintes travas de negócio:

* **Autenticação Segura**: Sistema de login com diferenciação de perfis (ADM e Comum).
* **Gestão de Usuários (Exclusivo ADM)**: Criação de novas contas com definição de hierarquia.
* **Controle de Produtos**: Cadastro de itens com definição de estoque mínimo para alertas.
* **Alertas Visuais**: Destaque automático (cor vermelha) na lista para produtos com quantidade abaixo do nível mínimo definido.
* **Validação de Dados**: Tratamento de exceções para impedir a entrada de caracteres de texto em campos numéricos, evitando corrupção do banco de dados.
* **Persistência de Dados**: Armazenamento relacional robusto utilizando SQLite.

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: Python 3.10+
* **Interface Gráfica (GUI)**: Tkinter (Biblioteca padrão do Python)
* **Banco de Dados**: SQLite3 (Relacional e Serverless)
* **Modelagem**: brModelo (Modelo Entidade-Relacionamento)

## 📊 Modelagem de Dados

A arquitetura do banco de dados segue o modelo relacional unificado, onde o controle de acesso é gerenciado pelo atributo `perfil`.

## 📋 Pré-requisitos e Instalação

Como o sistema utiliza bibliotecas nativas do Python e o SQLite, não é necessário instalar dependências externas pesadas.

1. **Clone o repositório ou baixe o código**:
```bash
git clone https://github.com/seu-usuario/estoque-unifecaf.git

```


2. **Execute a aplicação**:
```bash
python main.py

```



> **Nota**: No primeiro acesso, utilize as credenciais padrão de Administrador:
> * **Usuário**: `admin`
> * **Senha**: `1234`
> 
> 

## 🏗️ Estrutura do Projeto

* `main.py`: Arquivo principal contendo a lógica da interface e regras de negócio.
* `estoque.db`: Arquivo de banco de dados gerado automaticamente na primeira execução.
* `Relatorio_Tecnico.pdf`: Documentação teórica e modelagem brModelo.

## ✒️ Autor

* **Francisco José Dos Santos** - *Desenvolvimento e Documentação* - UniFECAF

---
Print das telas da Aplicação:
<img width="901" height="403" alt="image" src="https://github.com/user-attachments/assets/5e81a897-8df2-4a11-909b-6937f39aad1d" />
<img width="890" height="457" alt="image" src="https://github.com/user-attachments/assets/a39ec8e2-a198-4369-98bd-efd0c8ba38f9" />
<img width="295" height="320" alt="image" src="https://github.com/user-attachments/assets/e1100727-ba7c-4dbb-be55-29781ab6096c" />
<img width="939" height="229" alt="image" src="https://github.com/user-attachments/assets/d1492905-c272-429e-838f-5e1802fd45e9" />
<img width="885" height="270" alt="image" src="https://github.com/user-attachments/assets/ad76d65f-1ec7-430c-99c5-34d5bb5700d5" />
<img width="888" height="290" alt="image" src="https://github.com/user-attachments/assets/9797c39a-43a8-4c20-a8ce-97ddce75a9c7" />
<img width="881" height="329" alt="image" src="https://github.com/user-attachments/assets/a3dfad49-141e-41ee-afcb-997425d68043" />







