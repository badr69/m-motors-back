import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

from app.core.db import Base
from app.core.config import Config

# 🔹 IMPORT TES MODELS (important pour autogenerate)
from app.modules.users.model import User
from app.modules.roles.model import Role


# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔹 Metadata SQLAlchemy
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
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------
# ONLINE MODE (PRO PRETTY CLEAN)
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
            compare_type=True,  # 🔥 détecte changements de types
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