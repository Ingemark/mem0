import os
from argparse import ArgumentParser
from pathlib import Path
import sys

from alembic import command
from alembic.config import Config

# Add the parent directory 'openmemory/api' to the Python path
# This is necessary so that alembic's env.py can find the 'app' module
api_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(api_dir))


def run_migrations(revision: str = 'head'):
    """Runs the database migrations."""
    # The alembic.ini file is in the parent directory of this script
    alembic_ini_path = api_dir / 'alembic.ini'
    alembic_cfg = Config(str(alembic_ini_path))

    # The script location is the directory containing this script
    script_location = Path(__file__).parent.resolve()
    alembic_cfg.set_main_option('script_location', str(script_location))

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    print(f"Running database migrations to revision: {revision}...")
    # Set the sqlalchemy.url in the config
    alembic_cfg.set_main_option('sqlalchemy.url', database_url)

    # Run the upgrade command
    command.upgrade(alembic_cfg, revision)
    print("Database migrations completed successfully.")


if __name__ == '__main__':
    parser = ArgumentParser(description="Run database migrations for OpenMemory.")
    parser.add_argument(
        '-r', '--revision',
        default='head',
        help="The revision to upgrade to. Defaults to 'head'."
    )
    args = parser.parse_args()
    run_migrations(revision=args.revision)
