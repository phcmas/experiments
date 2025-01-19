import { useState, useEffect } from "react"

const events = (type, message) => {
  let color = "gray"

  switch (type) {
    case "info":
      color = "blue"
      break
    case "error":
      color = "red"
      break
    case "success":
      color = "green"
      break
    case "warning":
      color = "yellow"
      break
  }

  return (
    <div
      className={`p-4 mb-4 text-sm text-${color}-800 rounded-lg bg-${color}-50 dark:bg-gray-800 dark:text`}
    >
      <span className="font-medium">{type}! </span>
      {message}
    </div>
  )
}

export default function Home() {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    const sse = new EventSource("http://localhost:8000/stream", {
      withCredentials: true,
    })

    sse.onmessage = (event) => {
      const data = JSON.parse(event.data.replace("data: ", ""))
      setMessages((prev) => [...prev, data])

      console.log(event.data)
    }
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <ul>
        {messages.length > 0 ? (
          messages.map((message, i) => {
            return <li key={i}>{events(message.type, message.message)}</li>
          })
        ) : (
          <p>No messages</p>
        )}
      </ul>
    </main>
  )
}
