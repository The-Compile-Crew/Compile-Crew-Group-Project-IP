"""
Migration script to add new columns to the shortlist table.
Run this script once with your Flask app context.
"""

from App.database import db
from sqlalchemy import text
from App.main import create_app

def migrate_shortlist_table():
    app = create_app()
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                conn.execute(text("ALTER TABLE shortlist ADD COLUMN student_name VARCHAR(128) NOT NULL DEFAULT ''"))
            except Exception:
                pass  # Column may already exist
            try:
                conn.execute(text("ALTER TABLE shortlist ADD COLUMN student_identifier VARCHAR(32) NOT NULL DEFAULT ''"))
            except Exception:
                pass
            try:
                conn.execute(text("ALTER TABLE shortlist ADD COLUMN details TEXT NOT NULL DEFAULT ''"))
            except Exception:
                pass
    print("Migration completed.")

if __name__ == "__main__":
    migrate_shortlist_table()
