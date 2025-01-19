import { useState, useEffect } from "react"

export default function Home() {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    const sse = new EventSource("http://localhost:8000/stream", {
      withCredentials: true,
    })

    sse.onmessage = (event) => {
      console.log(event.data)
    }
  }, [])

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      I am from homepage
    </main>
  )
}
