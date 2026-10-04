# 🤖 Discord Bot IA

Este es un bot de Discord potenciado con Inteligencia Artificial utilizando la API de OpenRouter.

## 🚀 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
* **Node.js** (versión 18 o superior) o **Python** (según el lenguaje que uses)
* **Git** configurado en tu equipo

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com
cd tu-repositorio
```

### 2. Configurar las Variables de Entorno ⚠️ (Muy Importante)
El proyecto necesita credenciales privadas para funcionar. Estas credenciales **nunca** deben subirse al repositorio público.

1. En la raíz del proyecto, crea un archivo llamado exactamente **`.env`**.
2. Copia y pega las siguientes variables dentro del archivo `.env`:

```env
DISCORD_TOKEN=tu_token_de_discord_aqui
OPENROUTER_API_KEY=tu_api_key_de_openrouter_aqui
```

3. Reemplaza `tu_token_de_discord_aqui` y `tu_api_key_de_openrouter_aqui` con tus credenciales reales.

> 💡 **Nota de seguridad:** El archivo `.env` ya se encuentra incluido en el `.gitignore`, por lo que Git ignorará este archivo automáticamente para evitar filtraciones de seguridad.

### 3. Instalar dependencias
```bash
# Si usas Node.js:
npm install

# Si usas Python:
pip install -r requirements.txt
```

### 4. Iniciar el Bot
```bash
# Si usas Node.js:
npm start

# Si usas Python:
python main.py
```
