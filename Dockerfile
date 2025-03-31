# Usando a imagem oficial do Python
FROM python:3.11

# Instalando o Dockerize
ENV DOCKERIZE_VERSION v0.9.3

RUN apt-get update \
    && apt-get install -y wget \
    && wget -O - https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz | tar xzf - -C /usr/local/bin \
    && apt-get autoremove -yqq --purge wget && rm -rf /var/lib/apt/lists/*

# Definindo o diretório de trabalho para a pasta "project"
WORKDIR /app/project

# Copiando os arquivos para o contêiner
COPY . /app

# Instalando as dependências do Django
RUN pip install --no-cache-dir -r /app/requirements.txt

# Rodando o comando para aguardar o banco de dados e iniciar o Django
CMD ["dockerize", "-wait", "tcp://db:3306", "-timeout", "30s", "python", "manage.py", "runserver", "0.0.0.0:8000"]
