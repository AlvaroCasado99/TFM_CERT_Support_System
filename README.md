# TFM_CERT_Support_System

# Para lanzar la base de datos mongo
1. Ir a *app/*
2. Levantar el contenedor: *docker compose up -d* 

# Para lanzar la API en local con UVICORN:
1. Ir a la carpeta raíz
2. Ejecutar el comando: *python3 main.py*

o también:
1. Ir a la carpeta raíz
2. Lanzar el comando:  *uvicorn app.api.main:app --reload*
    **app.api.main** -> Es la ruta al MAIN de la API
    **:app** -> Es el nombre de la instancia de FastAPI en el main.py
    **--reload** -> Permite que se recargue el servidor cuando detecte cambios en el código fuente

# ¿Cómo funciona?
Arquitectura:
1. API principal (Host)
2. Base de datos Mongo (Docker)
3. Nginx (Host)
4. Microservicio 1: Smishing Type (Docker)
5. Microservicio 2: NER Detection (Docker)
6. Microservicio 3: Deteccion de URL, Mail, Phone... (Docker)
7. Microservicio 4: Obtención de código HTML (Docker)
8. Microservicio 5: Función de similitud de campañas (Docker)

## 🔐 Simular TLS

En este proyecto se incluye una simulación de **CA (Certificate Authority)** y **Servidor** para configurar HTTPS en Nginx con certificados firmados por una CA propia.  

### Pasos

1. **Crear directorios**
   ```bash
   cd app/nginx
   mkdir -p ssl CA
   ```

2. **Generar la clave privada de la CA**
   ```bash
   cd CA
   openssl genrsa -des3 -out CA.key 2048
   ```
   > Se pedirá una contraseña. Recuerda guardarla.

3. **Crear el certificado de la CA**
   ```bash
   openssl req -x509 -new -nodes -key CA.key -sha256 -days 1825 -out CA.crt
   ```
   > Pulsa Enter en todos los campos salvo en **Common Name**, donde puedes escribir por ejemplo `autofirmado`.

4. **Generar la clave privada del servidor (sin passphrase)**
   ```bash
   cd ../ssl
   openssl genrsa -out server.key 2048
   ```
   🔹 **Opcional**: si quieres que tenga contraseña deberás generar la clave como a continuación. Además, tendrás que modificar el `nginx.conf`, descomentar la línea con `ssl_password_file` y crear un archivo en /ssl llamado passphrases.txt con la contraseña:
   ```bash
   cd ../ssl
   openssl genrsa -des3 -out server.key 2048
   ```

5. **Generar el CSR (Certificate Signing Request) del servidor**
   ```bash
   openssl req -new -key server.key -out server.csr
   ```
   > Igual que antes, solo completa **Common Name** (`autofirmado`, `localhost` o el dominio/IP que vayas a usar).

6. **Crear archivo de configuración para las extensiones (SAN)**  
   Crea `ssl/configFirma.txt` con este contenido:
   ```ini
   authorityKeyIdentifier=keyid,issuer
   basicConstraints=CA:FALSE
   keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
   subjectAltName = @alt_names

   [alt_names]
   DNS.1 = 127.0.0.1
   DNS.2 = localhost
   ```
   🔹 **Opcional**: si quieres acceder desde otra máquina de la red, añade tu IP:
   ```ini
   IP.1 = 192.168.1.XXX
   ```

7. **Firmar el CSR con la CA para generar el certificado del servidor**
   ```bash
   openssl x509 -req -in server.csr \
     -CA ../CA/CA.crt -CAkey ../CA/CA.key -CAcreateserial \
     -out server.crt -days 1825 -sha256 -extfile configFirma.txt
   ```

### Resultado esperado

- En `CA/` tendrás:
  - `CA.key` → clave privada de la CA (**secreta, no compartir**).
  - `CA.crt` → certificado público de la CA (hay que instalarlo en los clientes para que confíen).

- En `ssl/` tendrás:
  - `server.key` → clave privada del servidor (solo la usa Nginx).
  - `server.csr` → petición de certificado (se puede borrar tras generar el .crt).
  - `server.crt` → certificado del servidor, firmado por la CA.
  - `configFirma.txt` → archivo con extensiones y SAN.

### Instalar la CA en los clientes

- **Linux (Debian/Ubuntu)**:
  ```bash
  sudo cp CA/CA.crt /usr/local/share/ca-certificates/CA.crt
  sudo update-ca-certificates
  ```

- **Linux (Fedora/RHEL/CentOS)**:
  ```bash
  sudo cp CA/CA.crt /etc/pki/ca-trust/source/anchors/
  sudo update-ca-trust
  ```

- **Firefox**:
  - Ajustes → Privacidad y seguridad → Certificados → Ver certificados → Autoridades → Importar → selecciona `CA.crt`.
  - Marca “Confiar en esta CA para identificar sitios web”.
  - Alternativa: en `about:config` poner `security.enterprise_roots.enabled = true` para que use el almacén del sistema.

### Verificar

- Comprueba que Nginx arranca:
  ```bash
  sudo nginx -t && sudo systemctl reload nginx
  ```

- Test en consola:
  ```bash
  curl -vk https://localhost
  ```

- Test en navegador:
  - Si `CA.crt` está instalado → verás el candado sin errores.
  - Si no lo está → Firefox/Chrome avisarán de certificado no confiable.
