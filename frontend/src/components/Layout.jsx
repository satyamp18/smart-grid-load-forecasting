import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import "../assets/styles/globals.css";

function Layout() {
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

export default Layout;