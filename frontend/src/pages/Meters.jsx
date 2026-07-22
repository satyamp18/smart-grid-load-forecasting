import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import "../assets/styles/meters.css";

import MeterForm from "../components/MeterForm";
import MeterTable from "../components/MeterTable";

import {
  getMeters,
  createMeter,
  updateMeter,
  deleteMeter,
} from "../services/meterService";

import { getZones } from "../services/zoneService";

function Meters() {
  const [meters, setMeters] = useState([]);
  const [zones, setZones] = useState([]);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const [editingMeter, setEditingMeter] = useState(null);

  const loadData = async () => {
    try {
      const meterData = await getMeters();
      const zoneData = await getZones();

      setMeters(meterData);
      setZones(zoneData);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load data");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSubmit = async (meter) => {
    try {
      if (editingMeter) {
        await updateMeter(editingMeter.id, meter);
        toast.success("Meter Updated Successfully");
      } else {
        await createMeter(meter);
        toast.success("Meter Added Successfully");
      }

      setEditingMeter(null);
      setOpen(false);

      await loadData();
    } catch (error) {
      console.error(error);
      toast.error("Operation Failed");
    }
  };

  const handleDelete = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this meter?"
    );

    if (!confirmed) return;

    try {
      await deleteMeter(id);

      toast.success("Meter Deleted Successfully");

      await loadData();
    } catch (error) {
      console.error(error);
      toast.error("Delete Failed");
    }
  };

  const handleEdit = (meter) => {
    setEditingMeter(meter);
    setOpen(true);
  };

  const handleClose = () => {
    setEditingMeter(null);
    setOpen(false);
  };

  const filteredMeters = meters.filter((meter) =>
    meter.meter_code.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <div className="page-header">
        <div className="page-title">
          <h1>Smart Meters</h1>
          <p>Manage all smart meters in your grid.</p>
        </div>

        <button
          className="primary-btn"
          onClick={() => {
            setEditingMeter(null);
            setOpen(true);
          }}
        >
          + Add Smart Meter
        </button>
      </div>

      <div className="table-toolbar">
        <input
          className="search-box"
          type="text"
          placeholder="🔍 Search Meter..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <MeterTable
        meters={filteredMeters}
        zones={zones}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      {open && (
        <MeterForm
          meter={editingMeter}
          zones={zones}
          onSubmit={handleSubmit}
          onClose={handleClose}
        />
      )}
    </>
  );
}

export default Meters;