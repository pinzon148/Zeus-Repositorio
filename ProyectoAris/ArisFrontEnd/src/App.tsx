import { FormEvent, useState } from 'react'
import './App.css'

type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
}

const BACKEND_URL = 'http://localhost:8000'

const initialMessages: Message[] = [
  {
    id: 'm1',
    role: 'assistant',
    text: 'Bienvenido a Proyecto Aris. Aquí verás un chat diseñado para ofrecer respuestas más claras, interacciones más amables y una interfaz pensada para ti.'
  }
]

function App() {
  const [messages, setMessages] = useState<Message[]>(initialMessages)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const prompt = input.trim()
    if (!prompt) return

    const userMessage: Message = {
      id: `u-${Date.now()}`,
      role: 'user',
      text: prompt
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(`${BACKEND_URL}/api/aris-fast`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'gpt-4o-mini',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
          max_tokens: 1000
        })
      })

      if (!response.ok) {
        let errorText = response.statusText
        try {
          const errorBody = await response.json()
          if (errorBody?.detail) {
            errorText = errorBody.detail
          }
        } catch {
          // ignore parse error
        }
        throw new Error(`Backend error: ${errorText}`)
      }

      const data = await response.json()
      
      // Extraer el contenido de forma segura
      let assistantText = 'No se pudo obtener una respuesta.'
      
      if (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content) {
        assistantText = data.choices[0].message.content
      } else if (typeof data === 'string') {
        assistantText = data
      } else if (data.detail) {
        throw new Error(data.detail)
      }

      const assistantMessage: Message = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        text: assistantText
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorText =
        error instanceof Error
          ? error.message
          : 'Error al conectar con el backend. Asegúrate de que está ejecutándose en http://localhost:8000'

      const errorMessage: Message = {
        id: `e-${Date.now()}`,
        role: 'assistant',
        text: `Error: ${errorText}`
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setMessages(initialMessages)
    setInput('')
  }

  return ( 
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Proyecto Aris</p>
          <h1>Aris: mejor porque está hecho para ti</h1>
          <p className="hero-copy">
            Aris ofrece respuestas más adaptadas, una experiencia visual más amable y un flujo de conversación pensado para que te sientas en control.
          </p>
        </div>
        <button type="button" className="secondary-button" onClick={handleClear}>
          Limpiar chat
        </button>
      </header>

      <div className="chat-panel">
        <div className="chat-log">
          {messages.map((message) => (
            <article key={message.id} className={`chat-message ${message.role}`}>
              <span className="message-role">{message.role === 'user' ? 'Tú' : 'Aris'}</span>
              <p>{message.text}</p>
            </article>
          ))}
          {loading && (
            <article className="chat-message assistant">
              <span className="message-role">Aris</span>
              <p>Escribiendo...</p>
            </article>
          )}
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Escribe tu mensaje aquí..."
            autoComplete="off"
            disabled={loading}
          />
          <button type="submit" className="primary-button" disabled={!input.trim() || loading}>
            {loading ? 'Enviando...' : 'Enviar'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
