#!/bin/bash

# Uso: ./cleanup.sh <nombre1> <nombre2> ...
if [ $# -lt 1 ]; then
  echo "Debe pasar al menos un nombre de contenedor o imagen como parámetro"
  exit 1
fi

echo "Deteniendo contenedores con docker-compose..."
docker compose down

for CONTAINER_NAME in "$@"; do
  echo "Buscando imágenes relacionadas con: $CONTAINER_NAME"

  # Obtener los IDs de las imágenes cuyo nombre coincida con el parámetro
  IMAGE_IDS=$(docker images --format "{{.Repository}} {{.ID}}" | grep "$CONTAINER_NAME" | awk '{print $2}')

  if [ -z "$IMAGE_IDS" ]; then
    echo "No se encontraron imágenes para '$CONTAINER_NAME'"
    continue
  fi

  echo "Imágenes encontradas para '$CONTAINER_NAME': $IMAGE_IDS"

  # Eliminar las imágenes
  for id in $IMAGE_IDS; do
    echo "Eliminando imagen $id..."
    docker rmi -f $id
  done
done

echo "Proceso completado."

