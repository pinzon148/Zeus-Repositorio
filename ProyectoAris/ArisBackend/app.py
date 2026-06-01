import os
from typing import List, Optional
from datetime import datetime, timedelta

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "gpt-4o-mini"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY no definido. Establece la variable de entorno antes de ejecutar el backend.")

openai_client = OpenAI(api_key=openai_api_key)

# Caché simple para datos externos
weather_cache = {"data": None, "timestamp": None}

app = FastAPI(title="Aris Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items_db = [
    Item(id=1, name="Artículo 1", description="Ejemplo de item"),
    Item(id=2, name="Artículo 2", description="Otro ejemplo"),
]

@app.get("/")
async def root():
    return {"message": "Backend de Aris activo"}

@app.get("/api/status")
async def status():
    return {"status": "ok", "service": "aris-backend"}

@app.get("/api/items", response_model=List[Item])
async def list_items():
    return items_db

@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = openai_client.chat.completions.create(
            model=request.model,
            messages=[message.dict() for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return response.to_dict() if hasattr(response, "to_dict") else response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/joke")
async def joke():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://icanhazdadjoke.com/",
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Error al obtener chiste: {exc}")

@app.get("/api/quote")
async def quote():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.quotable.io/random")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Error al obtener cita: {exc}")

@app.post("/api/chat-enriched")
async def chat_enriched(request: ChatRequest):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            weather = await client.get(
                "https://api.weatherapi.com/v1/current.json?key=free&q=London",
            )
            weather.raise_for_status()
            weather_data = weather.json()

        weather_info = (
            f"Clima: {weather_data.get('current', {}).get('condition', {}).get('text')}. "
            f"Temp: {weather_data.get('current', {}).get('temp_c')}°C."
        )

        enriched_messages = [
            {"role": "system", "content": "Eres Aris, más avanzado que ChatGPT porque integras datos reales en tiempo real."},
            *[message.dict() for message in request.messages],
            {
                "role": "system",
                "content": (
                    f"Datos reales disponibles: {weather_info} Usa esto para respuestas más actualizadas."
                ),
            },
        ]

        response = openai_client.chat.completions.create(
            model=request.model,
            messages=enriched_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return response.to_dict() if hasattr(response, "to_dict") else response
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Error al obtener API externa: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/aris")
async def aris_advanced(request: ChatRequest):
    """Endpoint principal de Aris: responde usando múltiples fuentes de datos."""
    try:
        weather_info = ""
        # Usar caché si es reciente (menos de 5 minutos)
        if weather_cache["data"] and weather_cache["timestamp"]:
            if datetime.now() - weather_cache["timestamp"] < timedelta(minutes=5):
                weather_info = weather_cache["data"]
            else:
                # Actualizar caché
                async with httpx.AsyncClient(timeout=5.0) as client:
                    weather = await client.get(
                        "https://api.weatherapi.com/v1/current.json?key=free&q=London",
                    )
                    weather.raise_for_status()
                    weather_data = weather.json()
                    weather_info = (
                        f"Clima: {weather_data.get('current', {}).get('condition', {}).get('text')}. "
                        f"Temperatura: {weather_data.get('current', {}).get('temp_c')}°C."
                    )
                    weather_cache["data"] = weather_info
                    weather_cache["timestamp"] = datetime.now()
        else:
            # Primera vez, obtener datos
            async with httpx.AsyncClient(timeout=5.0) as client:
                weather = await client.get(
                    "https://api.weatherapi.com/v1/current.json?key=free&q=London",
                )
                weather.raise_for_status()
                weather_data = weather.json()
                weather_info = (
                    f"Clima: {weather_data.get('current', {}).get('condition', {}).get('text')}. "
                    f"Temperatura: {weather_data.get('current', {}).get('temp_c')}°C."
                )
                weather_cache["data"] = weather_info
                weather_cache["timestamp"] = datetime.now()

        enriched_messages = [
            {
                "role": "system",
                "content": (
                    "Eres Aris: avanzado, con acceso a datos reales, APIs públicas y análisis superior. "
                    "ChatGPT no puede hacer esto porque sus datos son estáticos. "
                    "Tú tienes información en tiempo real. "
                    f"Datos ahora: {weather_info}"
                ),
            },
            *[message.dict() for message in request.messages],
        ]

        response = openai_client.chat.completions.create(
            model=request.model,
            messages=enriched_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return response.to_dict() if hasattr(response, "to_dict") else response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/aris-fast")
async def aris_fast(request: ChatRequest):
    """Respuesta rápida sin consultar APIs externas."""
    try:
        messages = [
            {
                "role": "system",
                "content": "Eres Aris: asistente avanzado optimizado para respuesta rápida. Proporciona respuestas directas y útiles.",
            },
            *[message.dict() for message in request.messages],
        ]

        response = openai_client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return response.to_dict() if hasattr(response, "to_dict") else response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
