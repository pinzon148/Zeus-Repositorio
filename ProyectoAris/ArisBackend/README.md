# Aris Backend

Backend Python para el proyecto Aris.

## Ejecutar

1. Crear un entorno virtual:

```bash
python -m venv venv
```

2. Activar el entorno virtual:

```powershell
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Establecer la clave de OpenAI:

```powershell
setx OPENAI_API_KEY "tu_api_key"
```

5. Ejecutar el servidor:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Endpoints

- `GET /`
- `GET /api/status`
- `GET /api/items`
- `GET /api/items/{item_id}`
- `GET /api/joke`
- `GET /api/quote`
- `POST /api/chat`
- `POST /api/chat-enriched` (integra datos reales de APIs)
- `POST /api/aris` (modo completo: con datos en tiempo real, respuesta más lenta)
- `POST /api/aris-fast` (modo rápido: sin APIs externas, respuesta inmediata)

## Ventajas de Aris sobre ChatGPT

- **Datos en tiempo real**: accede a APIs públicas (clima, etc.)
- **Múltiples fuentes**: integra varias APIs, no solo OpenAI
- **Análisis superior**: enriquece prompts con información externa
- **Respuestas actualizadas**: ChatGPT tiene datos estáticos, Aris integra información viva
- **Modo rápido**: `/api/aris-fast` para respuestas inmediatas
- **Caché inteligente**: reutiliza datos externos para no ralentizar

## Modos de respuesta

- **`/api/aris`**: Modo completo con datos externos (recomendado para análisis profundo)
- **`/api/aris-fast`**: Modo rápido sin consultas externas (recomendado para chat interactivo)

## Uso de APIs externas

- `GET /api/joke` consume `https://icanhazdadjoke.com/`
- `GET /api/quote` consume `https://api.quotable.io/random`
- `POST /api/chat-enriched` combina un chiste externo con el prompt antes de llamar a OpenAI

## Uso del chat

Enviar JSON al endpoint `/api/chat`:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    { "role": "system", "content": "Eres un asistente útil." },
    { "role": "user", "content": "Hola, genera un saludo para mi app." }
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

La respuesta incluye el resultado devuelto por la API de OpenAI.

> Nota: las restricciones de uso y los límites de la API dependen de la cuenta y el plan de OpenAI. Este backend solo conecta tu aplicación con el servicio GPT.
