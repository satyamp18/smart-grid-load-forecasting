import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import {
  getReports,
  createReport,
} from "../services/reportService";

import "../assets/styles/reports.css";

const initialForm = {
  zone_id: "",
  total_load_kw: "",
  report_time: "",
};

function Reports() {
  const [reports, setReports] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(true);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await getReports();
      setReports(data);
    } catch (err) {
      toast.error("Failed to load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log({
        zone_id: Number(form.zone_id),
        total_load_kw: Number(form.total_load_kw),
        report_time: form.report_time,
    });

    try {
      await createReport({
        zone_id: Number(form.zone_id),
        total_load_kw: Number(form.total_load_kw),
        report_time: form.report_time,
      });

      toast.success("Report Added Successfully");

      setForm(initialForm);

      loadReports();
    } catch {
      toast.error("Unable to create report");
    }
  };

  return (
    <div className="reports-page">

      <div className="reports-header">
        <h2>Load Reports</h2>

        <button onClick={loadReports}>
          Refresh
        </button>
      </div>

      <div className="summary-card">

        <h3>Total Reports</h3>

        <span>{reports.length}</span>

      </div>

      <form
        className="report-form"
        onSubmit={handleSubmit}
      >

        <input
          type="number"
          name="zone_id"
          placeholder="Zone ID"
          value={form.zone_id}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          step="0.01"
          name="total_load_kw"
          placeholder="Total Load (kW)"
          value={form.total_load_kw}
          onChange={handleChange}
          required
        />

        <input
          type="datetime-local"
          name="report_time"
          value={form.report_time}
          onChange={handleChange}
          required
        />

        <button type="submit">
          Generate Report
        </button>

      </form>

      <div className="table-container">

        {loading ? (

          <p>Loading Reports...</p>

        ) : reports.length === 0 ? (

          <p>No Reports Found</p>

        ) : (

          <table>

            <thead>

              <tr>

                <th>ID</th>
                <th>Zone</th>
                <th>Total Load (kW)</th>
                <th>Report Time</th>

              </tr>

            </thead>

            <tbody>

              {reports.map((report) => (

                <tr key={report.id}>

                  <td>{report.id}</td>

                  <td>{report.zone_id}</td>

                  <td>{report.total_load_kw}</td>

                  <td>
                    {new Date(
                      report.report_time
                    ).toLocaleString()}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        )}

      </div>

    </div>
  );
}

export default Reports;