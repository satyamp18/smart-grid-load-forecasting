function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}) {
  if (totalPages <= 1) return null;

  return (
    <div className="pagination">

      <button
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        Previous
      </button>

      {Array.from({ length: totalPages }, (_, i) => (

        <button
          key={i}
          className={
            currentPage === i + 1
              ? "active-page"
              : ""
          }
          onClick={() => onPageChange(i + 1)}
        >
          {i + 1}
        </button>

      ))}

      <button
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        Next
      </button>

    </div>
  );
}

export default Pagination;