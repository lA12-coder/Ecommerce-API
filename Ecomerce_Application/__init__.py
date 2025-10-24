"""Application package init.

Provide a fallback so that Django can use PyMySQL when the
`MySQLdb` C extension (mysqlclient) is not available on the host.

This is a safe, best-effort fallback: if PyMySQL is installed it will
be registered as the MySQLdb interface. If neither is available the
ImportError will be left to Django when it tries to load the DB backend.
"""
try:
    # Prefer the native MySQLdb if present
    import MySQLdb  # noqa: F401
except ImportError:
    # Fall back to PyMySQL (pure-Python) if available
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except Exception:
        # If PyMySQL isn't installed either, do nothing. Django will raise
        # the original error when it attempts to import the DB backend.
        pass

# Keep this file minimal — other startup behavior (celery app import,
# etc.) should go in other modules so failures are explicit and easy to
# control in different environments.
