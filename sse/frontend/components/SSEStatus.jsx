const SSEStatus = ({ sse }) => {
  return (
    <div className="sse-status">
      <span>{sse ? "SSE Connected" : "SSE Disconnected"}</span>
    </div>
  )
}

export { SSEStatus }
