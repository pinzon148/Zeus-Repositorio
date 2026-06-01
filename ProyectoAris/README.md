# 🚀 Aris - Chat Avanzado con IA

Aris es una aplicación de chat inteligente que combina **Frontend React moderno** con **Backend Python avanzado** para ofrecer respuestas más inteligentes, contextuales y actualizadas que ChatGPT tradicional.

## ✨ Características

- **Respuestas en tiempo real**: Integración con múltiples APIs públicas para datos actualizados
- **Interfaz moderna**: Diseño clean con animaciones fluidas y tema azul cian
- **Dos modos de respuesta**:
  - **Modo Rápido** (`/api/aris-fast`): Respuestas inmediatas sin consultas externas
  - **Modo Completo** (`/api/aris`): Análisis profundo con datos externos
- **Caché inteligente**: Reutiliza datos para no ralentizar
- **Accesible**: Totalmente responsivo (móvil, tablet, desktop)
- **API extensible**: Estructura lista para agregar más integraciones

## 📋 Requisitos

### Frontend
- Node.js 16+ 
- npm o yarn

### Backend
- Python 3.10+
- pip

## 🛠️ Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone <repo-url>
cd ProyectoAris
```

### 2. Configurar Backend

```bash
cd ArisBackend

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key de OpenAI
# Windows:
setx OPENAI_API_KEY "sk-tu-clave-aqui"
# macOS/Linux:
export OPENAI_API_KEY="sk-tu-clave-aqui"

# Ejecutar servidor
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

El backend estará disponible en `http://localhost:8000`

### 3. Configurar Frontend

En **otra terminal**:

```bash
cd ArisFrontEnd

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173` (o el puerto que vite asigne)

## 🎯 Uso

1. Abre el navegador en `http://localhost:5173`
2. Escribe tu pregunta en el campo de chat
3. Aris procesará tu mensaje y enviará una respuesta inteligente

## 📡 API Endpoints

### Frontend → Backend

El frontend consume estos endpoints:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/aris-fast` | POST | Respuesta rápida (sin APIs externas) |
| `/api/aris` | POST | Respuesta completa (con datos externos) |
| `/api/chat` | POST | Chat simple (solo OpenAI) |
| `/api/status` | GET | Estado del servidor |

### Estructura de request (POST)

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    { "role": "user", "content": "Tu pregunta aquí" }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

## 🏗️ Estructura del Proyecto

```
ProyectoAris/
├── ArisFrontEnd/                 # Frontend React + TypeScript
│   ├── src/
│   │   ├── App.tsx              # Componente principal
│   │   ├── App.css              # Estilos modernos
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
│
├── ArisBackend/                  # Backend FastAPI Python
│   ├── app.py                   # Aplicación principal
│   ├── requirements.txt         # Dependencias Python
│   └── README.md               # Documentación backend
│
└── README.md                     # Este archivo
```

## 🔧 Tecnologías

### Frontend
- **React 19** - Framework UI
- **TypeScript** - Type safety
- **Vite** - Build tool rápido
- **CSS3** - Diseño moderno con variables CSS

### Backend
- **FastAPI** - Framework web asincrónico
- **OpenAI** - API de chat completions
- **httpx** - Cliente HTTP asincrónico
- **Pydantic** - Validación de datos
- **CORS** - Soporte para solicitudes cruzadas

## 🚀 Características Avanzadas

### Caché Inteligente
El backend cachea datos externos (como clima) durante 5 minutos para:
- Reducir latencia
- Minimizar llamadas a APIs externas
- Mantener coherencia en conversaciones

### Enriquecimiento de Prompts
Antes de enviar a OpenAI, el backend:
1. Obtiene datos contextuales (clima, noticias, etc.)
2. Enriquece el prompt del usuario
3. Envía el prompt mejorado a OpenAI
4. Devuelve respuesta más inteligente y contextualizada

### Validación de Datos
Todos los requests usan modelos Pydantic:
- `ChatRequest` - Valida estructura de chat
- `Message` - Valida mensajes individuales

## 📝 Variables de Entorno

### Backend (ArisBackend)

```env
OPENAI_API_KEY=sk-...       # Requerido: Clave API de OpenAI
```

## 🐛 Troubleshooting

### Error: "Failed to fetch"
- El backend no está ejecutándose en `http://localhost:8000`
- Solución: Ejecuta `uvicorn app:app --reload` en la carpeta ArisBackend

### Error: "OPENAI_API_KEY no definido"
- Olvidaste configurar la variable de entorno
- Solución: Ejecuta `setx OPENAI_API_KEY "sk-tu-clave"` y reinicia PowerShell

### Respuestas lentas
- Modo `/api/aris` llama a APIs externas (más lento)
- Solución: Usa `/api/aris-fast` para respuestas inmediatas

### Python no encontrado
- Instala Python 3.10+ desde https://www.python.org/downloads
- Marca la casilla "Add Python to PATH" durante la instalación

## 📚 Documentación Adicional

- [Backend README](./ArisBackend/README.md) - Detalles de la API
- [OpenAI Docs](https://platform.openai.com/docs) - Documentación de OpenAI

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la MIT License - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autores

Proyecto Aris - Chat inteligente con IA

## 🆘 Soporte

Si tienes problemas:

1. Revisa el [Troubleshooting](#-troubleshooting)
2. Verifica que ambos servidores (frontend y backend) estén ejecutándose
3. Abre un issue en el repositorio

---

**Hecho con ❤️ para conversaciones inteligentes**
