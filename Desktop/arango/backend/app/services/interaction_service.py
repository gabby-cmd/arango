"""
Service for drug interaction detection and analysis
"""
import time
from typing import List, Dict, Any
from app.services.arango_service import arango_service
from app.models.schemas import InteractionResponse
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class InteractionService:
    """Service for detecting and analyzing drug interactions"""
    
    def __init__(self):
        self.db = arango_service.get_database()
    
    def search_drugs(self, search_query: str, limit: int = None) -> List[Dict[str, Any]]:
        """
        Search for drugs by name (case-insensitive)
        
        Args:
            search_query: Search term
            limit: Maximum number of results
            
        Returns:
            List of drug documents
        """
        limit = limit or settings.DRUG_SEARCH_LIMIT
        
        query = """
        FOR drug IN drugs
            FILTER LOWER(drug.name) LIKE LOWER(CONCAT("%", @search_query, "%")) OR
                   LOWER(drug.generic_name) LIKE LOWER(CONCAT("%", @search_query, "%"))
            LIMIT @limit
            RETURN MERGE(drug, {_key: drug._key})
        """
        
        try:
            results = arango_service.execute_query(
                query,
                bind_vars={"search_query": search_query, "limit": limit}
            )
            return results
        except Exception as e:
            logger.error(f"Drug search failed: {e}")
            raise
    
    def check_interactions(self, drug_keys: List[str]) -> Dict[str, Any]:
        """
        Check for interactions between multiple drugs using the critical AQL query
        
        Args:
            drug_keys: List of drug _key values
            
        Returns:
            Dictionary with interactions_found, highest_severity, query_time_ms, and interactions
        """
        start_time = time.time()
        
        # Critical AQL query for interaction detection
        query = """
        LET drug_keys = @drug_keys
        
        // Get all compounds from selected drugs
        LET prescription_compounds = (
          FOR drug_key IN drug_keys
            FOR compound IN OUTBOUND CONCAT("drugs/", drug_key) drug_contains_compound
              RETURN DISTINCT compound
        )
        
        // Find all pairwise interactions
        FOR c1 IN prescription_compounds
          FOR c2 IN prescription_compounds
            FILTER c1._id < c2._id  // Avoid duplicates (A-B same as B-A)
            
            FOR interaction IN compound_interacts_with
              FILTER (interaction._from == c1._id AND interaction._to == c2._id) OR
                     (interaction._from == c2._id AND interaction._to == c1._id)
              
              // Get affected drug names
              LET affected_drugs = (
                FOR drug_key IN drug_keys
                  FOR compound IN OUTBOUND CONCAT("drugs/", drug_key) drug_contains_compound
                    FILTER compound._id == c1._id OR compound._id == c2._id
                    FOR drug IN INBOUND compound drug_contains_compound
                      FILTER drug._key == drug_key
                      RETURN DISTINCT drug.name
              )
              
              RETURN {
                compound_1: c1.name,
                compound_2: c2.name,
                affected_drugs: affected_drugs,
                severity: interaction.severity,
                interaction_type: interaction.interaction_type,
                description: interaction.description,
                mechanism: interaction.mechanism,
                clinical_management: interaction.clinical_management,
                evidence_level: interaction.evidence_level,
                onset: interaction.onset,
                documentation: interaction.documentation
              }
        """
        
        try:
            results = arango_service.execute_query(
                query,
                bind_vars={"drug_keys": drug_keys}
            )
            
            query_time_ms = (time.time() - start_time) * 1000
            
            # Determine highest severity
            severities = ["severe", "moderate", "minor"]
            highest_severity = None
            if results:
                result_severities = [r.get("severity") for r in results]
                for severity in severities:
                    if severity in result_severities:
                        highest_severity = severity
                        break
            
            # Convert to InteractionResponse models
            interactions = [InteractionResponse(**result) for result in results]
            
            return {
                "interactions_found": len(interactions),
                "highest_severity": highest_severity,
                "query_time_ms": round(query_time_ms, 2),
                "interactions": [interaction.model_dump() for interaction in interactions]
            }
        except Exception as e:
            logger.error(f"Interaction check failed: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary with total counts and breakdowns
        """
        try:
            # Get collection counts
            drugs_count = self.db.collection("drugs").count()
            compounds_count = self.db.collection("compounds").count()
            interactions_count = self.db.collection("compound_interacts_with").count()
            
            # Get interactions by severity
            severity_query = """
            FOR interaction IN compound_interacts_with
                COLLECT severity = interaction.severity WITH COUNT INTO count
                RETURN {severity, count}
            """
            
            severity_results = arango_service.execute_query(severity_query)
            interactions_by_severity = {
                result["severity"]: result["count"]
                for result in severity_results
            }
            
            return {
                "total_drugs": drugs_count,
                "total_compounds": compounds_count,
                "total_interactions": interactions_count,
                "interactions_by_severity": interactions_by_severity
            }
        except Exception as e:
            logger.error(f"Statistics retrieval failed: {e}")
            raise

