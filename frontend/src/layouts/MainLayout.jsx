import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import "../assets/styles/layout.css";

function MainLayout() {
    return (
        <div className="app-layout">

            <Sidebar />

            <section className="main-content">

                <Navbar />

                <main className="page-content">
                    <Outlet />
                </main>

            </section>

        </div>
    );
}

export default MainLayout;