const Prediction = ({ prediction }) => {
  return (
    <li>
      <div className={`p-4 mb-4 text-sm text-gray-800 rounded-lg bg-gray-50 dark:bg-gray-800 dark:text`}>
        <span className="font-medium"></span>
        {`sleep_stages: ${JSON.stringify(prediction.sleep_stages)}, osas: ${JSON.stringify(prediction.osas)}, snorings: ${JSON.stringify(prediction.snorings)}`}
      </div>
    </li>
  )
}

const RealtimePrediction = ({ prediction }) => {
  const { seq, sleepStages, osas, snorings } = prediction

  return (
    <li>
      <div class="container">
        <div class="array-title">seq:</div>
        <div class="array-items">{seq}</div>

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
          <RealtimePrediction key={idx} prediction={prediction} />
        ))}
      </ul>
    </div>
  )
}

export { Predictions }
