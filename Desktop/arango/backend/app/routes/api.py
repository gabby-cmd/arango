"""
API routes for drug interaction checking
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging
import time
import traceback

from app.models.schemas import (
    DrugResponse,
    CheckInteractionsRequest,
    CheckInteractionsResponse,
    HealthResponse,
    StatsResponse,
    ConditionWarningRequest
)
from app.services.interaction_service import InteractionService
from app.services.arango_service import arango_service
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
interaction_service = InteractionService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns API and database connection status
    """
    try:
        db_status = "connected" if arango_service.health_check() else "disconnected"
        return HealthResponse(status="healthy", database=db_status)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(status="unhealthy", database="error")


@router.get("/drugs", response_model=List[DrugResponse])
async def search_drugs(
    search: str = Query(..., min_length=1, description="Search query for drug name"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of results")
):
    """
    Search for drugs by name
    
    - **search**: Search term (case-insensitive, matches name or generic_name)
    - **limit**: Maximum number of results (1-50)
    """
    try:
        results = interaction_service.search_drugs(search, limit)
        # Convert to response models, ensuring _key is preserved
        drug_responses = []
        for drug in results:
            # Ensure _key is explicitly included - Pydantic v2 needs this
            drug_data = dict(drug)
            if "_key" not in drug_data:
                drug_data["_key"] = drug.get("_key") or drug.get("_id", "").split("/")[-1]
            # Use model_validate with explicit _key
            response = DrugResponse.model_validate(drug_data)
            drug_responses.append(response)
        return drug_responses
    except Exception as e:
        logger.error(f"Drug search error: {e}")
        raise HTTPException(status_code=500, detail=f"Drug search failed: {str(e)}")


@router.get("/drugs/{drug_key}", response_model=DrugResponse)
async def get_drug_by_key(drug_key: str):
    """
    Get a single drug by its _key
    
    - **drug_key**: The _key of the drug to retrieve
    """
    try:
        db = arango_service.get_database()
        drugs_collection = db.collection("drugs")
        
        if not drugs_collection.has(drug_key):
            raise HTTPException(status_code=404, detail=f"Drug not found: {drug_key}")
        
        drug = drugs_collection.get(drug_key)
        
        # Ensure _key is explicitly included
        drug_data = dict(drug)
        if "_key" not in drug_data:
            drug_data["_key"] = drug.get("_key") or drug.get("_id", "").split("/")[-1]
        
        # Use model_validate with explicit _key
        response = DrugResponse.model_validate(drug_data)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching drug {drug_key}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-interactions", response_model=CheckInteractionsResponse)
async def check_interactions(request: CheckInteractionsRequest):
    """
    Check for interactions between multiple drugs
    
    - **drug_keys**: List of drug _key values (minimum 2, maximum 20)
    
    Returns all pairwise interactions between the selected drugs with detailed information.
    """
    try:
        # Validate minimum drugs
        if len(request.drug_keys) < settings.MIN_DRUGS_FOR_CHECK:
            raise HTTPException(
                status_code=400,
                detail=f"At least {settings.MIN_DRUGS_FOR_CHECK} drugs required for interaction check"
            )
        
        # Validate maximum drugs
        if len(request.drug_keys) > settings.MAX_DRUGS_FOR_CHECK:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {settings.MAX_DRUGS_FOR_CHECK} drugs allowed for interaction check"
            )
        
        # Verify all drug keys exist
        db = arango_service.get_database()
        drugs_collection = db.collection("drugs")
        
        for drug_key in request.drug_keys:
            if not drugs_collection.has(drug_key):
                raise HTTPException(
                    status_code=400,
                    detail=f"Drug with key '{drug_key}' not found"
                )
        
        # Check interactions
        result = interaction_service.check_interactions(request.drug_keys)
        return CheckInteractionsResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Interaction check error: {e}")
        raise HTTPException(status_code=500, detail=f"Interaction check failed: {str(e)}")


@router.get("/stats", response_model=StatsResponse)
async def get_statistics():
    """
    Get database statistics
    
    Returns total counts of drugs, compounds, interactions, and breakdown by severity.
    """
    try:
        stats = interaction_service.get_statistics()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Statistics retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")


@router.post("/check-condition-warnings")
async def check_condition_warnings(request: ConditionWarningRequest):
    """
    Check for condition-specific drug warnings using ArangoDB graph traversal.
    
    Given patient conditions and selected drugs, traverse the graph:
    Drug → Compound → Condition Modifier → Condition
    
    Returns warnings for drugs that are affected by patient's conditions.
    """
    try:
        start_time = time.time()
        db = arango_service.get_database()
        
        # AQL query to find condition-based warnings
        query = """
        WITH drugs, compounds, conditions
        LET drug_keys = @drug_keys
        LET patient_conditions = @patient_conditions
        
        FOR drug_key IN drug_keys
            LET drug_id = CONCAT("drugs/", drug_key)
            
            FOR edge1 IN drug_contains_compound
                FILTER edge1._from == drug_id
                LET compound = DOCUMENT(edge1._to)
                
                FOR modifier IN condition_modifiers
                    FILTER modifier._from == compound._id
                    FILTER modifier._to IN patient_conditions
                    
                    LET condition = DOCUMENT(modifier._to)
                    
                    RETURN {
                        drug_name: DOCUMENT(drug_id).name,
                        drug_key: drug_key,
                        compound_name: compound.name,
                        condition_name: condition.name,
                        condition_key: condition._key,
                        modifier_type: modifier.modifier_type,
                        severity: modifier.severity,
                        threshold: modifier.threshold,
                        description: modifier.description,
                        mechanism: modifier.mechanism,
                        clinical_management: modifier.clinical_management,
                        evidence_level: modifier.evidence_level,
                        guideline: modifier.guideline,
                        monitoring: modifier.monitoring,
                        alternative_drugs: modifier.alternative_drugs
                    }
        """
        
        # Convert condition names to full collection IDs
        condition_ids = [f"conditions/{cond}" for cond in request.conditions]
        
        result = db.aql.execute(
            query,
            bind_vars={
                'drug_keys': request.drug_keys,
                'patient_conditions': condition_ids
            }
        )
        
        warnings = list(result)
        
        # Sort by severity (critical > caution > warning > monitoring_required > dose_adjustment)
        severity_order = {
            'critical': 0,
            'caution': 1,
            'warning': 2,
            'monitoring_required': 3,
            'dose_adjustment': 4
        }
        warnings.sort(key=lambda x: severity_order.get(x.get('severity', ''), 99))
        
        query_time = (time.time() - start_time) * 1000
        
        return {
            "warnings_found": len(warnings),
            "query_time_ms": round(query_time, 2),
            "warnings": warnings
        }
        
    except Exception as e:
        logger.error(f"Error checking condition warnings: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

