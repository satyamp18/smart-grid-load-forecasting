import { useEffect, useState } from "react";

function App() {
  const [forecasts, setForecasts] = useState([]);
  const [temperature, setTemperature] = useState("");
  const [hour, setHour] = useState("");
  const [predicted, setPredicted] = useState(null);

  // GET history
  const loadData = () => {
    fetch("http://127.0.0.1:8000/forecasts")
      .then((res) => res.json())
      .then((data) => setForecasts(data))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    loadData();
  }, []);

  // POST forecast
  const generateForecast = () => {
    fetch("http://127.0.0.1:8000/forecast", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: Number(temperature),
        hour: Number(hour),
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setPredicted(data.predicted_load);
        loadData(); // refresh table
      })
      .catch((err) => console.log(err));
  };

  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <div className="max-w-5xl mx-auto">

        <h1 className="text-4xl font-bold mb-8">
          Smart Grid Load Forecasting
        </h1>

        {/* INPUT */}
        <div className="bg-white p-6 rounded-xl shadow mb-6">
          <h2 className="text-xl font-semibold mb-4">
            Generate Forecast
          </h2>

          <div className="grid gap-4">
            <input
              type="number"
              placeholder="Temperature"
              value={temperature}
              onChange={(e) => setTemperature(e.target.value)}
              className="border p-3 rounded"
            />

            <input
              type="number"
              placeholder="Hour"
              value={hour}
              onChange={(e) => setHour(e.target.value)}
              className="border p-3 rounded"
            />

            <button
              onClick={generateForecast}
              className="bg-blue-600 text-white p-3 rounded"
            >
              Generate Forecast
            </button>
          </div>
        </div>

        {/* OUTPUT */}
        <div className="bg-white p-6 rounded-xl shadow mb-6">
          <h2 className="text-xl font-semibold">
            Predicted Load
          </h2>

          <p className="text-3xl font-bold mt-4">
            {predicted !== null ? `${predicted} MW` : "-- MW"}
          </p>
        </div>

        {/* HISTORY */}
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-4">
            Forecast History
          </h2>

          <table className="w-full">
            <thead>
              <tr>
                <th>ID</th>
                <th>Temperature</th>
                <th>Hour</th>
                <th>Load</th>
              </tr>
            </thead>

            <tbody>
              {forecasts.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.temperature}</td>
                  <td>{item.hour}</td>
                  <td>{item.predicted_load}</td>
                </tr>
              ))}
            </tbody>
          </table>

        </div>
      </div>
    </div>
  );
}

export default App;