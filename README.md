# Sistema de Comunicación Cliente-Proxy-Servidor con Docker

Sistema de red distribuido que implementa un modelo de comunicación de tres capas utilizando sockets TCP/UDP en Python y Docker. El sistema permite la comunicación entre un cliente y un servidor a través de un proxy intermediario que aplica filtros de seguridad y control de tráfico, mientras una terminal centralizada monitorea todas las actividades en tiempo real.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionamiento Detallado](#funcionamiento-detallado)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Modelo OSI](#modelo-osi)
- [Contribuciones](#contribuciones)

## 🎯 Descripción General

Este proyecto implementa un sistema de comunicación en red que simula un entorno empresarial real donde los mensajes del cliente pasan por un sistema de proxy para filtrado de contenido y control de seguridad antes de llegar al servidor. Todo el tráfico de red es monitoreado por una terminal centralizada que registra cada operación.

### Flujo de Comunicación

```
Cliente → Proxy → Servidor
   ↓        ↓        ↓
   └────→ Terminal ←┘
```

**Proceso paso a paso:**
1. El **Cliente** envía un mensaje al **Proxy** (no directamente al servidor)
2. El **Proxy** filtra el mensaje aplicando:
   - Filtro de palabras prohibidas
   - Firewall de control de puertos
3. Si el mensaje pasa los filtros, el **Proxy** lo reenvía al **Servidor**
4. El **Servidor** procesa el mensaje y envía una confirmación al **Proxy**
5. El **Proxy** retorna la confirmación al **Cliente**
6. En cada paso, todos los componentes envían logs a la **Terminal** para monitoreo en tiempo real

## 🏗️ Arquitectura del Sistema

### Componentes

| Componente | IP | Puerto | Protocolo | Función |
|------------|----------|--------|-----------|---------|
| **Terminal** | 172.17.0.2 | 5001 | UDP | Monitoreo centralizado de eventos |
| **Servidor** | 172.17.0.3 | 5000 | TCP | Procesa mensajes y envía confirmaciones |
| **Proxy** | 172.17.0.5 | 4000 | TCP | Filtra contenido y controla acceso |
| **Cliente** | Variable | 5000 | TCP | Envía mensajes al sistema |

### Diagrama de Red

```
┌──────────────┐
│   Terminal   │ ← Recibe logs UDP de todos los componentes
│  172.17.0.2  │
│   Puerto 5001│
└──────────────┘
       ↑
       │ (UDP logs)
       │
┌──────┴───────────────────┬─────────────────────┐
│                          │                     │
┌──────────────┐  TCP   ┌──────────────┐  TCP  ┌──────────────┐
│   Cliente    │───────→│    Proxy     │──────→│   Servidor   │
│  Variable IP │        │ 172.17.0.5   │       │ 172.17.0.3   │
│  Puerto 5000 │←───────│ Puerto 4000  │←──────│ Puerto 5000  │
└──────────────┘        └──────────────┘       └──────────────┘
```

## ✨ Características

### 🔒 Seguridad
- **Filtro de contenido**: Bloquea mensajes que contienen palabras prohibidas
- **Firewall de puertos**: El servidor rechaza conexiones desde puertos específicos (puerto 6000 bloqueado)
- **Control de acceso**: Validación de conexiones antes de permitir comunicación

### 🔍 Monitoreo
- **Terminal centralizada**: Recibe y muestra todos los eventos del sistema en tiempo real
- **Seguimiento de mensajes**: Cada mensaje es rastreado a través de todo su recorrido
- **Identificación de clientes**: Cada cliente se identifica con nombre y dirección MAC

### 🌐 Red
- **Comunicación TCP**: Conexiones confiables entre Cliente-Proxy-Servidor
- **Logging UDP**: Envío rápido de mensajes de monitoreo a la Terminal
- **Direcciones MAC**: Identificación única de cada componente en la red

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Socket Programming**: Biblioteca estándar de Python para comunicación en red
- **Docker**: Contenedorización de cada componente del sistema
- **TCP/IP**: Protocolo de comunicación principal
- **UDP**: Protocolo para mensajes de logging
- **UUID**: Identificación de dispositivos mediante direcciones MAC

## 📦 Requisitos Previos

- Docker instalado en tu sistema
- Docker Compose (opcional, para despliegue simplificado)
- Python 3.x (si se ejecuta localmente sin Docker)
- Conocimientos básicos de redes y contenedores

## 🚀 Instalación

### Opción 1: Con Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-cliente-proxy-servidor.git
cd sistema-cliente-proxy-servidor
```

2. Construye las imágenes Docker para cada componente:
```bash
# Terminal
docker build -t red-terminal ./terminal

# Servidor
docker build -t red-servidor ./servidor

# Proxy
docker build -t red-proxy ./proxy

# Cliente
docker build -t red-cliente ./cliente
```

3. Crea una red Docker personalizada:
```bash
docker network create --subnet=172.17.0.0/16 red-proyecto
```

### Opción 2: Ejecución Local (Sin Docker)

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-cliente-proxy-servidor.git
cd sistema-cliente-proxy-servidor
```

2. Asegúrate de tener Python 3.x instalado:
```bash
python3 --version
```

## 💻 Uso

### Con Docker

**Importante**: Los componentes deben iniciarse en el siguiente orden:

1. **Inicia la Terminal** (debe estar lista para recibir logs):
```bash
docker run --name terminal --network red-proyecto --ip 172.17.0.2 -it red-terminal
```

2. **Inicia el Servidor** (en una nueva terminal):
```bash
docker run --name servidor --network red-proyecto --ip 172.17.0.3 -it red-servidor
```

3. **Inicia el Proxy** (en una nueva terminal):
```bash
docker run --name proxy --network red-proyecto --ip 172.17.0.5 -it red-proxy
```

4. **Inicia el Cliente** (en una nueva terminal):
```bash
docker run --name cliente --network red-proyecto -it red-cliente
```

### Sin Docker (Local)

Ejecuta cada componente en terminales separadas:

```bash
# Terminal 1: Terminal
cd terminal
python3 terminal.py

# Terminal 2: Servidor
cd servidor
python3 servidor.py

# Terminal 3: Proxy
cd proxy
python3 proxy.py

# Terminal 4: Cliente
cd cliente
python3 cliente.py 172.17.0.5  # IP del proxy
```

### Interacción con el Sistema

1. Al iniciar el cliente, se te pedirá ingresar tu nombre
2. Una vez conectado, puedes enviar mensajes al servidor
3. Escribe tus mensajes y presiona Enter
4. Verás las confirmaciones del servidor
5. Escribe `exit` para cerrar la conexión

**Ejemplo de interacción:**
```
Ingresa tu nombre: Juan
Conectado al proxy 172.17.0.5:4000. Escribe 'exit' para salir.
Mensaje a enviar: Hola servidor
-> Confirmación del servidor: Mensaje recibido: Hola servidor
Mensaje a enviar: exit
```

## 📁 Estructura del Proyecto

```
.
├── README.md                    # Este archivo
├── cliente/
│   └── cliente.py              # Código del cliente
├── proxy/
│   └── proxy.py                # Código del proxy con filtros
├── servidor/
│   └── servidor.py             # Código del servidor
├── terminal/
│   └── terminal.py             # Terminal de monitoreo
└── documentos/
    ├── explicacion_cliente.txt  # Documentación técnica del cliente
    ├── explicacion_proxy.txt    # Documentación técnica del proxy
    ├── explicacion_servidor.txt # Documentación técnica del servidor
    ├── explicacion_terminal.txt # Documentación técnica de la terminal
    ├── modeloOSI.txt           # Relación con el modelo OSI
    ├── cliente.jpg             # Captura de pantalla del cliente
    ├── proxy.jpg               # Captura de pantalla del proxy
    ├── servidor.jpg            # Captura de pantalla del servidor
    └── terminal.jpg            # Captura de pantalla de la terminal
```

## 🔧 Funcionamiento Detallado

### Cliente (`cliente.py`)

- Se conecta al proxy usando TCP en el puerto 4000
- Utiliza un puerto específico (5000) para la conexión saliente
- Identifica la máquina mediante su dirección MAC
- Envía el nombre del usuario al proxy
- Transmite mensajes al proxy
- Recibe confirmaciones del servidor a través del proxy
- Envía logs a la Terminal mediante UDP

**Características especiales:**
- Manejo de rechazos de conexión (puerto bloqueado)
- Notificación a la terminal en caso de errores
- Cierre controlado de conexiones

### Proxy (`proxy.py`)

Actúa como intermediario con funciones de seguridad:

**Filtros implementados:**
1. **Filtro de palabras prohibidas**: Bloquea mensajes que contienen "mala palabra"
2. **Control de flujo**: Gestiona la comunicación bidireccional entre cliente y servidor

**Proceso:**
1. Escucha conexiones de clientes en el puerto 4000
2. Al recibir un cliente, establece conexión con el servidor
3. Filtra cada mensaje recibido del cliente
4. Si el mensaje pasa los filtros, lo reenvía al servidor
5. Recibe la confirmación del servidor y la retorna al cliente
6. Registra todas las operaciones en la Terminal

### Servidor (`servidor.py`)

Componente final que procesa los mensajes:

**Funcionalidades:**
- Escucha en el puerto 5000 para conexiones TCP
- **Firewall de puertos**: Rechaza conexiones desde el puerto 6000
- Recibe mensajes filtrados por el proxy
- Genera confirmaciones de recepción
- Envía logs detallados a la Terminal

**Validaciones:**
- Verifica el puerto de origen de cada conexión
- Identifica clientes por nombre e IP
- Maneja múltiples conexiones secuenciales

### Terminal (`terminal.py`)

Centro de monitoreo del sistema:

- Utiliza UDP para recibir mensajes de todos los componentes
- Escucha en el puerto 5001
- Muestra en tiempo real:
  - Conexiones establecidas
  - Mensajes enviados y recibidos
  - Acciones del proxy (filtrado, reenvío)
  - Respuestas del servidor
  - Errores y rechazos

**Ventaja del protocolo UDP:**
- No requiere establecer conexiones
- Los componentes pueden enviar logs sin esperar respuesta
- Minimiza la latencia del monitoreo

## 📸 Capturas de Pantalla

### Cliente
![Cliente en ejecución](documentos/cliente.jpg)
*Interfaz del cliente enviando mensajes al proxy*

### Proxy
![Proxy filtrando mensajes](documentos/proxy.jpg)
*Proxy aplicando filtros y reenviando mensajes al servidor*

### Servidor
![Servidor procesando mensajes](documentos/servidor.jpg)
*Servidor recibiendo y confirmando mensajes*

### Terminal
![Terminal monitoreando el sistema](documentos/terminal.jpg)
*Terminal mostrando todos los eventos del sistema en tiempo real*

## 🌐 Modelo OSI

Este proyecto implementa varias capas del modelo OSI:

### Capa 1: Física
- Transmisión de bits a través de Ethernet o Wi-Fi
- Manejada por el hardware de red (tarjetas de red, switches)

### Capa 2: Enlace de Datos
- Direcciones MAC únicas para cada componente
- Detección y corrección de errores en la transmisión
- Los switches dirigen los paquetes usando direcciones MAC

### Capa 3: Red
- Direccionamiento IP:
  - Terminal: `172.17.0.2`
  - Servidor: `172.17.0.3`
  - Proxy: `172.17.0.5`
- Enrutamiento de paquetes entre diferentes IPs
- Soporte para subredes mediante Docker Network

### Capa 4: Transporte
- **TCP**: Conexiones confiables entre Cliente-Proxy-Servidor
  - Garantiza entrega de mensajes
  - Mantiene el orden de los paquetes
  - Control de flujo y congestión
- **UDP**: Logs a la Terminal
  - Transmisión rápida sin confirmación
  - Sin garantía de entrega (aceptable para logs)

### Capa 7: Aplicación
- Protocolos personalizados para la comunicación
- Formato de mensajes específico del sistema
- Lógica de negocio (filtrado, autenticación, confirmaciones)

**Documentación completa:** Ver [documentos/modeloOSI.txt](documentos/modeloOSI.txt)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado como proyecto educativo para demostrar conceptos de:
- Programación de sockets en Python
- Arquitectura de redes
- Contenedorización con Docker
- Modelo OSI
- Sistemas distribuidos

---

**Nota**: Este es un proyecto educativo diseñado para ilustrar conceptos de redes y comunicación. No está diseñado para entornos de producción sin mejoras adicionales de seguridad y escalabilidad.
