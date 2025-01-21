import { useState } from "react"

const DisplayPrediction = ({ prediction }) => {
  return (
    <li>
      <div className={`p-4 mb-4 text-sm text-gray-800 rounded-lg bg-gray-50 dark:bg-gray-800 dark:text`}>
        <span className="font-medium"></span>
        {`sleep_stages: ${JSON.stringify(prediction.sleep_stages)}, osas: ${JSON.stringify(prediction.osas)}, snorings: ${JSON.stringify(prediction.snorings)}`}
      </div>
    </li>
  )
}

const DisplayPredictions = ({ predictions }) => {
  if (predictions.length === 0) return

  return (
    <div>
      <ul>
        {predictions.map((prediction, idx) => (
          <DisplayPrediction key={idx} prediction={prediction} />
        ))}
      </ul>
    </div>
  )
}

const StartSSEButton = ({ sessionId, sse, setSse, setPredictions }) => {
  const startSSE = () => {
    if (sse) return

    if (!sessionId) {
      alert("Please enter a session id")
      return
    }

    const eventSource = new EventSource(`http://localhost:8000/stream/${sessionId}`, { withCredentials: true })

    eventSource.onmessage = (event) => {
      const prediction = JSON.parse(event.data.replace("data: ", ""))
      setPredictions((prev) => [prediction, ...prev])
    }

    eventSource.onerror = () => {
      console.error("sse connection error")
      eventSource.close()
    }

    setSse(eventSource)
  }

  return (
    <button className="button" onClick={startSSE}>
      Start Stream
    </button>
  )
}

const EndSSEButton = ({ sse, setSse }) => {
  const endSSE = () => {
    if (sse) {
      sse.close()
      setSse(null)
      console.log("sse connection closed")
    }
  }

  return (
    <button className="button" onClick={endSSE}>
      End Stream
    </button>
  )
}

export default function Home() {
  const [sessionId, setSessionId] = useState("")
  const [predictions, setPredictions] = useState([])
  const [sse, setSse] = useState(null)

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-xl font-bold mb-4">Sleep Data SSE</h1>
      <div className="input-container">
        <input
          type="text"
          value={sessionId}
          placeholder="Enter Session ID"
          onChange={(e) => setSessionId(e.target.value)}
          className="input"
        />
        <StartSSEButton sessionId={sessionId} sse={sse} setSse={setSse} setPredictions={setPredictions} />
        <EndSSEButton sse={sse} setSse={setSse} />
        <div className="sse-status">
          <span>{sse ? "SSE Connected" : "SSE Disconnected"}</span>
        </div>
      </div>
      <DisplayPredictions predictions={predictions} />
    </main>
  )
}
