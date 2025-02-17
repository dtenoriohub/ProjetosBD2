import requests
import pandas as pd
import psycopg2

# convertendo dados para padrao em UTF-8
def to_utf8(value):
    if isinstance(value, str):
        return value.encode("utf-8", "ignore").decode("utf-8")
    return value

# Configuração da API
API_KEY = "0f70af974f6e6a66c6559d9fa5d7e6d7"
URL_POPULAR_MOVIES = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=pt-BR&page=1"

# Requisição para filmes populares
response = requests.get(URL_POPULAR_MOVIES)
data = response.json()

if "results" in data:
    df = pd.DataFrame(data["results"])

    # Mostrar os dados antes do tratamento
    print("Antes do tratamento:")
    print(df.head())

    # Colunas que não estao no endpoint e precisam ser buscadas separadamente
    df["budget"] = None
    df["revenue"] = None
    df["tagline"] = None
    df["homepage"] = None

    # Buscar detalhes de cada filme individualmente
    for index, row in df.iterrows():
        movie_id = row["id"]
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=pt-BR"
        movie_response = requests.get(movie_url)
        movie_data = movie_response.json()

        df.at[index, "budget"] = movie_data.get("budget")
        df.at[index, "revenue"] = movie_data.get("revenue")
        df.at[index, "tagline"] = movie_data.get("tagline", "Sem slogan")
        df.at[index, "homepage"] = movie_data.get("homepage", "Sem site oficial")

    # Substituindo valores sem tratamento com valores específicos
    df["budget"] = df["budget"].fillna("nao disponivel")  # Substitui valores nulos em 'budget' por "nao disponivel"
    df["revenue"] = df["revenue"].fillna(0)  # Substitui valores nulos em 'revenue' por 0

    # Substitui campos vazios em 'tagline' por "Sem slogan"
    df["tagline"] = df["tagline"].apply(lambda x: "Sem slogan" if x == "" else x)

    # Substitui campos vazios em 'homepage' por "Sem site oficial"
    df["homepage"] = df["homepage"].apply(lambda x: "Sem site oficial" if x == "" else x)

    # Se o campo for nulo, manter nulo; caso contrário, substitui valores vazios
    df["genres"] = df["genre_ids"].apply(lambda x: ", ".join(map(str, x)) if isinstance(x, list) and x else "Desconhecido")

    # Garantir que os textos estão em UTF-8
    df["title"] = df["title"].apply(to_utf8)
    df["tagline"] = df["tagline"].apply(to_utf8)
    df["homepage"] = df["homepage"].apply(to_utf8)
    df["genres"] = df["genres"].apply(to_utf8)

    # Mostrar os dados depois do tratamento
    print("\nDepois do tratamento:")
    print(df.head())

    # Contagem de valores nulos por coluna
    nulos_por_coluna = df.isnull().sum()
    nulos_totais = nulos_por_coluna.sum()

    # Filtrar e exibir apenas as colunas que possuem valores nulos
    colunas_com_nulos = df.columns[df.isnull().any()]

    print("\n📌 Colunas com valores nulos:")
    print(colunas_com_nulos.tolist())

    # Filtrar colunas que possuem valores nulos
    colunas_com_nulos = nulos_por_coluna[nulos_por_coluna > 0]

    # Exibir contagem de valores nulos
    print("\n📌 Contagem de valores nulos por coluna:")
    print(colunas_com_nulos)

    print(f"\n🔴 Total de valores nulos encontrados: {nulos_totais}")

    # Salvar os arquivos CSV
    df.to_csv("filmes_tratados.csv", index=False, encoding="utf-8-sig")
    print("\n✅ Arquivo 'filmes_tratados.csv' salvo com sucesso!")

    # Conectar ao banco de dados PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname="Movie_db", 
            user="postgres", 
            password="dtenorio2012", 
            host="localhost", 
            port="5432"
        )
        cursor = conn.cursor()

        # Criar tabela no PostgreSQL
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INT PRIMARY KEY,
            title TEXT,
            budget INT,
            revenue INT,
            tagline TEXT,
            homepage TEXT,
            genres TEXT
        );
        """)

        # Inserir ou atualizar os dados no PostgreSQL (UPSERT)
        for index, row in df.iterrows():
            cursor.execute("""
            INSERT INTO filmes (id, title, budget, revenue, tagline, homepage, genres)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET title = EXCLUDED.title,
                budget = EXCLUDED.budget,
                revenue = EXCLUDED.revenue,
                tagline = EXCLUDED.tagline,
                homepage = EXCLUDED.homepage,
                genres = EXCLUDED.genres;
            """, (row["id"], row["title"], row["budget"], row["revenue"], row["tagline"], row["homepage"], row["genres"]))

        # Commit e fechar a conexão
        conn.commit()
        cursor.close()
        conn.close()

        print("\n✅ Dados inseridos ou atualizados no banco de dados PostgreSQL com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")

else:
    print("Nenhum dado encontrado.")
