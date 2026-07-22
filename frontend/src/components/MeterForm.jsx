import { useEffect, useState } from "react";

function MeterForm({ meter, onSubmit, zones, onClose }) {
  const [meterCode, setMeterCode] = useState("");
  const [zoneId, setZoneId] = useState("");

  useEffect(() => {
    if (meter) {
      setMeterCode(meter.meter_code);
      setZoneId(meter.zone_id.toString());
    } else {
      setMeterCode("");
      setZoneId("");
    }
  }, [meter]);

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      meter_code: meterCode.trim(),
      zone_id: Number(zoneId),
    });

    setMeterCode("");
    setZoneId("");
  };

  return (
    <div className="modal-overlay">
      <div className="modal">

        <h2>{meter ? "Edit Smart Meter" : "Add Smart Meter"}</h2>

        <form onSubmit={handleSubmit}>

          <input
            type="text"
            placeholder="Enter Meter Code"
            value={meterCode}
            onChange={(e) => setMeterCode(e.target.value)}
            required
          />

          <select
            value={zoneId}
            onChange={(e) => setZoneId(e.target.value)}
            required
          >
            <option value="">Select Zone</option>

            {zones.map((zone) => (
              <option key={zone.id} value={zone.id}>
                {zone.zone_name}
              </option>
            ))}
          </select>

          <div className="modal-actions">

            <button
              type="button"
              className="cancel-btn"
              onClick={onClose}
            >
              Cancel
            </button>

            <button
              type="submit"
              className="primary-btn"
            >
              {meter ? "Update Meter" : "Add Meter"}
            </button>

          </div>

        </form>

      </div>
    </div>
  );
}

export default MeterForm;