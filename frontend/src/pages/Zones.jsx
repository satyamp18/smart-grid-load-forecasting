import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import "../assets/styles/zones.css";

import ZoneForm from "../components/ZoneForm";
import ZoneTable from "../components/ZoneTable";

import {
  getZones,
  createZone,
  updateZone,
  deleteZone,
} from "../services/zoneService";

function Zones() {
  const [zones, setZones] = useState([]);
  const [selectedZone, setSelectedZone] = useState(null);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const loadZones = async () => {
    try {
      const data = await getZones();
      setZones(data);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load zones");
    }
  };

  useEffect(() => {
    loadZones();
  }, []);

  const handleSubmit = async (zoneData) => {
    try {
      if (selectedZone) {
        await updateZone(selectedZone.id, zoneData);
        toast.success("Zone Updated Successfully");
      } else {
        await createZone(zoneData);
        toast.success("Zone Added Successfully");
      }

      setSelectedZone(null);
      setOpen(false);
      loadZones();
    } catch (error) {
      console.error(error);
      toast.error("Operation Failed");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this zone?")) return;

    try {
      await deleteZone(id);
      toast.success("Zone Deleted Successfully");
      loadZones();
    } catch (error) {
      console.error(error);
      toast.error("Delete Failed");
    }
  };

  const handleEdit = (zone) => {
    setSelectedZone(zone);
    setOpen(true);
  };

  const handleClose = () => {
    setSelectedZone(null);
    setOpen(false);
  };

  const filteredZones = zones.filter((zone) =>
    zone.zone_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <div className="page-header">
        <div className="page-title">
          <h1>Grid Zones</h1>
          <p>Manage all smart grid zones.</p>
        </div>

        <button
          className="primary-btn"
          onClick={() => {
            setSelectedZone(null);
            setOpen(true);
          }}
        >
          + Add Zone
        </button>
      </div>

      <div className="table-toolbar">
        <input
          className="search-box"
          type="text"
          placeholder="🔍 Search Zone..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <ZoneTable
        zones={filteredZones}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      {open && (
        <ZoneForm
          selectedZone={selectedZone}
          onSubmit={handleSubmit}
          onCancel={handleClose}
        />
      )}
    </>
  );
}

export default Zones;