# Use a imagem oficial do Python mais leve
FROM python:3.8-slim

# Defina um ambiente não interativo para evitar prompts do apt
ENV DEBIAN_FRONTEND=noninteractive

# Instale dependências essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie e instale apenas as dependências antes para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Defina variáveis de ambiente para produção
ENV FLASK_APP=imageProcAPI.py
ENV FLASK_RUN_HOST=0.0.0.0

# Execute o servidor Flask diretamente para melhor compatibilidade
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]