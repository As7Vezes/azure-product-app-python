# 🛒 Streamlit Product Catalog

Aplicação web simples desenvolvida com **Python + Streamlit**, que permite o **cadastro de produtos com imagem**, armazenando as informações em um banco de dados **SQL Server** e as imagens no **Azure Blob Storage**.

---

## 🚀 Funcionalidades

<details>
<summary>Clique para ver</summary>

- 📦 Cadastro de produtos com:
  - Nome
  - Descrição
  - Preço
  - Imagem
- ☁️ Upload automático da imagem para o Azure Blob Storage
- 🗃️ Armazenamento dos dados em um banco de dados SQL Server
- 🖼️ Listagem dos produtos em formato de cards, com imagem e informações

</details>

---

## 🧪 Tecnologias utilizadas

<details>
<summary>Clique para ver</summary>

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Azure Blob Storage](https://azure.microsoft.com/pt-br/products/storage/blobs/)
- [SQL Server](https://www.microsoft.com/pt-br/sql-server/)
- [pyodbc](https://pypi.org/project/pyodbc/)
- [dotenv](https://pypi.org/project/python-dotenv/)

</details>

---

## 🧰 Pré-requisitos

<details>
<summary>Clique para ver</summary>

- Python 3.9 ou superior
- Conta no Azure com um Blob Storage configurado
- Instância do SQL Server com a tabela `Produtos` criada:

```sql
CREATE TABLE Produtos (
    id INT PRIMARY KEY IDENTITY,
    name VARCHAR(255),
    descricao TEXT,
    preco DECIMAL(10, 2),
    imagem_url TEXT
);


## 🚀 Instalação e execução

<details> <summary>Clique para ver</summary>
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/streamlit-product-catalog.git
cd streamlit-product-catalog
Crie um ambiente virtual e ative:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Crie um arquivo .env com suas credenciais:

env
Copiar
Editar
BLOB_CONNECTION_STRING=...
BLOB_CONTAINER_NAME=...
BLOB_ACCOUNT_NAME=...

SQL_SERVER=...
SQL_DATABASE=...
SQL_USER=...
SQL_PASSWORD=...
Execute a aplicação:

bash
Copiar
Editar
streamlit run app.py
</details>


