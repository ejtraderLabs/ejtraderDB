from .exceptions import Empty, Full  


try:
    from .dict import DictSQLite  #noqa
    from .sqlqueue import SQLiteQueue, FIFOSQLiteQueue, FILOSQLiteQueue, UniqueQ  # noqa
    
except ImportError:
    import logging

    log = logging.getLogger(__name__)
    log.info("No sqlite3 module found, sqlite3 based queues are not available")

__all__ = ["DictSQLite", "SQLiteQueue", "FIFOSQLiteQueue","FILOSQLiteQueue", "UniqueQ", "Empty", "Full"]
