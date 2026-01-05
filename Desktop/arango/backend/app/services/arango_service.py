"""
ArangoDB connection and database service
"""
from arango import ArangoClient
from arango.database import StandardDatabase
from arango.exceptions import ArangoServerError
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class ArangoService:
    """Service for managing ArangoDB connections and operations"""
    
    def __init__(self):
        self.client: ArangoClient = None
        self.db: StandardDatabase = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to ArangoDB"""
        try:
            settings.validate()
            self.client = ArangoClient(hosts=settings.ARANGO_HOST)
            self.db = self.client.db(
                settings.ARANGO_DB,
                username=settings.ARANGO_USER,
                password=settings.ARANGO_PASSWORD
            )
            logger.info(f"Connected to ArangoDB: {settings.ARANGO_DB}")
        except Exception as e:
            logger.error(f"Failed to connect to ArangoDB: {e}")
            raise
    
    def get_database(self) -> StandardDatabase:
        """Get the database instance"""
        if self.db is None:
            self._connect()
        return self.db
    
    def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            if self.db is None:
                return False
            # Simple query to verify connection
            self.db.aql.execute("RETURN 1")
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def execute_query(self, query: str, bind_vars: dict = None) -> list:
        """Execute an AQL query and return results"""
        try:
            cursor = self.db.aql.execute(query, bind_vars=bind_vars or {})
            return list(cursor)
        except ArangoServerError as e:
            logger.error(f"AQL query error: {e}")
            raise
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise


# Global service instance
arango_service = ArangoService()

