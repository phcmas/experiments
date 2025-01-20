function createSessionId() {
  const stringPool = "abcdefghijklmnopqrstuvwxyz0123456789"

  const randomStr = new Array(5)
    .fill(null)
    .map(() => stringPool[Math.floor(Math.random() * stringPool.length)])
    .join("")

  const withoutMs = new Date().toISOString().split(".")[0]
  const startTime = withoutMs.replace(/[-T:Z]/g, "") // Remove "-", "T", ":", and "Z"
  return `${startTime}_${randomStr}`
}

export { createSessionId }
