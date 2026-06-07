from app.modules.vehicles.model import Vehicle
from app.core.logger import setup_logger

logger = setup_logger("vehicle-service")


class VehicleService:

    # =====================
    # CREATE VEHICLE
    # =====================
    @staticmethod
    def create_vehicle(db, data):

        logger.info(
            f"Creating vehicle: {data.get('brand')} {data.get('model')}"
        )

        vehicle = Vehicle(
            brand=data.get("brand"),
            model=data.get("model"),
            year=data.get("year"),
            mileage=data.get("mileage"),
            fuel_type=data.get("fuel_type"),
            transmission=data.get("transmission"),
            price=data.get("price"),
            description=data.get("description"),
            image_url=data.get("image_url"),
            category=data.get("category"),
            vehicle_type=data.get("vehicle_type"),
            status="available"
        )

        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)

        logger.info(f"Vehicle created successfully: {vehicle.id}")

        return {
            "data": {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "mileage": vehicle.mileage,
                "fuel_type": vehicle.fuel_type,
                "transmission": vehicle.transmission,
                "price": float(vehicle.price) if vehicle.price else None,
                "description": vehicle.description,
                "image_url": vehicle.image_url,
                "category": vehicle.category,
                "vehicle_type": vehicle.vehicle_type,
                "status": vehicle.status,
            },
            "error": None
        }

    # =====================
    # GET ALL VEHICLES
    # =====================
    @staticmethod
    def get_vehicles(db):

        vehicles = db.query(Vehicle).filter(
            Vehicle.is_deleted == False
        ).all()

        return {
            "data": [
                {
                    "id": v.id,
                    "brand": v.brand,
                    "model": v.model,
                    "year": v.year,
                    "mileage": v.mileage,
                    "fuel_type": v.fuel_type,
                    "transmission": v.transmission,
                    "price": float(v.price) if v.price else None,
                    "description": v.description,
                    "image_url": v.image_url,
                    "category": v.category,
                    "vehicle_type": v.vehicle_type,
                    "status": v.status,
                }
                for v in vehicles
            ],
            "error": None
        }

    # =====================
    # GET VEHICLE BY ID
    # =====================
    @staticmethod
    def get_vehicle_by_id(db, vehicle_id):

        vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.is_deleted == False
        ).first()

        if not vehicle:
            return {
                "data": None,
                "error": "Vehicle not found"
            }

        return {
            "data": {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "mileage": vehicle.mileage,
                "fuel_type": vehicle.fuel_type,
                "transmission": vehicle.transmission,
                "price": float(vehicle.price) if vehicle.price else None,
                "description": vehicle.description,
                "image_url": vehicle.image_url,
                "category": vehicle.category,
                "vehicle_type": vehicle.vehicle_type,
                "status": vehicle.status,
            },
            "error": None
        }

    # =====================
    # UPDATE VEHICLE
    # =====================
    @staticmethod
    def update_vehicle(db, vehicle_id, data):

        vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id
        ).first()

        if not vehicle:
            return {
                "data": None,
                "error": "Vehicle not found"
            }

        for field in [
            "brand",
            "model",
            "year",
            "mileage",
            "fuel_type",
            "transmission",
            "price",
            "description",
            "image_url",
            "category",
            "vehicle_type",
            "status"
        ]:
            if field in data:
                setattr(vehicle, field, data[field])

        db.commit()
        db.refresh(vehicle)

        logger.info(f"Vehicle updated successfully: {vehicle.id}")

        return {
            "data": {
                "id": vehicle.id,
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "mileage": vehicle.mileage,
                "fuel_type": vehicle.fuel_type,
                "transmission": vehicle.transmission,
                "price": float(vehicle.price) if vehicle.price else None,
                "description": vehicle.description,
                "image_url": vehicle.image_url,
                "category": vehicle.category,
                "vehicle_type": vehicle.vehicle_type,
                "status": vehicle.status,
            },
            "error": None
        }

    # =====================
    # DELETE VEHICLE (US-09)
    # =====================
    @staticmethod
    def delete_vehicle(db, vehicle_id):

        vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.is_deleted == False
        ).first()

        if not vehicle:
            return {
                "data": None,
                "error": "Vehicle not found"
            }

        vehicle.is_deleted = True

        db.commit()

        logger.info(f"Vehicle deleted successfully: {vehicle.id}")

        return {
            "data": {
                "message": "Vehicle deleted successfully"
            },
            "error": None
        }
    # @staticmethod
    # def delete_vehicle(db, vehicle_id):
    #
    #     vehicle = db.query(Vehicle).filter(
    #         Vehicle.id == vehicle_id
    #     ).first()
    #
    #     if not vehicle:
    #         return {
    #             "data": None,
    #             "error": "Vehicle not found"
    #         }
    #
    #     # soft delete
    #     vehicle.is_deleted = True
    #
    #     db.commit()
    #
    #     logger.info(f"Vehicle deleted successfully: {vehicle.id}")
    #
    #     return {
    #         "data": {
    #             "message": "Vehicle deleted successfully"
    #         },
    #         "error": None
    #     }

    # =====================
    # GET AVAILABLE VEHICLES
    # =====================
    @staticmethod
    def get_available_vehicles(db, vehicle_type=None):

        query = db.query(Vehicle).filter(
            Vehicle.is_deleted == False,
            Vehicle.status == "available"
        )

        # location / achat
        if vehicle_type:
            query = query.filter(
                Vehicle.vehicle_type == vehicle_type
            )

        vehicles = query.all()

        return {
            "data": [
                {
                    "id": v.id,
                    "brand": v.brand,
                    "model": v.model,
                    "year": v.year,
                    "mileage": v.mileage,
                    "fuel_type": v.fuel_type,
                    "transmission": v.transmission,
                    "price": float(v.price) if v.price else None,
                    "description": v.description,
                    "image_url": v.image_url,
                    "category": v.category,
                    "vehicle_type": v.vehicle_type,
                    "status": v.status,
                }
                for v in vehicles
            ],
            "error": None
        }

    # =====================
    # SEARCH VEHICLES
    # =====================
    @staticmethod
    def search_vehicles(db, filters):

        query = db.query(Vehicle).filter(
            Vehicle.is_deleted == False,
            Vehicle.status == "available"
        )

        # =====================
        # FILTERS
        # =====================

        if filters.get("vehicle_type"):
            query = query.filter(
                Vehicle.vehicle_type == filters["vehicle_type"]
            )

        if filters.get("category"):
            query = query.filter(
                Vehicle.category == filters["category"]
            )

        if filters.get("brand"):
            query = query.filter(
                Vehicle.brand.ilike(f"%{filters['brand']}%")
            )

        if filters.get("max_price"):
            query = query.filter(
                Vehicle.price <= float(filters["max_price"])
            )

        if filters.get("max_mileage"):
            query = query.filter(
                Vehicle.mileage <= int(filters["max_mileage"])
            )

        # =====================
        # SORTING
        # =====================

        sort = filters.get("sort")

        if sort == "price_asc":
            query = query.order_by(
                Vehicle.price.asc()
            )

        elif sort == "price_desc":
            query = query.order_by(
                Vehicle.price.desc()
            )

        elif sort == "year_desc":
            query = query.order_by(
                Vehicle.year.desc()
            )

        elif sort == "mileage_asc":
            query = query.order_by(
                Vehicle.mileage.asc()
            )

        # =====================
        # PAGINATION
        # =====================

        page = int(filters.get("page", 1))
        limit = int(filters.get("limit", 10))

        offset = (page - 1) * limit

        total = query.count()

        vehicles = query.offset(offset).limit(limit).all()

        return {
            "data": [
                {
                    "id": v.id,
                    "brand": v.brand,
                    "model": v.model,
                    "year": v.year,
                    "mileage": v.mileage,
                    "fuel_type": v.fuel_type,
                    "transmission": v.transmission,
                    "price": float(v.price) if v.price else None,
                    "description": v.description,
                    "image_url": v.image_url,
                    "category": v.category,
                    "vehicle_type": v.vehicle_type,
                    "status": v.status,
                }
                for v in vehicles
            ],

            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (
                    total // limit
                ) + (
                    1 if total % limit else 0
                )
            },

            "error": None
        }