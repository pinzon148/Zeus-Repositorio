import { FormEvent, useState } from 'react'
import './App.css'

type Message = {
  id: string
  role: 'user' | 'assistant'
  text: string
}

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

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const prompt = input.trim()
    if (!prompt) return

    setMessages((prev) => [
      ...prev,
      { id: `u-${Date.now()}`, role: 'user', text: prompt },
      {
        id: `a-${Date.now()}`,
        role: 'assistant',
        text: 'Esta es una respuesta de ejemplo. Más adelante podemos conectar una API real.'
      },
    ])
    setInput('')
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
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Escribe tu mensaje aquí..."
            autoComplete="off"
          />
          <button type="submit" className="primary-button" disabled={!input.trim()}>
            Enviar
          </button>
        </form>
      </div>
    </div>
  )
}

export default App
