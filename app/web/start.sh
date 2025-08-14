#!/bin/bash

# Levantar streamlit
/venv/bin/streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &

# Inicia sshd en primer plano (mantiene el contenedor vivo)
/usr/sbin/sshd -D

