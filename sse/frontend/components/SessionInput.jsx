const SessionInput = ({ sessionId, setSessionId }) => {
  return (
    <input
      type="text"
      value={sessionId}
      placeholder="Enter Session ID"
      onChange={(e) => setSessionId(e.target.value)}
      className="input"
    />
  )
}

export { SessionInput }
