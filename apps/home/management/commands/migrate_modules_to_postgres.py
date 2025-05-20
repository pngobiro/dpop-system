from django.core.management.base import BaseCommand
import sqlite3
import psycopg2
from django.conf import settings

class Command(BaseCommand):
    help = 'Migrate modules from SQLite to PostgreSQL'

    def handle(self, *args, **kwargs):
        self.stdout.write('Migrating modules from SQLite to PostgreSQL...')

        # Connect to SQLite
        sqlite_conn = sqlite3.connect('db.sqlite3')
        sqlite_cursor = sqlite_conn.cursor()

        # Get modules from SQLite
        sqlite_cursor.execute("SELECT * FROM home_module")
        modules = sqlite_cursor.fetchall()

        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        pg_cursor = pg_conn.cursor()

        # Insert each module into PostgreSQL
        for module in modules:
            try:
                # Assuming columns are: id, name, description, icon_class, url_name, permission_codename
                pg_cursor.execute("""
                    INSERT INTO home_module (name, description, icon_class, url_name, permission_codename)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """, (module[1], module[2], module[3], module[4], module[5]))
                
                self.stdout.write(f"Migrated module: {module[1]}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error migrating module {module[1]}: {str(e)}"))

        # Commit and close connections
        pg_conn.commit()
        pg_cursor.close()
        pg_conn.close()
        sqlite_cursor.close()
        sqlite_conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully migrated modules to PostgreSQL'))