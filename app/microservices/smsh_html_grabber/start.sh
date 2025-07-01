#!/bin/bash

# Inicia gunicorn con trabajadores asíncronos "uvicorn"en segundo plano
/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 html_grabber_service:app \
    -k uvicorn.workers.UvicornWorker \
    --max-requests 400 --max-requests-jitter 200 &

# Inicia sshd en primer plano (mantiene el contenedor vivo)
/usr/sbin/sshd -D

