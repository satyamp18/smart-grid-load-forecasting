import { useEffect, useMemo, useState } from "react";
import { toast } from "react-toastify";

import ReadingForm from "../components/ReadingForm";
import ReadingTable from "../components/ReadingTable";

import {
  getReadings,
  createReading,
  updateReading,
  deleteReading,
} from "../services/readingService";

import "../assets/styles/readings.css";

function Readings() {
  const [readings, setReadings] = useState([]);
  const [loading, setLoading] = useState(true);

  const [search, setSearch] = useState("");

  const [showModal, setShowModal] = useState(false);

  const [selectedReading, setSelectedReading] = useState(null);

  const loadReadings = async () => {
    try {
      setLoading(true);
      const data = await getReadings();
      setReadings(data);
    } catch (error) {
      toast.error("Failed to load readings");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReadings();
  }, []);

  const filteredReadings = useMemo(() => {
    return readings.filter((reading) =>
      reading.meter_id
        .toString()
        .includes(search.toLowerCase())
    );
  }, [readings, search]);

  const handleAdd = () => {
    setSelectedReading(null);
    setShowModal(true);
  };

  const handleEdit = (reading) => {
    setSelectedReading(reading);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this reading?")) return;

    try {
      await deleteReading(id);
      toast.success("Reading deleted successfully");
      loadReadings();
    } catch {
      toast.error("Unable to delete reading");
    }
  };

  const handleSubmit = async (formData) => {
    try {
      if (selectedReading) {
        await updateReading(selectedReading.id, formData);
        toast.success("Reading updated successfully");
      } else {
        await createReading(formData);
        toast.success("Reading added successfully");
      }

      setShowModal(false);
      loadReadings();
    } catch {
      toast.error("Operation failed");
    }
  };

  return (
    <div className="page-container">

      <div className="page-header">

        <div>
          <h2>Meter Readings</h2>
          <p>Manage smart grid meter readings.</p>
        </div>

        <button
          className="primary-btn"
          onClick={handleAdd}
        >
          + Add Reading
        </button>

      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <h3>{readings.length}</h3>
          <span>Total Readings</span>
        </div>

        <div className="stat-card">
          <h3>
            {readings
              .reduce(
                (sum, item) => sum + item.power_kw,
                0
              )
              .toFixed(2)}
          </h3>
          <span>Total kW</span>
        </div>

      </div>

      <div className="table-card">

        <div className="table-toolbar">

          <input
            type="text"
            placeholder="Search by Meter ID..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

        </div>

        <ReadingTable
          readings={filteredReadings}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />

      </div>

      {showModal && (
        <ReadingForm
          reading={selectedReading}
          onSubmit={handleSubmit}
          onClose={() => setShowModal(false)}
        />
      )}

    </div>
  );
}

export default Readings;