function ReadingTable({
  readings,
  loading,
  onEdit,
  onDelete,
}) {
  if (loading) {
    return (
      <div className="loading">
        Loading readings...
      </div>
    );
  }

  if (readings.length === 0) {
    return (
      <div className="empty-state">
        No readings found.
      </div>
    );
  }

  return (
    <table className="data-table">

      <thead>

        <tr>
          <th>ID</th>
          <th>Meter</th>
          <th>Voltage</th>
          <th>Current</th>
          <th>Power</th>
          <th>Timestamp</th>
          <th>Actions</th>
        </tr>

      </thead>

      <tbody>

        {readings.map((reading) => (
          <tr key={reading.id}>

            <td>{reading.id}</td>

            <td>{reading.meter_id}</td>

            <td>{reading.voltage} V</td>

            <td>{reading.current} A</td>

            <td>{reading.power_kw.toFixed(2)} kW</td>

            <td>
              {new Date(
                reading.timestamp
              ).toLocaleString()}
            </td>

            <td>

              <button
                className="edit-btn"
                onClick={() =>
                  onEdit(reading)
                }
              >
                ✏ Edit
              </button>

              <button
                className="delete-btn"
                onClick={() =>
                  onDelete(reading.id)
                }
              >
                🗑 Delete
              </button>

            </td>

          </tr>
        ))}

      </tbody>

    </table>
  );
}

export default ReadingTable;