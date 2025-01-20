import { useState, useEffect } from "react"
import { createSessionId } from "./util"

function realtime_data(data) {
  let color = "gray"
  let message = `sleep_stages: ${JSON.stringify(data.sleep_stages)}, osas: ${JSON.stringify(data.osas)}, snoring: ${JSON.stringify(data.snorings)} `

  return (
    <div
      className={`p-4 mb-4 text-sm text-${color}-800 rounded-lg bg-${color}-50 dark:bg-gray-800 dark:text`}
    >
      <span className="font-medium"></span>
      {`sleep_stages: ${JSON.stringify(data.sleep_stages)}, osas: ${JSON.stringify(data.osas)}, snoring: ${JSON.stringify(data.snorings)}`}
    </div>
  )
}

export default function Home() {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    const session_id = createSessionId()
    const sse = new EventSource(`http://localhost:8000/stream/${session_id}`, {
      withCredentials: true,
    })

    console.log(`session_id: ${session_id}`)

    sse.onmessage = (event) => {
      const data = JSON.parse(event.data.replace("data: ", ""))
      setMessages((prev) => [...prev, data])
    }
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <ul>
        {messages.length > 0 ? (
          messages.map((message, i) => {
            return <li key={i}>{realtime_data(message)}</li>
          })
        ) : (
          <p>No messages</p>
        )}
      </ul>
    </main>
  )
}
