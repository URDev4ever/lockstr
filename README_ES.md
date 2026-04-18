<h1 align="center">🔐 lockstr</h1>
<p align="center">
  🇺🇸 <a href="README.md"><b>English</b></a> |
  🇪🇸 <b>Español</b>
</p>
<h3 align="center">lockstr es una herramienta de cifrado de archivos por línea de comandos, segura y minimalista, construida sobre criptografía simétrica Fernet.
Cifra y descifra archivos y directorios en el lugar, sin exponer nunca la clave de cifrado en pantalla.</h3>

> ⚠️ Sin la clave, los archivos cifrados son **irrecuperables de forma permanente**.

---

## ✨ Características

* 🔒 Cifrado simétrico fuerte (Fernet / AES + HMAC)
* 📁 Cifra **archivos o directorios completos** (recursivo)
* 🧠 El encabezado mágico evita el doble cifrado accidental
* 🧪 Modo dry-run (vista previa sin cambios)
* 📋 Claves de cifrado copiadas al portapapeles (nunca impresas)
* ⌨️ Ingreso seguro de la clave (entrada oculta)
* 🔁 Reemplazo atómico de archivos (sin corrupción parcial)
* 🧰 Multiplataforma (Linux, macOS, Windows)
* 🚫 Sin acceso a red, sin almacenamiento de claves, sin telemetría

---

## 🔐 Descripción general de la criptografía

lockstr utiliza **Fernet** de la librería `cryptography`:

* Cifrado AES-128-CBC
* Autenticación HMAC-SHA256
* Verificación de integridad incorporada
* Detección de manipulación
* Modelo de clave simétrica

La misma clave se usa para cifrar y descifrar los datos.

---

## 📦 Instalación

### 1. Requisitos

* Python **3.6+**
* Paquetes requeridos:

  ```bash
  pip install cryptography pyperclip
  ```

#### Soporte de portapapeles en Linux (recomendado)

```bash
sudo apt install xclip          # X11
sudo apt install wl-clipboard   # Wayland
```

---

### 2. Instalar lockstr

Clona el proyecto con:

```bash
git clone https://github.com/urdev4ever/lockstr.git
cd lockstr
```

Desde el directorio del proyecto:

```bash
python installer.py
```

Esto hará:

* Copiar `lockstr.py` a un directorio apropiado del sistema
* Crear un comando wrapper `lockstr`
* Agregar instrucciones si tu PATH necesita actualizarse

---

## 🚀 Uso

### Sintaxis básica

```bash
lockstr encrypt <ruta>
lockstr decrypt <ruta>
```

Donde `<ruta>` puede ser:

* Un solo archivo
* Un directorio (procesado recursivamente)

---

### 🔒 Cifrar un archivo

```bash
lockstr encrypt secret.txt
```

* Genera una nueva clave de cifrado
* La copia al portapapeles
* Cifra el archivo **en el lugar**

---

### 🔓 Descifrar un archivo

```bash
lockstr decrypt secret.txt
```

* Solicita la clave (entrada oculta)
* Restaura el archivo original

---

### 📁 Cifrar un directorio

```bash
lockstr encrypt ./documents/
```

Todos los archivos dentro del directorio se cifran de forma recursiva.

---

## 🧪 Modo Dry-run (Altamente recomendado)

Previsualiza qué se va a cifrar o descifrar **sin modificar nada**:

```bash
lockstr encrypt ./backup/ --dry-run
```

Esto muestra:

* Árbol de archivos
* Cantidad de archivos afectados
* No se realizan cambios

---

## ⚙️ Opciones de línea de comandos

| Opción                | Descripción                                 |
| --------------------- | ------------------------------------------- |
| `--dry-run`           | Muestra qué se procesaría sin hacer cambios |
| `--confirm`           | Pide confirmación antes de procesar         |
| `--include-hidden`    | Incluye archivos ocultos (`.archivo`)       |
| `--continue-on-error` | Continúa incluso si algunos archivos fallan |
| `-h, --help`          | Muestra el mensaje de ayuda                 |

---

## 🧠 Protección con encabezado mágico

lockstr antepone un **encabezado mágico** a los archivos cifrados:

```
LOCKSTR1\0
```

Esto le permite a lockstr:

* Detectar archivos ya cifrados
* Evitar el doble cifrado
* Rechazar intentos de descifrado sobre archivos sin cifrar

---

## 🔑 Manejo de claves y seguridad

* Las claves **nunca se imprimen**
* Las claves se copian al portapapeles **una sola vez**
* Las claves no se guardan ni se registran
* El descifrado requiere ingreso manual de la clave (entrada oculta)

> 📌 Guarda tu clave inmediatamente en un gestor de contraseñas.

---

## ⚠️ Notas importantes de seguridad

* 🔥 Si perdés la clave, los archivos son irrecuperables
* 🧠 lockstr no almacena copias de seguridad
* 🧪 Probá siempre con `--dry-run`
* 💾 Respaldá archivos importantes antes de cifrar
* 🦠 No protege contra malware ni keyloggers
* 📋 El contenido del portapapeles puede ser accesible por otras aplicaciones

---

## 🛠️ Manejo de errores

lockstr maneja de forma segura:

* Cifrado inválido o corrupto
* Claves incorrectas
* Errores de permisos
* Fallos parciales (continuación opcional)
* Ejecución interrumpida (Ctrl+C)

Las escrituras atómicas evitan la corrupción de archivos.

---

## 🧱 Estructura del proyecto

```
lockstr/
├── lockstr.py      # Aplicación CLI principal
├── installer.py    # Instalador del sistema
├── README.md
└── README_ES.md
```

---

## 🎯 Filosofía de diseño

lockstr está diseñado para ser:

* **Explícito** — sin comportamientos ocultos
* **Seguro por defecto** — opciones de dry-run y confirmación
* **Solo local** — sin red
* **Difícil de usar mal** — encabezados mágicos y validaciones
* **Minimalista** — hace una sola cosa y la hace bien

No está pensado para ser:

* Una solución de backup
* Un gestor de contraseñas
* Una herramienta de cifrado en la nube

---

## 🧪 Plataformas probadas

* Linux (X11 / Wayland)
* Windows 10+
* macOS (zsh / bash)

---

## 🧠 Advertencia final

> **Si cifrás archivos y perdés la clave, no hay forma de recuperarlos.**

> **Esto es intencional.**

---

Hecho con <3 por URDev.
