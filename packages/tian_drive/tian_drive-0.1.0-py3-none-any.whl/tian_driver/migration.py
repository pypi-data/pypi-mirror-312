import os
import socket
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from tian_core import singleton

logger = logging.getLogger(__name__)


check_schema_sql = """
    SELECT * 
    FROM information_schema.schemata 
    WHERE schema_name = 'tian_version' LIMIT 1;
"""

create_schema_sql = "CREATE SCHEMA IF NOT EXISTS tian_version;"
create_table_sql = """
    CREATE TABLE IF NOT EXISTS tian_version.db_version (
        version TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT current_timestamp,
        updated_at TIMESTAMP DEFAULT current_timestamp,
        updated_by VARCHAR(255) DEFAULT 'system',
        created_by VARCHAR(255) DEFAULT 'system',
        applied_at TIMESTAMPTZ DEFAULT now()
    );
"""

check_version_sql = "SELECT * FROM tian_version.db_version WHERE version = :version;"
insert_version_sql = """
    INSERT INTO tian_version.db_version 
    (version, created_by, updated_by)
    VALUES (:version, :created_by, :updated_by);
"""

@singleton
class DatabaseMigrator:
    def __init__(self, db_connection):
        # Print the database connection
        logger.warning(f"✅ CHECK SUCCESS: Database connection: {db_connection}")
        self.db_connection = db_connection

        # Ensure the db_version table exists
        self.ensure_schema_and_table()

    def ensure_schema_and_table(self):
        """Ensure the 'tian_version.db_version' table exists, create if not."""
        with self.db_connection.connect() as connection:
            trans = connection.begin()
            try:
                result = connection.execute(text(check_schema_sql)).fetchone()
                if result is None:
                    result = connection.execute(text(create_schema_sql))
                
                result = connection.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'tian_version' AND table_name = 'db_version');")).fetchone()
                if not result[0]:
                    connection.execute(text(create_table_sql))
                trans.commit()
            except SQLAlchemyError as e:
                trans.rollback()
                logger.error(f"Database error: {e}")
                raise e
            logger.warning(f"✅ CHECK SUCCESS: tian_version schema exists: {result}")

    def get_migration_directory(self) -> str:
        """Check if DATABASE_MIGRATION_DIR exists, ask user if empty."""
        migration_dir = os.getenv('DATABASE_MIGRATION_DIR')
        while not migration_dir:
            logger.warning("🚧 DATABASE_MIGRATION_DIR environment variable is not set.")
            migration_dir = input("✈  ✈   ✈  Please enter the migration directory path: ")
        logger.warning(f"✅ CHECK SUCCESS: DATABASE_MIGRATION_DIR: {migration_dir}")
        return migration_dir


    def run_migration(self) -> None:
        """Run the migration process if migration files exist."""
        migration_dir = self.get_migration_directory()
        migrations_dir_path = os.path.join(os.getcwd(), migration_dir)
        logger.warning(f"✅ CHECK SUCCESS: Migrations directory: {migrations_dir_path}")

        # Get migration files
        try:
            migration_files = sorted(os.listdir(migrations_dir_path))
        except FileNotFoundError:
            logger.error(f"Migration directory not found: {migrations_dir_path}")
            return

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            created_by = f"{hostname} ({ip_address})"
        except Exception as e:
            logger.error(f"Error getting hostname and ip address: {e}")
            created_by = 'system'
            
        with self.db_connection.connect() as connection:
            for migration_file in migration_files:
                if not migration_file.endswith(".sql"):
                    continue
                connection.begin()
                try:
                    result = connection.execute(text(check_version_sql), {'version': migration_file} ).fetchone()
                    if result is not None:
                        # convert to timestamp
                        logger.warning(f"❌ SKIP: Skipping already applied migration: {migration_file}: {result.applied_at}")
                        raise Exception(f"Migration {migration_file} already applied.")
                    with open(os.path.join(migrations_dir_path, migration_file), 'r', encoding='utf-8') as file:
                        migration_sql = file.read()
                        connection.execute(text(migration_sql))
                        connection.execute(text(insert_version_sql), {
                            'version': migration_file,
                            'created_by': created_by,
                            'updated_by': created_by
                        })
                        logger.warning(f"✅ DONE > Successfully applied migration: {migration_file}")
                        connection.commit()
                except Exception as e:
                    connection.rollback()
                    continue



        