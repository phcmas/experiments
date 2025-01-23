const Prediction = ({ prediction }) => {
  const { seq, sleepStages, osas, snorings, arrivedAt } = prediction

  return (
    <li>
      <div class="container">
        <div class="array-title">arrived_at:</div>
        <div class="array-items">{arrivedAt.split(" ")[1]}</div>

        <div class="array-title">sleep_stages:</div>
        <div class="array-items">{JSON.stringify(sleepStages)}</div>

        <div class="array-title">osas:</div>
        <div class="array-items">{JSON.stringify(osas)}</div>

        <div class="array-title">snorings:</div>
        <div class="array-items">{JSON.stringify(snorings)}</div>
      </div>
    </li>
  )
}

const Predictions = ({ predictions }) => {
  if (predictions.length === 0) return

  return (
    <div>
      <ul>
        {predictions.map((prediction, idx) => (
          <Prediction key={idx} prediction={prediction} />
        ))}
      </ul>
    </div>
  )
}

export { Predictions }
