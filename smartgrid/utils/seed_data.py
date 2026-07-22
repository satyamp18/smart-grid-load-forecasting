from datetime import datetime, timedelta
import random

from smartgrid.db.session import SessionLocal

from smartgrid.models.zone import Zone
from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading
from smartgrid.models.alert import Alert
from smartgrid.models.load_report import LoadReport

db = SessionLocal()

try:
    print("Creating Zones...")

    zones = [
        Zone(zone_name="North Grid", max_capacity_kw=500),
        Zone(zone_name="South Grid", max_capacity_kw=650),
        Zone(zone_name="East Grid", max_capacity_kw=800),
    ]

    db.add_all(zones)
    db.commit()

    zones = db.query(Zone).all()

    print("Creating Smart Meters...")

    meters = []

    meter_no = 1

    for zone in zones:
        for _ in range(3):
            meters.append(
                SmartMeter(
                    meter_code=f"MTR{meter_no:03}",
                    zone_id=zone.id
                )
            )
            meter_no += 1

    db.add_all(meters)
    db.commit()

    meters = db.query(SmartMeter).all()

    print("Creating Meter Readings...")

    readings = []

    for meter in meters:
        for i in range(30):
            voltage = round(random.uniform(220, 240), 2)
            current = round(random.uniform(5, 25), 2)
            power = round(voltage * current / 1000, 2)

            readings.append(
                MeterReading(
                    meter_id=meter.id,
                    voltage=voltage,
                    current=current,
                    power_kw=power,
                    timestamp=datetime.now() - timedelta(minutes=i * 10)
                )
            )

    db.add_all(readings)
    db.commit()

    print("Creating Alerts...")

    messages = [
        "High Load",
        "Voltage Drop",
        "Power Surge",
        "Meter Offline",
        "Communication Failure"
    ]

    severities = ["LOW", "MEDIUM", "HIGH"]

    alerts = []

    for _ in range(20):
        zone = random.choice(zones)

        alerts.append(
            Alert(
                zone_id=zone.id,
                message=random.choice(messages),
                severity=random.choice(severities),
                created_at=datetime.now()
            )
        )

    db.add_all(alerts)
    db.commit()

    print("Creating Load Reports...")

    reports = []

    for zone in zones:
        for i in range(10):
            reports.append(
                LoadReport(
                    zone_id=zone.id,
                    total_load_kw=round(random.uniform(150, 450), 2),
                    report_time=datetime.now() - timedelta(hours=i)
                )
            )

    db.add_all(reports)
    db.commit()

    print("\n========== DATABASE SEEDED ==========")
    print("Zones         :", db.query(Zone).count())
    print("Meters        :", db.query(SmartMeter).count())
    print("Readings      :", db.query(MeterReading).count())
    print("Alerts        :", db.query(Alert).count())
    print("Load Reports  :", db.query(LoadReport).count())
    print("=====================================")

finally:
    db.close()