from app.db.engine import engine


def get_db_version():
    with engine.connect() as conn:
        result = conn.exec_driver_sql("SELECT version();")
        return result.fetchone()[0]