#!/bin/bash

# Script para levantar docker-compose con o sin logs

if [ "$1" == "-logs" ]; then
    echo "Lanzando docker-compose con logs..."
    docker compose up
else
    echo "Lanzando docker-compose en segundo plano..."
    docker compose up -d
fi
