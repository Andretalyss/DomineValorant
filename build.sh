#!/bin/bash

echo -e "Deletando imagens antigas\n"
sudo docker rm -f valorant_api

echo -e "Buildando nova imagem\n"
sudo docker build -t valorant-api .

echo -e "Deletando recursos não utilizados no docker\n"
sudo docker system prune -f

echo -e "Verificando se postgres está ativo\n"
postgres_status=$(sudo docker ps | grep postgres_db)
if ! echo $postgres_status | grep -q "Up"; then
    # Criando volume para o postgres
    echo -e "Postgres não está ativo, iniciando container\n"
    sudo mkdir -p /tmp/postgres
    sudo docker run -d -e POSTGRES_PASSWORD=pass -p 5432:5432 -v /tmp/postgres:/var/lib/postgresql/data --name postgres_db postgres
fi

echo -e "Iniciando nova imagem -> http://localhost:5000/ \n"
sudo docker run -d -p 5000:5000 --network host --name valorant_api valorant-api:latest

