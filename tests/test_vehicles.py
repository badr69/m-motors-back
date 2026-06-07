import pytest
from app.modules.vehicles.model import Vehicle
from app.modules.vehicles.service import VehicleService


# ======================
# FIXTURE VEHICLE
# ======================
@pytest.fixture()
def test_vehicle(db_session):

    vehicle = Vehicle(
        brand="Toyota",
        model="Corolla",
        year=2020,
        mileage=50000,
        fuel_type="petrol",
        transmission="manual",
        price=15000,
        description="Test vehicle",
        image_url=None,
        category="SUV",
        vehicle_type="location",
        status="available"
    )

    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)

    return vehicle


# ======================
# CREATE VEHICLE
# ======================
def test_create_vehicle(db_session):

    data = {
        "brand": "BMW",
        "model": "X5",
        "year": 2022,
        "mileage": 10000,
        "fuel_type": "diesel",
        "transmission": "automatic",
        "price": 60000,
        "description": "Luxury SUV",
        "image_url": None,
        "category": "SUV",
        "vehicle_type": "location"
    }

    result = VehicleService.create_vehicle(db_session, data)

    assert result["error"] is None
    assert result["data"]["brand"] == "BMW"
    assert result["data"]["status"] == "available"


# ======================
# GET AVAILABLE VEHICLES
# ======================
def test_get_available_vehicles(db_session, test_vehicle):

    result = VehicleService.get_available_vehicles(db_session)

    assert result["error"] is None
    assert len(result["data"]) >= 1


# ======================
# GET AVAILABLE VEHICLES EMPTY CASE
# ======================
def test_get_available_vehicles_empty(db_session):

    # véhicule NON disponible
    v = Vehicle(
        brand="Test",
        model="Empty",
        year=2020,
        mileage=1000,
        fuel_type="petrol",
        transmission="manual",
        price=1000,
        description="empty",
        image_url=None,
        category="SUV",
        vehicle_type="location",
        status="rented"
    )

    db_session.add(v)
    db_session.commit()

    result = VehicleService.get_available_vehicles(db_session)

    assert result["error"] is None


# ======================
# UPDATE VEHICLE
# ======================
def test_update_vehicle(db_session, test_vehicle):

    result = VehicleService.update_vehicle(
        db_session,
        test_vehicle.id,
        {"price": 99999, "mileage": 12345}
    )

    assert result["error"] is None
    assert result["data"]["price"] == 99999


# ======================
# DELETE VEHICLE
# ======================
@staticmethod
def delete_vehicle(db, vehicle_id):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.is_deleted == False
    ).first()

    if not vehicle:
        return {"data": None, "error": "Vehicle not found"}

    vehicle.is_deleted = True

    db.commit()

    return {
        "data": {"message": "Vehicle deleted successfully"},
        "error": None
    }


# ======================
# DELETE VEHICLE TWICE (EDGE CASE)
# ======================
def test_delete_vehicle_twice(db_session, test_vehicle):

    result1 = VehicleService.delete_vehicle(db_session, test_vehicle.id)
    assert result1["error"] is None

    # IMPORTANT: flush session state
    db_session.expire_all()

    result2 = VehicleService.delete_vehicle(db_session, test_vehicle.id)

    assert result2["error"] == "Vehicle not found"


# ======================
# GET BY ID NOT FOUND
# ======================
def test_get_vehicle_not_found(db_session):

    result = VehicleService.get_vehicle_by_id(db_session, 999999)

    assert result["error"] == "Vehicle not found"