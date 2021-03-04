from .exceptions import Empty, Full  


try:
    from .dict import DictSQLite 
    
except ImportError:
    import logging

    log = logging.getLogger(__name__)
    log.info("No sqlite3 module found, sqlite3 based queues are not available")

__all__ = ["DictSQLite", "Empty", "Full",
           "__author__", "__license__", "__version__"]
