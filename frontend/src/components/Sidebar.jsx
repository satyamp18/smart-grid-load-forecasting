import { NavLink } from "react-router-dom";
import {
    FaTachometerAlt,
    FaMapMarkedAlt,
    FaBolt,
    FaDatabase,
    FaChartLine,
    FaFileAlt,
    FaExclamationTriangle
} from "react-icons/fa";

import "../assets/styles/sidebar.css";

function Sidebar() {

    return (

        <aside className="sidebar">

            <div className="logo">

                ⚡ Smart Grid

            </div>

            <nav>

                <NavLink to="/">
                    <FaTachometerAlt />
                    <span>Dashboard</span>
                </NavLink>

                <NavLink to="/zones">
                    <FaMapMarkedAlt />
                    <span>Zones</span>
                </NavLink>

                <NavLink to="/meters">
                    <FaBolt />
                    <span>Smart Meters</span>
                </NavLink>

                <NavLink to="/readings">
                    <FaDatabase />
                    <span>Readings</span>
                </NavLink>

                <NavLink to="/analytics">
                    <FaChartLine />
                    <span>Analytics</span>
                </NavLink>

                <NavLink to="/reports">
                    <FaFileAlt />
                    <span>Reports</span>
                </NavLink>
                
                <NavLink to="/alerts">
                    <FaExclamationTriangle />
                    <span>Alerts</span>
                </NavLink>

            </nav>

        </aside>

    );

}

export default Sidebar;