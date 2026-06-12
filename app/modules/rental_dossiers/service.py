from app.modules.rental_dossiers.model import RentalDossier
from app.modules.vehicles.model import Vehicle
from app.core.logger import setup_logger


logger = setup_logger("rental-dossier-service")
allowed_status = ["approved", "rejected"]


class RentalDossierService:

    # =====================
    # CREATE DOSSIER (US-12)
    # =====================
    @staticmethod
    def create_dossier(db, user_id, data):

        logger.info(f"Creating rental dossier for user: {user_id}")

        vehicle_id = data.get("vehicle_id")
        message = data.get("message")

        # =====================
        # CHECK VEHICLE
        # =====================
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == vehicle_id,
            Vehicle.is_deleted == False
        ).first()

        if not vehicle:
            return {
                "data": None,
                "error": "Vehicle not found"
            }

        if vehicle.status != "available":
            return {
                "data": None,
                "error": "Vehicle not available"
            }

        # =====================
        # CREATE DOSSIER
        # =====================
        dossier = RentalDossier(
            user_id=user_id,
            vehicle_id=vehicle_id,
            status="pending",
            message=message
        )

        db.add(dossier)
        db.commit()
        db.refresh(dossier)

        logger.info(f"Rental dossier created successfully: {dossier.id}")

        return {
            "data": {
                "id": dossier.id,
                "user_id": dossier.user_id,
                "vehicle_id": dossier.vehicle_id,
                "status": dossier.status,
                "message": dossier.message,
                "created_at": dossier.created_at
            },
            "error": None
        }

    # =====================
    # GET MY DOSSIERS
    # =====================
    @staticmethod
    def get_my_dossiers(db, user_id):

        dossiers = db.query(RentalDossier).filter(
            RentalDossier.user_id == user_id
        ).all()

        return {
            "data": [
                {
                    "id": d.id,
                    "status": d.status,
                    "message": d.message,
                    "created_at": d.created_at,

                    # EPIC 6 FRONT REQUIREMENT
                    "vehicle": {
                        "id": d.vehicle.id,
                        "brand": d.vehicle.brand,
                        "model": d.vehicle.model
                    } if d.vehicle else None,

                    "documents": [
                        {
                            "id": doc.id,
                            "filename": doc.filename
                        }
                        for doc in d.documents
                    ]
                }
                for d in dossiers
            ],
            "error": None
        }


    # =====================
    # GET ALL DOSSIERS (ADMIN)
    # =====================
    @staticmethod
    def get_dossiers(db, status=None, sort="desc"):

        from app.modules.rental_dossiers.model import RentalDossier

        query = db.query(RentalDossier)

        # =====================
        # FILTER: STATUS ONLY (MVP)
        # =====================
        if status:
            query = query.filter(RentalDossier.status == status)

        # =====================
        # SORT
        # =====================
        if sort == "asc":
            query = query.order_by(RentalDossier.created_at.asc())
        else:
            query = query.order_by(RentalDossier.created_at.desc())

        dossiers = query.all()

        return {
            "data": [
                {
                    "id": d.id,

                    # CLIENT INFO (US-15 requirement)
                    "client": {
                        "id": d.user.id if d.user else None,
                        "name": getattr(d.user, "name", None),
                        "email": getattr(d.user, "email", None)
                    },

                    "status": d.status,
                    "message": d.message,
                    "created_at": d.created_at,

                    "vehicle": {
                        "id": d.vehicle.id,
                        "brand": d.vehicle.brand,
                        "model": d.vehicle.model
                    } if d.vehicle else None,

                    "documents": [
                        {
                            "id": doc.id,
                            "filename": doc.filename
                        }
                        for doc in d.documents
                    ]
                }
                for d in dossiers
            ],
            "error": None
        }
    # =====================
    # GET BY ID
    # =====================
    @staticmethod
    def get_dossier_by_id(db, dossier_id, user_id=None, is_admin=False):

        dossier = db.query(RentalDossier).filter(
            RentalDossier.id == dossier_id
        ).first()

        if not dossier:
            return {
                "data": None,
                "error": "Dossier not found"
            }

        # =====================
        # SECURITY CHECK
        # =====================
        if not is_admin and dossier.user_id != user_id:
            return {
                "data": None,
                "error": "Forbidden"
            }

        return {
            "data": {
                "id": dossier.id,
                "status": dossier.status,
                "message": dossier.message,
                "created_at": dossier.created_at,

                # EPIC 6 IMPORTANT
                "vehicle": {
                    "id": dossier.vehicle.id,
                    "brand": dossier.vehicle.brand,
                    "model": dossier.vehicle.model
                } if dossier.vehicle else None,

                "documents": [
                    {
                        "id": doc.id,
                        "filename": doc.filename,
                        "filepath": doc.filepath
                    }
                    for doc in dossier.documents
                ]
            },
            "error": None
        }


    # =====================
    # UPDATE STATUS (ADMIN)
    # =====================
    @staticmethod
    def update_status(db, dossier_id, data):

        logger.info(f"Updating dossier status: {dossier_id}")

        dossier = db.query(RentalDossier).filter(
            RentalDossier.id == dossier_id
        ).first()

        if not dossier:
            return {
                "data": None,
                "error": "Dossier not found"
            }

        new_status = data.get("status")

        allowed_status = [
            "pending",
            "approved",
            "rejected",
            "cancelled",
            "completed"
        ]

        if new_status not in allowed_status:
            return {
                "data": None,
                "error": "Invalid status"
            }

        # =====================
        # UPDATE STATUS
        # =====================
        dossier.status = new_status

        # =====================
        # VEHICLE LOGIC
        # =====================
        vehicle = db.query(Vehicle).filter(
            Vehicle.id == dossier.vehicle_id
        ).first()

        if vehicle:

            if new_status == "approved":
                vehicle.status = "rented"

            elif new_status in ["rejected", "cancelled"]:
                vehicle.status = "available"

        db.commit()
        db.refresh(dossier)

        logger.info(f"Dossier updated successfully: {dossier.id}")

        return {
            "data": {
                "id": dossier.id,
                "user_id": dossier.user_id,
                "vehicle_id": dossier.vehicle_id,
                "status": dossier.status,
                "message": dossier.message,
                "created_at": dossier.created_at
            },
            "error": None
        }

    # =====================
    # DELETE DOSSIER
    # =====================
    @staticmethod
    def delete_dossier(db, dossier_id, user_id=None, is_admin=False):

        logger.info(f"Deleting dossier: {dossier_id}")

        dossier = db.query(RentalDossier).filter(
            RentalDossier.id == dossier_id
        ).first()

        if not dossier:
            return {
                "data": None,
                "error": "Dossier not found"
            }

        # =====================
        # SECURITY RULES
        # =====================
        if not is_admin:

            if dossier.user_id != user_id:
                return {
                    "data": None,
                    "error": "Forbidden"
                }

            if dossier.status != "pending":
                return {
                    "data": None,
                    "error": "Cannot delete dossier"
                }

            if dossier.documents and len(dossier.documents) > 0:
                return {
                    "data": None,
                    "error": "Cannot delete dossier with documents"
                }

        db.delete(dossier)
        db.commit()

        logger.info(f"Dossier deleted successfully: {dossier.id}")

        return {
            "data": {
                "message": "Dossier deleted successfully"
            },
            "error": None
        }


