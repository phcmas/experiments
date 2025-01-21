import { useState } from "react"
import { Predictions } from "@/components/Prediction"
import { StartSSEButton, EndSSEButton } from "@/components/SSEButton"
import { SessionInput } from "@/components/SessionInput"
import { SSEStatus } from "@/components/SSEStatus"

export default function Home() {
  const [sessionId, setSessionId] = useState("")
  const [predictions, setPredictions] = useState([])
  const [sse, setSse] = useState(null)

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-xl font-bold mb-4">Sleep Data SSE</h1>
      <div className="input-container">
        <SessionInput sessionId={sessionId} setSessionId={setSessionId} />
        <StartSSEButton sessionId={sessionId} sse={sse} setSse={setSse} setPredictions={setPredictions} />
        <EndSSEButton sse={sse} setSse={setSse} />
        <SSEStatus sse={sse} />
      </div>
      <Predictions predictions={predictions} />
    </main>
  )
}
