import { Routes, Route } from "react-router-dom";
import Zones from "./pages/Zones.jsx";
import Meters from "./pages/Meters.jsx";
import Analytics from "./pages/Analytics.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Zones />} />
      <Route path="/meters" element={<Meters />} />
      <Route path="/analytics" element={<Analytics />} />
    </Routes>
  );
}

export default App;