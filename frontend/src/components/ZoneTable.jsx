function ZoneTable({
  zones,
  onEdit,
  onDelete,
}) {
  return (
    <div className="table-card">

      <table className="data-table">

        <thead>
          <tr>
            <th>#</th>
            <th>Zone Name</th>
            <th>Capacity</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>

          {zones.length === 0 ? (

            <tr>
              <td
                colSpan="5"
                className="empty-row"
              >
                No Zones Found
              </td>
            </tr>

          ) : (

            zones.map((zone, index) => (

              <tr key={zone.id}>

                <td>{index + 1}</td>

                <td>
                  <strong>
                    {zone.zone_name}
                  </strong>
                </td>

                <td>
                  {zone.max_capacity_kw} KW
                </td>

                <td>
                  <span className="status active">
                    Active
                  </span>
                </td>

                <td>

                  <button
                    className="edit-btn"
                    onClick={() => onEdit(zone)}
                  >
                    ✏️ Edit
                  </button>

                  <button
                    className="delete-btn"
                    onClick={() => onDelete(zone.id)}
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

export default ZoneTable;