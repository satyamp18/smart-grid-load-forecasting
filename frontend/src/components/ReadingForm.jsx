import { useEffect, useState } from "react";

function ReadingForm({ reading, onSubmit, onClose }) {
  const [formData, setFormData] = useState({
    meter_id: "",
    voltage: "",
    current: "",
    timestamp: "",
  });

  useEffect(() => {
    if (reading) {
      setFormData({
        meter_id: reading.meter_id,
        voltage: reading.voltage,
        current: reading.current,
        timestamp: reading.timestamp?.slice(0, 16),
      });
    }
  }, [reading]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const power =
    formData.voltage && formData.current
      ? (
          (Number(formData.voltage) *
            Number(formData.current)) /
          1000
        ).toFixed(2)
      : "0.00";

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      !formData.meter_id ||
      !formData.voltage ||
      !formData.current ||
      !formData.timestamp
    ) {
      alert("Please fill all fields");
      return;
    }

    onSubmit({
      ...formData,
      meter_id: Number(formData.meter_id),
      voltage: Number(formData.voltage),
      current: Number(formData.current),
      timestamp: new Date(formData.timestamp).toISOString(),
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal">

        <h2>
          {reading ? "Edit Reading" : "Add Reading"}
        </h2>

        <form onSubmit={handleSubmit}>

          <label>Meter ID</label>
          <input
            type="number"
            name="meter_id"
            value={formData.meter_id}
            onChange={handleChange}
          />

          <label>Voltage (V)</label>
          <input
            type="number"
            step="0.01"
            name="voltage"
            value={formData.voltage}
            onChange={handleChange}
          />

          <label>Current (A)</label>
          <input
            type="number"
            step="0.01"
            name="current"
            value={formData.current}
            onChange={handleChange}
          />

          <label>Power (kW)</label>
          <input
            value={power}
            disabled
          />

          <label>Timestamp</label>
          <input
            type="datetime-local"
            name="timestamp"
            value={formData.timestamp}
            onChange={handleChange}
          />

          <div className="modal-actions">

            <button
              type="submit"
              className="primary-btn"
            >
              {reading ? "Update" : "Save"}
            </button>

            <button
              type="button"
              className="secondary-btn"
              onClick={onClose}
            >
              Cancel
            </button>

          </div>

        </form>

      </div>
    </div>
  );
}

export default ReadingForm;