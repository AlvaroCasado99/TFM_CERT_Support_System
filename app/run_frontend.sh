#!/bin/bash

# Activar el entorno conda
conda activate test_env

# Establecer PYTHONPATH y lanzar Streamlit
PYTHONPATH=. streamlit run web/app.py
