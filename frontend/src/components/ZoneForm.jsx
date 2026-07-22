import { useEffect, useState } from "react";

function ZoneForm({
  selectedZone,
  onSubmit,
  onCancel,
}) {
  const [zoneName, setZoneName] = useState("");
  const [capacity, setCapacity] = useState("");

  useEffect(() => {
    if (selectedZone) {
      setZoneName(selectedZone.zone_name);
      setCapacity(selectedZone.max_capacity_kw);
    } else {
      setZoneName("");
      setCapacity("");
    }
  }, [selectedZone]);

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      zone_name: zoneName.trim(),
      max_capacity_kw: Number(capacity),
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal">

        <h2>
          {selectedZone ? "Edit Zone" : "Add Zone"}
        </h2>

        <form onSubmit={handleSubmit}>

          <input
            type="text"
            placeholder="Zone Name"
            value={zoneName}
            onChange={(e) => setZoneName(e.target.value)}
            required
          />

          <input
            type="number"
            placeholder="Maximum Capacity (KW)"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            required
          />

          <div className="modal-actions">

            <button
              type="button"
              className="cancel-btn"
              onClick={onCancel}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="primary-btn"
            >
              {selectedZone ? "Update Zone" : "Add Zone"}
            </button>

          </div>

        </form>

      </div>
    </div>
  );
}

export default ZoneForm;