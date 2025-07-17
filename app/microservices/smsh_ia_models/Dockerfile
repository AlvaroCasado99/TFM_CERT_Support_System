FROM python:3.13-slim

# Ports to expose
EXPOSE 8000
EXPOSE 2222

# Crear un directorio de trabajo
WORKDIR /app

# Establecer el pythonpath
ENV PYTHONPATH=/app

# Copiar archivos necesarios
COPY ./microservices/smsh_ia_models/start.sh /app/
COPY ./microservices/smsh_ia_models/requirements.txt /app/
COPY ./microservices/smsh_ia_models/ia_service.py /app/
COPY ./microservices/smsh_ia_models/bert_classifier /app/bert_classifier

# Dependencies
RUN apt-get update && apt-get install -y \
	openssh-server \
	python3 \
	python3-pip \
	python3-venv \
	sudo \
	libssl-dev \
	libffi-dev \
	build-essential \
	cmake \
	pkg-config \
	libpython3-dev \
	libgl1 \
	libglib2.0-0  && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

# Directorio para SSHD
RUN mkdir -p /run/sshd

# Creo usuario sin privilegios
RUN useradd -m -s /bin/bash lucia &&  echo "lucia:lucia" | chpasswd

# Hardening de SSH
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config && \
	sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
	sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
	sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config

# Configuración para la API del microservicio
RUN python3 -m venv /venv && \
	/venv/bin/pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
	/venv/bin/pip3 install -r requirements.txt

# Descargar modelo spacy
RUN /venv/bin/python3 -m spacy download en_core_web_sm

# Elimino la cache para alivianar la imagen
RUN rm -rf /root/.cache/pip

# Doy permisos de ejecucion al start
RUN chmod +x start.sh

CMD ["./start.sh"]
