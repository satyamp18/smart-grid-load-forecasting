from datetime import datetime
from smartgrid.db.session import SessionLocal
from smartgrid.models.zone import Zone
from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading
from smartgrid.models.load_report import LoadReport
from smartgrid.models.alert import Alert

def seed():
    db = SessionLocal()
    try:
        db.query(Alert).delete()
        db.query(LoadReport).delete()
        db.query(MeterReading).delete()
        db.query(SmartMeter).delete()
        db.query(Zone).delete()
        db.commit()
        
        zone_a = Zone(zone_name="North Sector Zone A", max_capacity_kw=10.0)
        zone_b = Zone(zone_name="South Sector Zone B", max_capacity_kw=15.0)
        db.add_all([zone_a, zone_b])
        db.commit()
        db.refresh(zone_a)
        db.refresh(zone_b)
        
        meter_1 = SmartMeter(meter_code="MTR-001", zone_id=zone_a.id)
        meter_2 = SmartMeter(meter_code="MTR-002", zone_id=zone_b.id)
        db.add_all([meter_1, meter_2])
        db.commit()
        db.refresh(meter_1)
        db.refresh(meter_2)
        
        reading_1 = MeterReading(meter_id=meter_1.id, voltage=220.0, current=43.18, power_kw=9.5, timestamp=datetime.utcnow())
        reading_2 = MeterReading(meter_id=meter_2.id, voltage=220.0, current=22.73, power_kw=5.0, timestamp=datetime.utcnow())
        db.add_all([reading_1, reading_2])
        db.commit()
        
        print("✅ Database successfully seeded with 2 zones, 2 meters, and initial readings.")
    except Exception as e:
        print("❌ Seeding failed:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
