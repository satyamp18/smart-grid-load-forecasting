import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import Zones from "./pages/Zones";
import Meters from "./pages/Meters";
import Readings from "./pages/Readings";
import Analytics from "./pages/Analytics";
import Reports from "./pages/Reports";
import NotFound from "./pages/NotFound";
import Alerts from "./pages/Alerts";


function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/zones" element={<Zones />} />
          <Route path="/meters" element={<Meters />} />
          <Route path="/readings" element={<Readings />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/alerts" element={<Alerts />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;