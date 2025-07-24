import logging
import os
import sys

def setup_logger(name: str, log_file: str = "app.log", base_path: str = "./app/logs") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Evita configurar múltiples veces

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s: %(message)s")

    # Handler para consola (stdout -> útil en Docker)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Handler para archivo
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler(f"{base_path}/{log_file}")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
