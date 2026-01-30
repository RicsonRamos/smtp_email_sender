# Use a imagem oficial do Python (versão Slim para ser mais leve)
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para algumas libs Python
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de requisitos primeiro (otimiza o cache do Docker)
COPY requirements.txt .

# Instala as bibliotecas do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto para dentro do container
COPY . .

# Cria as pastas necessárias caso não existam
RUN mkdir -p data logs attachments config

# Expõe a porta que o Streamlit usa por padrão
EXPOSE 8501

# Comando para iniciar o app quando o container subir
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]