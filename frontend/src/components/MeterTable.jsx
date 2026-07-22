function MeterTable({ meters, zones, onEdit, onDelete }) {

  const getZoneName = (id) => {
    const zone = zones.find((z) => z.id === id);
    return zone ? zone.zone_name : "-";
  };

  return (
    <div className="table-card">

      <table className="data-table">

        <thead>
          <tr>
            <th>#</th>
            <th>Meter Code</th>
            <th>Zone</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>

          {meters.length === 0 ? (

            <tr>
              <td colSpan="5" className="empty-row">
                No Smart Meters Found
              </td>
            </tr>

          ) : (

            meters.map((meter, index) => (

              <tr key={meter.id}>

                <td>{index + 1}</td>

                <td>
                  <strong>{meter.meter_code}</strong>
                </td>

                <td>{getZoneName(meter.zone_id)}</td>

                <td>
                  <span className="status active">
                    Active
                  </span>
                </td>

                <td>

                  <button
                    className="edit-btn"
                    onClick={() => onEdit(meter)}
                  >
                    ✏️ Edit
                  </button>

                  <button
                    className="delete-btn"
                    onClick={() => onDelete(meter.id)}
                  >
                    🗑 Delete
                  </button>

                </td>

              </tr>

            ))

          )}

        </tbody>

      </table>

    </div>
  );
}

export default MeterTable;