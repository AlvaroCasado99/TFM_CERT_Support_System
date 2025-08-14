#!/bin/bash

# Inicia gunicorn con trabajadores asíncronos "uvicorn"en segundo plano
/venv/bin/gunicorn -w 1 -b 0.0.0.0:8000 main:app \
    -k uvicorn.workers.UvicornWorker \
    --max-requests 400 --max-requests-jitter 200 &

# Inicia sshd en primer plano (mantiene el contenedor vivo)
/usr/sbin/sshd -D

