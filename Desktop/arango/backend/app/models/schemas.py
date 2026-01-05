"""
Pydantic models for request/response validation
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_serializer


class DrugResponse(BaseModel):
    """Drug information response model"""
    key: str = Field(..., alias="_key", serialization_alias="_key")
    name: str
    generic_name: str
    brand_names: List[str]
    strength: str
    dosage_form: str
    drug_class: str
    indication: List[str]
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_key": "warfarin_5mg",
                "name": "Warfarin",
                "generic_name": "Warfarin Sodium",
                "brand_names": ["Coumadin", "Jantoven"],
                "strength": "5mg",
                "dosage_form": "tablet",
                "drug_class": "anticoagulant",
                "indication": ["atrial_fibrillation", "dvt", "pe"]
            }
        }
    
    def model_dump(self, **kwargs):
        """Override to ensure _key is included in output with correct serialization"""
        # Use by_alias=True to ensure _key is serialized correctly
        return super().model_dump(by_alias=True, **kwargs)


class InteractionResponse(BaseModel):
    """Drug interaction response model"""
    compound_1: str
    compound_2: str
    affected_drugs: List[str]
    severity: Literal["severe", "moderate", "minor"]
    interaction_type: str
    description: str
    mechanism: str
    clinical_management: str
    evidence_level: str
    onset: str
    documentation: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "compound_1": "Warfarin",
                "compound_2": "Acetylsalicylic Acid",
                "affected_drugs": ["Warfarin 5mg", "Aspirin 325mg"],
                "severity": "severe",
                "interaction_type": "pharmacodynamic",
                "description": "Increased risk of bleeding due to additive antiplatelet and anticoagulant effects",
                "mechanism": "Warfarin inhibits clotting factors while aspirin inhibits platelet aggregation",
                "clinical_management": "Avoid combination. If necessary, use 81mg aspirin and monitor INR closely.",
                "evidence_level": "high",
                "onset": "rapid",
                "documentation": "well-documented"
            }
        }


class CheckInteractionsRequest(BaseModel):
    """Request model for checking interactions"""
    drug_keys: List[str] = Field(..., min_items=2, max_items=20, description="List of drug _key values")
    
    class Config:
        json_schema_extra = {
            "example": {
                "drug_keys": ["warfarin_5mg", "aspirin_325mg"]
            }
        }


class CheckInteractionsResponse(BaseModel):
    """Response model for interaction check"""
    interactions_found: int
    highest_severity: Optional[str] = None
    query_time_ms: float
    interactions: List[InteractionResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "interactions_found": 2,
                "highest_severity": "severe",
                "query_time_ms": 45.2,
                "interactions": []
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    database: str


class StatsResponse(BaseModel):
    """Statistics response model"""
    total_drugs: int
    total_compounds: int
    total_interactions: int
    interactions_by_severity: dict


class ConditionWarningRequest(BaseModel):
    """Request model for checking condition-based warnings"""
    drug_keys: List[str]
    conditions: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "drug_keys": ["metformin_1000mg", "ibuprofen_200mg"],
                "conditions": ["kidney_disease_ckd", "diabetes_type_2"]
            }
        }

