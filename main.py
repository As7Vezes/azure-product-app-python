import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import uuid
import pyodbc
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Variáveis de ambiente
blobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Conexão com o banco de dados SQL Server
def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD}"
    )
    return pyodbc.connect(conn_str)

# Upload de imagem no Blob
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + "_" + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

# Inserção no banco
def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = get_connection()
        cursor = conn.cursor()
        insert_sql = """
            INSERT INTO Produtos (name, descricao, preco, imagem_url)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(insert_sql, (product_name, product_description, product_price, image_url))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False

# Listagem do banco
def list_products():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        st.error(f'Erro ao listar produtos: {e}')
        return []

# Exibição dos produtos
def list_products_screen():
    products = list_products()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['name']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R${product['preco']:.2f}")
                if product["imagem_url"]:
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200" alt="Imagem do Produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado.")

# Interface
st.title("Cadastro de Produtos")

product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "png", "jpeg"])

if st.button("Salvar Produto"):
    if product_image is not None and product_name and product_description:
        sucesso = insert_product(product_name, product_price, product_description, product_image)
        if sucesso:
            st.success("Produto salvo com sucesso.")
    else:
        st.warning("Preencha todos os campos e selecione uma imagem.")

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()
