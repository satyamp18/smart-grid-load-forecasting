import "./../assets/styles/cards.css";

function DashboardCard({ title, value, icon, color }) {
    return (
        <div className="dashboard-card">

            <div className="card-left">

                <h4>{title}</h4>

                <h2>{value}</h2>

            </div>

            <div
                className="card-icon"
                style={{ background: color }}
            >
                {icon}
            </div>

        </div>
    );
}

export default DashboardCard;