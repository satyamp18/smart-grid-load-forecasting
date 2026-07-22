function DeleteModal({ open, title, message, onConfirm, onCancel }) {
  if (!open) return null;

  return (
    <div className="modal-overlay">
      <div className="delete-modal">

        <div className="delete-icon">
          🗑
        </div>

        <h2>{title}</h2>

        <p>{message}</p>

        <div className="modal-actions">

          <button
            className="cancel-btn"
            onClick={onCancel}
          >
            Cancel
          </button>

          <button
            className="delete-btn"
            onClick={onConfirm}
          >
            Delete
          </button>

        </div>

      </div>
    </div>
  );
}

export default DeleteModal;