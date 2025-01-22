# Use a imagem base do Python
FROM python:3.8-slim

# Instale dependências do sistema necessárias (se precisar, ajuste conforme o projeto)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copie e instale as dependências do Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie apenas os arquivos necessários do projeto
COPY . .

# Exponha a porta que o Flask usará (opcional)
EXPOSE 5000

# Defina o comando padrão para iniciar a aplicação
CMD ["python", "imageProcAPI.py"]
