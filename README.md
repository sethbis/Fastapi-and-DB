# API RESTful con FastAPI en AWS EC2 y Amazon RDS

API RESTful desarrollada con FastAPI y SQLModel para operaciones CRUD sobre las entidades Usuarios y Libros, persistiendo los datos en una base de datos PostgreSQL alojada en Amazon RDS y desplegada en una instancia AWS EC2.

---

## Estructura del Proyecto

```text
fastapi-aws-rds/
├── app/
│   ├── config.py         # Carga de variables de entorno
│   ├── db.py             # Conexion a base de datos y sesion SQLModel
│   ├── models/
│   │   ├── usuario.py    # Modelo Usuario
│   │   └── libro.py      # Modelo Libro
│   └── routes/
│       ├── usuarios.py   # CRUD /usuarios
│       └── libros.py     # CRUD /libros
├── deploy/
│   ├── fastapi.service   # Servicio systemd para EC2
│   └── ecosystem.config.js # Configuracion PM2 alternativa
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Archivos ignorados por Git
├── main.py               # Punto de entrada FastAPI y endpoint /check-db
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Guia de ejecucion y despliegue
```

---

## 1. Configuracion y Ejecucion Local

### 1.1 Crear y activar entorno virtual

En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.2 Instalar dependencias
```bash
pip install -r requirements.txt
```

### 1.3 Configurar variables de entorno
Copiar el archivo `.env.example` a `.env` y definir los valores de conexion:
```bash
cp .env.example .env
```

Contenido de `.env`:
```env
DB_USER=postgres
DB_PASSWORD=tu_password_rds
DB_HOST=tu-instancia-rds.xxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
```

### 1.4 Ejecutar en local
```bash
uvicorn main:app --reload --port 8000
```
Swagger UI disponible en: `http://127.0.0.1:8000/docs`

---

## 2. Subir el Repositorio a GitHub o GitLab

Ejecutar en la raiz del proyecto:
```bash
git init
git add .
git commit -m "Implementacion API FastAPI con RDS y EC2"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

---

## 3. Configuracion de Amazon RDS (PostgreSQL)

1. Ir a la consola de AWS -> RDS -> Crear base de datos.
2. Metodo: Creacion estandar.
3. Motor: PostgreSQL (version 15 o superior).
4. Plantilla: Capa gratuita (Free Tier).
5. Identificador de base de datos: `fastapi-db`.
6. Usuario maestro: `postgres`.
7. Contrasena: Definir una contrasena segura y guardarla para el archivo `.env`.
8. Clase de instancia: `db.t3.micro` o `db.t4g.micro`.
9. Conectividad:
   - Acceso publico: Opcional (No si solo se conecta la EC2, o Si para pruebas directas).
   - Crear un Security Group para RDS, por ejemplo `rds-sg`.
10. Crear la base de datos y esperar a que el estado sea "Disponible".
11. Copiar el Endpoint generado (Host).

---

## 4. Configuracion de Amazon EC2

1. Ir a AWS -> EC2 -> Lanzar una instancia.
2. Nombre: `fastapi-ec2`.
3. Sistema Operativo: Ubuntu Server 22.04 LTS o 24.04 LTS.
4. Tipo de instancia: `t2.micro` o `t3.micro`.
5. Par de claves (Key pair): Seleccionar o crear clave `.pem`.
6. Security Group de la EC2 (`ec2-sg`):
   - Regla 1: SSH (Puerto 22) -> Origen: Mi IP (o 0.0.0.0/0).
   - Regla 2: TCP personalizada (Puerto 8000) -> Origen: 0.0.0.0/0.
7. Lanzar instancia y copiar su IP publica.

---

## 5. Regla de Comunicacion EC2 -> RDS (Security Groups)

1. Ir al Security Group de la base de datos RDS (`rds-sg`).
2. Editar reglas de entrada (Inbound rules):
   - Tipo: PostgreSQL.
   - Puerto: 5432.
   - Origen: Seleccionar el Security Group de la EC2 (`ec2-sg`) o la IP publica/privada de la EC2.
3. Guardar reglas.

---

## 6. Despliegue en la Instancia EC2

### 6.1 Conectar por SSH a EC2
```bash
ssh -i "tu-llave.pem" ubuntu@<IP_PUBLICA_EC2>
```

### 6.2 Instalar paquetes del sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
```

### 6.3 Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git fastapi-aws-rds
cd fastapi-aws-rds
```

### 6.4 Crear entorno virtual e instalar dependencias
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6.5 Configurar el archivo .env en EC2
```bash
nano .env
```
Pegar las credenciales reales de la base de datos RDS:
```env
DB_USER=postgres
DB_PASSWORD=tu_password_rds
DB_HOST=fastapi-db.xxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
```
Guardar con `Ctrl + O`, `Enter` y salir con `Ctrl + X`.

### 6.6 Opcion A: Mantener activo con systemd (Recomendado)
```bash
sudo cp deploy/fastapi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi
sudo systemctl status fastapi
```

### 6.7 Opcion B: Mantener activo con PM2
```bash
sudo apt install -y nodejs npm
sudo npm install -g pm2
pm2 start "venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000" --name "fastapi-app"
pm2 save
pm2 startup
```

---

## 7. Pruebas y Validacion de la API

Abrir en el navegador:
- Estado general: `http://<IP_PUBLICA_EC2>:8000/`
- Verificacion de conexion a RDS: `http://<IP_PUBLICA_EC2>:8000/check-db`
- Documentacion interactiva Swagger: `http://<IP_PUBLICA_EC2>:8000/docs`

### Endpoints disponibles:

#### Diagnostico:
- `GET /`: Mensaje de estado de la API.
- `GET /check-db`: Prueba ejecucion de `SELECT 1` directo sobre RDS.

#### Entidad Usuarios:
- `POST /usuarios/`: Crear usuario.
- `GET /usuarios/`: Listar todos los usuarios.
- `GET /usuarios/{usuario_id}`: Consultar usuario por ID.
- `PUT /usuarios/{usuario_id}`: Actualizar usuario.
- `DELETE /usuarios/{usuario_id}`: Eliminar usuario.

#### Entidad Libros:
- `POST /libros/`: Crear libro.
- `GET /libros/`: Listar todos los libros.
- `GET /libros/{libro_id}`: Consultar libro por ID.
- `PUT /libros/{libro_id}`: Actualizar libro.
- `DELETE /libros/{libro_id}`: Eliminar libro.

---

## 8. Lista de Evidencias para la Entrega

1. **Instancia EC2:** Captura de pantalla de la consola de AWS EC2 mostrando el estado "En ejecucion" y su IP publica.
2. **Instancia RDS:** Captura de la consola de AWS RDS con estado "Disponible" y el Endpoint visible.
3. **Security Groups:** Captura de las reglas de entrada de EC2 (puerto 8000 abierto) y de RDS (puerto 5432 permitiendo la conexion desde EC2).
4. **Endpoint /docs:** Captura de la documentacion Swagger accesible mediante la IP publica de EC2 (`http://<IP_PUBLICA_EC2>:8000/docs`).
5. **Operaciones CRUD:** Capturas de Swagger ejecutando exitosamente creacion (`POST`) y consulta (`GET`) para usuarios y libros.
6. **Persistencia en RDS:** Captura del endpoint `/check-db` retornando estado conectado y/o consulta desde un cliente SQL (como DBeaver o pgAdmin) confirmando que los registros existen en la base de datos RDS.
