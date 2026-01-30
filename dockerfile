# Use a versão leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para o container
COPY . .

# Executa o setup inicial para garantir que as pastas existam
RUN python init_setup.py

# Comando para rodar os testes antes de permitir o uso (Opcional, mas Senior)
# RUN pytest

# Define o comando de execução principal
CMD ["python", "runner.py"]
