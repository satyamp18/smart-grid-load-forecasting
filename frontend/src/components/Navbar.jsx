import { FaBell, FaUserCircle } from "react-icons/fa";
import "../assets/styles/navbar.css";

function Navbar() {
    return (
        <header className="navbar">

            <div className="nav-left">
                <h2>⚡ Smart Grid Monitoring System</h2>
                <p>Real-time Monitoring Dashboard</p>
            </div>

            <div className="nav-right">

                <FaBell className="icon" />

                <div className="profile">
                    <FaUserCircle />
                    <span>Admin</span>
                </div>

            </div>

        </header>
    );
}

export default Navbar;