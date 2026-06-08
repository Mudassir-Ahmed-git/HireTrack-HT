from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os
import sys

# ─── 1. Make sure Python can find your app folder ───────────────────────────
# This adds the backend/ folder to Python's search path.
# Without this, "from app.models import Base" would fail with ModuleNotFoundError.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─── 2. Load your .env file ──────────────────────────────────────────────────
# Reads DATABASE_URL and other variables from your .env file.
load_dotenv()

# ─── 3. Import your models ───────────────────────────────────────────────────
# This is the critical import. Alembic reads Base.metadata to know
# what tables exist. If you add new models later, import them here too.
from app.database import Base
from app.models import User          # import every model you write

# ─── 4. Alembic config object ────────────────────────────────────────────────
config = context.config

# Sets up Python logging from the alembic.ini [loggers] section.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─── 5. Point Alembic at your metadata ───────────────────────────────────────
# This is what tells Alembic which tables to track.
# When you run --autogenerate, it compares this metadata against
# the actual database and generates the difference as a migration.
target_metadata = Base.metadata

# ─── 6. Read database URL from environment ───────────────────────────────────
# Overrides the sqlalchemy.url in alembic.ini with your .env value.
def get_url():
    return os.getenv("DATABASE_URL")


# ─── 7. Offline mode (runs migrations without a live DB connection) ───────────
def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# ─── 8. Online mode (runs migrations with a live DB connection) ───────────────
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# ─── 9. Run whichever mode Alembic decides ───────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()