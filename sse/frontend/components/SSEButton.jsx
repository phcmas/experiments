import { useStartSSE, useEndSSE } from "@/hooks/useSSE"

const StartSSEButton = ({ sessionId, sse, setSse, setPredictions }) => {
  const { startSSE } = useStartSSE(sessionId, sse, setSse, setPredictions)

  return (
    <button className="button" onClick={startSSE}>
      Start Stream
    </button>
  )
}

const EndSSEButton = ({ sse, setSse }) => {
  const { endSSE } = useEndSSE(sse, setSse)

  return (
    <button className="button" onClick={endSSE}>
      End Stream
    </button>
  )
}

export { StartSSEButton, EndSSEButton }
