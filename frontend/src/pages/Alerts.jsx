import { useEffect, useMemo, useState } from "react";
import { toast } from "react-toastify";
import websocketService from "../services/websocketService";
import {
    getAllAlerts,
    deleteAlert,
    updateAlertStatus,
} from "../services/alertService";

import "../assets/styles/alerts.css";


const Alerts = () => {

    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    const [search, setSearch] = useState("");

    const [severityFilter, setSeverityFilter] =
        useState("ALL");

    const [statusFilter, setStatusFilter] =
        useState("ALL");



    // ------------------------
    // Load Alerts
    // ------------------------

    const loadAlerts = async () => {

        try {

            setLoading(true);

            const data = await getAllAlerts();

            setAlerts(data);

        }

        catch (error) {

            console.error(error);

            toast.error("Failed to load alerts");

        }

        finally {

            setLoading(false);

        }

    };



    useEffect(() => {

       loadAlerts();

       websocketService.connect();

       websocketService.subscribe(

           (message) => {

               if (

                   message.type ===

                   "NEW_ALERT"

               ) {

                   toast.info(

                     "⚠ New Alert Received"

                   );

                   loadAlerts();

               }

           }

       );

       return () => {

           websocketService.disconnect();

       };

    }, []);



    // ------------------------
    // Delete Alert
    // ------------------------

    const handleDelete = async (id) => {

        if (!window.confirm("Delete this alert?")) {

            return;

        }

        try {

            await deleteAlert(id);

            toast.success("Alert deleted");

            loadAlerts();

        }

        catch (error) {

            console.error(error);

            toast.error("Unable to delete alert");

        }

    };




    // ------------------------
    // Resolve Alert
    // ------------------------

    const handleResolve = async (id) => {

        try {

            await updateAlertStatus(

                id,

                "RESOLVED"

            );

            toast.success("Alert resolved");

            loadAlerts();

        }

        catch (error) {

            console.error(error);

            toast.error("Unable to update alert");

        }

    };





    // ------------------------
    // Filter
    // ------------------------

    const filteredAlerts = useMemo(() => {

        return alerts.filter((alert) => {

            const searchMatch =

                alert.message
                    .toLowerCase()
                    .includes(search.toLowerCase())

                ||

                String(alert.zone_id)
                    .includes(search);

            const severityMatch =

                severityFilter === "ALL"

                ||

                alert.severity === severityFilter;

            const statusMatch =

                statusFilter === "ALL"

                ||

                alert.status === statusFilter;

            return (

                searchMatch

                &&

                severityMatch

                &&

                statusMatch

            );

        });

    }, [

        alerts,

        search,

        severityFilter,

        statusFilter,

    ]);




    // ------------------------
    // Dashboard Cards
    // ------------------------

    const totalAlerts = alerts.length;

    const activeAlerts =

        alerts.filter(

            a => a.status === "ACTIVE"

        ).length;

    const resolvedAlerts =

        alerts.filter(

            a => a.status === "RESOLVED"

        ).length;

    const criticalAlerts =

        alerts.filter(

            a =>

            a.severity === "HIGH"

            ||

            a.severity === "CRITICAL"

        ).length;




    return (

        <div className="alerts-page">

            <div className="alerts-header">

                <div>

                    <h1>

                        Alert Management

                    </h1>

                    <p>

                        Monitor grid alerts in real time.

                    </p>

                </div>

                <button

                    className="refresh-btn"

                    onClick={loadAlerts}

                >

                    Refresh

                </button>

            </div>



            <div className="alert-cards">

                <div className="card">

                    <h3>Total Alerts</h3>

                    <h2>{totalAlerts}</h2>

                </div>

                <div className="card">

                    <h3>Critical</h3>

                    <h2>{criticalAlerts}</h2>

                </div>

                <div className="card">

                    <h3>Active</h3>

                    <h2>{activeAlerts}</h2>

                </div>

                <div className="card">

                    <h3>Resolved</h3>

                    <h2>{resolvedAlerts}</h2>

                </div>

            </div>



            <div className="toolbar">

                <input

                    type="text"

                    placeholder="Search alert..."

                    value={search}

                    onChange={(e) =>

                        setSearch(e.target.value)

                    }

                />



                <select

                    value={severityFilter}

                    onChange={(e) =>

                        setSeverityFilter(

                            e.target.value

                        )

                    }

                >

                    <option value="ALL">

                        All Severity

                    </option>

                    <option value="LOW">

                        LOW

                    </option>

                    <option value="MEDIUM">

                        MEDIUM

                    </option>

                    <option value="HIGH">

                        HIGH

                    </option>

                    <option value="CRITICAL">

                        CRITICAL

                    </option>

                </select>



                <select

                    value={statusFilter}

                    onChange={(e) =>

                        setStatusFilter(

                            e.target.value

                        )

                    }

                >

                    <option value="ALL">

                        All Status

                    </option>

                    <option value="ACTIVE">

                        ACTIVE

                    </option>

                    <option value="RESOLVED">

                        RESOLVED

                    </option>

                </select>

            </div>
                        {loading ? (

                <div className="loading">

                    <h2>Loading Alerts...</h2>

                </div>

            ) : filteredAlerts.length === 0 ? (

                <div className="empty-state">

                    <h2>No Alerts Found</h2>

                </div>

            ) : (

                <div className="table-container">

                    <table className="alerts-table">

                        <thead>

                            <tr>

                                <th>ID</th>

                                <th>Zone</th>

                                <th>Message</th>

                                <th>Severity</th>

                                <th>Status</th>

                                <th>Created</th>

                                <th>Actions</th>

                            </tr>

                        </thead>

                        <tbody>

                            {

                                filteredAlerts.map(

                                    (alert) => (

                                        <tr key={alert.id}>

                                            <td>

                                                {alert.id}

                                            </td>

                                            <td>

                                                Zone {alert.zone_id}

                                            </td>

                                            <td>

                                                {alert.message}

                                            </td>

                                            <td>

                                                <span

                                                    className={`severity ${alert.severity.toLowerCase()}`}

                                                >

                                                    {alert.severity}

                                                </span>

                                            </td>

                                            <td>

                                                <span

                                                    className={`status ${alert.status.toLowerCase()}`}

                                                >

                                                    {alert.status}

                                                </span>

                                            </td>

                                            <td>

                                                {

                                                    new Date(

                                                        alert.created_at

                                                    ).toLocaleString()

                                                }

                                            </td>

                                            <td>

                                                {

                                                    alert.status ===

                                                    "ACTIVE"

                                                    &&

                                                    (

                                                        <button

                                                            className="resolve-btn"

                                                            onClick={() =>

                                                                handleResolve(

                                                                    alert.id

                                                                )

                                                            }

                                                        >

                                                            Resolve

                                                        </button>

                                                    )

                                                }

                                                <button

                                                    className="delete-btn"

                                                    onClick={() =>

                                                        handleDelete(

                                                            alert.id

                                                        )

                                                    }

                                                >

                                                    Delete

                                                </button>

                                            </td>

                                        </tr>

                                    )

                                )

                            }

                        </tbody>

                    </table>

                </div>

            )}
                    </div>

    );

};

export default Alerts;