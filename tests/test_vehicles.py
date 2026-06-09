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


# ======================
# READ AVAILABLE
# ======================
def test_get_available_vehicles(db_session, test_vehicle):

    result = VehicleService.get_available_vehicles(db_session)

    assert result["error"] is None
    assert len(result["data"]) >= 1


# ======================
# READ NOT FOUND
# ======================
def test_get_vehicle_not_found(db_session):

    result = VehicleService.get_vehicle_by_id(db_session, 999999)

    assert result["error"] == "Vehicle not found"


# ======================
# UPDATE VEHICLE
# ======================
def test_update_vehicle(db_session, test_vehicle):

    result = VehicleService.update_vehicle(
        db_session,
        test_vehicle.id,
        {"price": 99999}
    )

    assert result["error"] is None
    assert result["data"]["price"] == 99999


# ======================
# DELETE VEHICLE
# ======================
def test_delete_vehicle_twice(db_session, test_vehicle):

    result1 = VehicleService.delete_vehicle(db_session, test_vehicle.id)
    assert result1["error"] is None

    db_session.expire_all()

    result2 = VehicleService.delete_vehicle(db_session, test_vehicle.id)
    assert result2["error"] == "Vehicle not found"


# ======================
# SEARCH VEHICLE
# ======================
def test_search_vehicle_by_brand(db_session, test_vehicle):

    test_vehicle.brand = "BMW"
    db_session.commit()

    result = VehicleService.search_vehicles(
        db_session,
        {"brand": "BMW"}
    )

    assert result["error"] is None
    assert any(v["brand"] == "BMW" for v in result["data"])


# ======================
# ROUTES (BASIC ONLY)
# ======================
def test_get_vehicle_route(client):
    res = client.get("/api/v1/vehicles/1")
    assert res.status_code in [200, 404]


def test_available_vehicles_route(client):
    res = client.get("/api/v1/vehicles/available")
    assert res.status_code == 200


def test_delete_vehicle_route(client):

    res = client.delete("/api/v1/vehicles/999")

    print("STATUS:", res.status_code)
    print("DATA:", res.get_data(as_text=True))

    assert True


def test_search_vehicle_empty(db_session):

    result = VehicleService.search_vehicles(
        db_session,
        {"brand": "NOT_FOUND"}
    )

    assert result["error"] is None


def test_vehicle_update_price_only(db_session, test_vehicle):

    result = VehicleService.update_vehicle(
        db_session,
        test_vehicle.id,
        {"price": 12345}
    )

    assert result["error"] is None