# Dockerfile otimizado para FastAPI

# Usa a imagem oficial do Python slim para reduzir o tamanho
FROM python:3.8-slim

# Defina um ambiente não interativo para evitar prompts do apt
ENV DEBIAN_FRONTEND=noninteractive

# Instale dependências essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala apenas as dependências antes para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Expõe a porta usada pelo FastAPI
EXPOSE 8011

# Comando para rodar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8011", "--reload"]