import { useCallback } from "react"

const useStartSSE = (sessionId, sse, setSse, setPredictions) => {
  const startSSE = useCallback(() => {
    if (sse) return

    if (!sessionId) {
      alert("Please enter a session id")
      return
    }

    const eventSource = new EventSource(`http://localhost:8000/v1/stream/${sessionId}`)

    eventSource.onmessage = (event) => {
      const raw_data = JSON.parse(event.data.replace("data: ", ""))
      const prediction = {
        seq: raw_data.inference_seq,
        sleepStages: raw_data.sleep_stages,
        osas: raw_data.osas,
        snorings: raw_data.snorings,
        arrivedAt: new Date().toLocaleString("sv-SE", { hour12: false }),
      }

      setPredictions((prev) => [prediction, ...prev])
    }

    eventSource.onerror = () => {
      console.error("sse connection error")
      eventSource.close()
    }

    setSse(eventSource)
  }, [sessionId, sse, setPredictions, setSse])

  return { startSSE }
}

const useEndSSE = (sse, setSse) => {
  const endSSE = useCallback(() => {
    if (sse) {
      sse.close()
      setSse(null)
      console.log("sse connection closed")
    }
  }, [sse, setSse])

  return { endSSE }
}

export { useStartSSE, useEndSSE }
