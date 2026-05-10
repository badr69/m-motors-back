from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

from app.core.db import Base
from app.core.config import Config

# Alembic Config object
config = context.config

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------
# 🔥 IMPORT DES MODELS (IMPORTANT POUR AUTOGENERATE)
# ---------------------------------------------------
from app.modules.users.model import User
from app.modules.roles.model import Role
from app.modules.vehicles.model import Vehicle
from app.modules.rental_dossiers.model import RentalDossier
from app.modules.documents.model import Document

# Metadata utilisée par Alembic
target_metadata = Base.metadata

# -------------------------
# OFFLINE MODE
# -------------------------
def run_migrations_offline() -> None:
    url = Config.SQLALCHEMY_DATABASE_URI

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------
# ONLINE MODE
# -------------------------
def run_migrations_online() -> None:
    connectable = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------
# RUN
# -------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()