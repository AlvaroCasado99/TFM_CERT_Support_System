#!/bin/bash

# Inicia gunicorn con trabajadores asíncronos "uvicorn"en segundo plano
/venv/bin/python3 bot_telegram.py &

# Inicia sshd en primer plano (mantiene el contenedor vivo)
/usr/sbin/sshd -D

