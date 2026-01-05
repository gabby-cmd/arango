"""
Complete database setup script for Drug Interaction Checker
Run this once to initialize your ArangoDB with all collections and sample data
"""

import os
import sys
from dotenv import load_dotenv
from arango import ArangoClient
from arango.exceptions import (
    DatabaseCreateError,
    CollectionCreateError,
    DocumentInsertError,
    ArangoServerError
)

# Load environment variables
load_dotenv()

# Connection configuration
ARANGO_HOST = os.getenv('ARANGO_HOST')
ARANGO_DB = os.getenv('ARANGO_DB')
ARANGO_USER = os.getenv('ARANGO_USER')
ARANGO_PASSWORD = os.getenv('ARANGO_PASSWORD')

# Validate configuration
if not all([ARANGO_HOST, ARANGO_DB, ARANGO_USER, ARANGO_PASSWORD]):
    print("❌ ERROR: Missing environment variables!")
    print("Please create a .env file with:")
    print("  ARANGO_HOST=https://d8c1701e2a10.arangodb.cloud:8529")
    print("  ARANGO_DB=drug_interation_db")
    print("  ARANGO_USER=root")
    print("  ARANGO_PASSWORD=your_password")
    sys.exit(1)

print("🔧 Starting ArangoDB setup...")
print(f"   Host: {ARANGO_HOST}")
print(f"   Database: {ARANGO_DB}")
print(f"   User: {ARANGO_USER}")
print()

# ============================================================================
# SAMPLE DATA DEFINITIONS
# ============================================================================

COMPOUNDS_DATA = [
    # Anticoagulants
    {"_key": "warfarin", "name": "Warfarin", "chemical_formula": "C19H16O4", 
     "compound_class": "coumarin_anticoagulant", "mechanism_of_action": "Vitamin K antagonist"},
    
    # NSAIDs
    {"_key": "acetylsalicylic_acid", "name": "Acetylsalicylic Acid", "chemical_formula": "C9H8O4",
     "compound_class": "salicylate", "mechanism_of_action": "COX-1 and COX-2 inhibitor"},
    {"_key": "ibuprofen", "name": "Ibuprofen", "chemical_formula": "C13H18O2",
     "compound_class": "propionic_acid", "mechanism_of_action": "Non-selective COX inhibitor"},
    {"_key": "naproxen", "name": "Naproxen", "chemical_formula": "C14H14O3",
     "compound_class": "propionic_acid", "mechanism_of_action": "Non-selective COX inhibitor"},
    
    # Antiplatelets
    {"_key": "clopidogrel", "name": "Clopidogrel", "chemical_formula": "C16H16ClNO2S",
     "compound_class": "thienopyridine", "mechanism_of_action": "P2Y12 receptor antagonist"},
    
    # ACE Inhibitors
    {"_key": "lisinopril", "name": "Lisinopril", "chemical_formula": "C21H31N3O5",
     "compound_class": "ace_inhibitor", "mechanism_of_action": "Angiotensin-converting enzyme inhibitor"},
    
    # Beta Blockers
    {"_key": "metoprolol", "name": "Metoprolol", "chemical_formula": "C15H25NO3",
     "compound_class": "beta_blocker", "mechanism_of_action": "Selective beta-1 adrenergic antagonist"},
    {"_key": "carvedilol", "name": "Carvedilol", "chemical_formula": "C24H26N2O4",
     "compound_class": "beta_blocker", "mechanism_of_action": "Non-selective beta and alpha-1 blocker"},
    
    # Statins
    {"_key": "atorvastatin", "name": "Atorvastatin", "chemical_formula": "C33H35FN2O5",
     "compound_class": "statin", "mechanism_of_action": "HMG-CoA reductase inhibitor"},
    
    # Calcium Channel Blockers
    {"_key": "amlodipine", "name": "Amlodipine", "chemical_formula": "C20H25ClN2O5",
     "compound_class": "dihydropyridine", "mechanism_of_action": "Calcium channel blocker"},
    
    # Cardiac Glycosides
    {"_key": "digoxin", "name": "Digoxin", "chemical_formula": "C41H64O14",
     "compound_class": "cardiac_glycoside", "mechanism_of_action": "Na+/K+-ATPase inhibitor"},
    
    # Diuretics
    {"_key": "furosemide", "name": "Furosemide", "chemical_formula": "C12H11ClN2O5S",
     "compound_class": "loop_diuretic", "mechanism_of_action": "Na-K-Cl cotransporter inhibitor"},
    
    # Diabetes medications
    {"_key": "metformin", "name": "Metformin", "chemical_formula": "C4H11N5",
     "compound_class": "biguanide", "mechanism_of_action": "Decreases hepatic glucose production"},
    {"_key": "glipizide", "name": "Glipizide", "chemical_formula": "C21H27N5O4S",
     "compound_class": "sulfonylurea", "mechanism_of_action": "Stimulates pancreatic insulin release"},
    {"_key": "insulin_glargine", "name": "Insulin Glargine", "chemical_formula": "C267H404N72O78S6",
     "compound_class": "long_acting_insulin", "mechanism_of_action": "Insulin receptor agonist"},
    
    # Antibiotics
    {"_key": "amoxicillin", "name": "Amoxicillin", "chemical_formula": "C16H19N3O5S",
     "compound_class": "penicillin", "mechanism_of_action": "Beta-lactam antibiotic"},
    {"_key": "azithromycin", "name": "Azithromycin", "chemical_formula": "C38H72N2O12",
     "compound_class": "macrolide", "mechanism_of_action": "50S ribosomal subunit inhibitor"},
    {"_key": "ciprofloxacin", "name": "Ciprofloxacin", "chemical_formula": "C17H18FN3O3",
     "compound_class": "fluoroquinolone", "mechanism_of_action": "DNA gyrase inhibitor"},
    
    # SSRIs
    {"_key": "sertraline", "name": "Sertraline", "chemical_formula": "C17H17Cl2N",
     "compound_class": "ssri", "mechanism_of_action": "Selective serotonin reuptake inhibitor"},
    {"_key": "fluoxetine", "name": "Fluoxetine", "chemical_formula": "C17H18F3NO",
     "compound_class": "ssri", "mechanism_of_action": "Selective serotonin reuptake inhibitor"},
    
    # Pain medications
    {"_key": "acetaminophen", "name": "Acetaminophen", "chemical_formula": "C8H9NO2",
     "compound_class": "analgesic", "mechanism_of_action": "COX inhibitor (CNS selective)"},
    {"_key": "tramadol", "name": "Tramadol", "chemical_formula": "C16H25NO2",
     "compound_class": "opioid_analgesic", "mechanism_of_action": "Mu-opioid receptor agonist and SNRI"},
    
    # Benzodiazepines
    {"_key": "alprazolam", "name": "Alprazolam", "chemical_formula": "C17H13ClN4",
     "compound_class": "benzodiazepine", "mechanism_of_action": "GABA-A receptor positive modulator"},
]

CONDITIONS_DATA = [
    {
        "_key": "kidney_disease_ckd",
        "name": "Chronic Kidney Disease",
        "category": "renal",
        "severity_stages": ["stage_3", "stage_4", "stage_5"],
        "clinical_definition": "Progressive loss of kidney function",
        "diagnostic_criteria": "eGFR < 60 mL/min/1.73m² for >3 months",
        "icd10_codes": ["N18.3", "N18.4", "N18.5"],
        "common_causes": ["diabetes", "hypertension", "glomerulonephritis"],
        "typical_labs": {
            "creatinine": ">1.5 mg/dL",
            "egfr": "<60 mL/min/1.73m²",
            "bun": ">20 mg/dL"
        }
    },
    {
        "_key": "diabetes_type_2",
        "name": "Diabetes Mellitus Type 2",
        "category": "endocrine",
        "clinical_definition": "Chronic metabolic disorder characterized by insulin resistance",
        "diagnostic_criteria": "HbA1c ≥6.5% or fasting glucose ≥126 mg/dL",
        "icd10_codes": ["E11"],
        "common_complications": ["neuropathy", "retinopathy", "nephropathy", "cardiovascular_disease"],
        "typical_labs": {
            "hba1c": ">6.5%",
            "fasting_glucose": ">126 mg/dL"
        }
    },
    {
        "_key": "liver_disease_cirrhosis",
        "name": "Liver Disease / Cirrhosis",
        "category": "hepatic",
        "severity_stages": ["compensated", "decompensated"],
        "clinical_definition": "Chronic liver damage leading to scarring and liver dysfunction",
        "diagnostic_criteria": "Clinical signs, imaging, biopsy showing fibrosis",
        "icd10_codes": ["K74"],
        "common_causes": ["alcohol", "viral_hepatitis", "nash"],
        "typical_labs": {
            "alt": "elevated",
            "ast": "elevated",
            "bilirubin": "elevated",
            "albumin": "decreased",
            "inr": "elevated"
        }
    },
    {
        "_key": "pregnancy",
        "name": "Pregnancy",
        "category": "reproductive",
        "clinical_definition": "State of carrying a developing embryo or fetus",
        "trimesters": ["first", "second", "third"],
        "special_considerations": ["teratogenicity", "maternal_safety", "fetal_development"]
    },
    {
        "_key": "elderly_age_65plus",
        "name": "Elderly (Age ≥65)",
        "category": "demographic",
        "clinical_definition": "Advanced age with associated physiological changes",
        "common_considerations": [
            "reduced_renal_clearance",
            "altered_drug_metabolism",
            "increased_fall_risk",
            "polypharmacy",
            "cognitive_changes"
        ],
        "beers_criteria_applicable": True
    }
]

DRUGS_DATA = [
    # Anticoagulants
    {"_key": "warfarin_5mg", "name": "Warfarin", "generic_name": "Warfarin Sodium",
     "brand_names": ["Coumadin", "Jantoven"], "dosage_form": "tablet", "strength": "5mg",
     "drug_class": "anticoagulant", "indication": ["atrial_fibrillation", "dvt", "pe"]},
    
    # Antiplatelets/NSAIDs
    {"_key": "aspirin_81mg", "name": "Aspirin Low Dose", "generic_name": "Acetylsalicylic Acid",
     "brand_names": ["Bayer", "Ecotrin"], "dosage_form": "tablet", "strength": "81mg",
     "drug_class": "antiplatelet", "indication": ["cardiovascular_prevention"]},
    
    {"_key": "aspirin_325mg", "name": "Aspirin", "generic_name": "Acetylsalicylic Acid",
     "brand_names": ["Bayer", "Bufferin"], "dosage_form": "tablet", "strength": "325mg",
     "drug_class": "nsaid", "indication": ["pain", "inflammation", "fever"]},
    
    {"_key": "clopidogrel_75mg", "name": "Plavix", "generic_name": "Clopidogrel",
     "brand_names": ["Plavix"], "dosage_form": "tablet", "strength": "75mg",
     "drug_class": "antiplatelet", "indication": ["acs", "stroke_prevention"]},
    
    {"_key": "ibuprofen_200mg", "name": "Advil", "generic_name": "Ibuprofen",
     "brand_names": ["Advil", "Motrin"], "dosage_form": "tablet", "strength": "200mg",
     "drug_class": "nsaid", "indication": ["pain", "inflammation"]},
    
    {"_key": "naproxen_500mg", "name": "Aleve", "generic_name": "Naproxen",
     "brand_names": ["Aleve", "Naprosyn"], "dosage_form": "tablet", "strength": "500mg",
     "drug_class": "nsaid", "indication": ["pain", "arthritis"]},
    
    # Cardiovascular
    {"_key": "lisinopril_10mg", "name": "Lisinopril", "generic_name": "Lisinopril",
     "brand_names": ["Prinivil", "Zestril"], "dosage_form": "tablet", "strength": "10mg",
     "drug_class": "ace_inhibitor", "indication": ["hypertension", "heart_failure"]},
    
    {"_key": "metoprolol_50mg", "name": "Metoprolol", "generic_name": "Metoprolol Succinate",
     "brand_names": ["Toprol-XL"], "dosage_form": "tablet", "strength": "50mg",
     "drug_class": "beta_blocker", "indication": ["hypertension", "heart_failure"]},
    
    {"_key": "carvedilol_25mg", "name": "Carvedilol", "generic_name": "Carvedilol",
     "brand_names": ["Coreg"], "dosage_form": "tablet", "strength": "25mg",
     "drug_class": "beta_blocker", "indication": ["heart_failure"]},
    
    {"_key": "atorvastatin_40mg", "name": "Lipitor", "generic_name": "Atorvastatin",
     "brand_names": ["Lipitor"], "dosage_form": "tablet", "strength": "40mg",
     "drug_class": "statin", "indication": ["hyperlipidemia"]},
    
    {"_key": "amlodipine_5mg", "name": "Norvasc", "generic_name": "Amlodipine",
     "brand_names": ["Norvasc"], "dosage_form": "tablet", "strength": "5mg",
     "drug_class": "calcium_channel_blocker", "indication": ["hypertension"]},
    
    {"_key": "digoxin_0_25mg", "name": "Digoxin", "generic_name": "Digoxin",
     "brand_names": ["Lanoxin"], "dosage_form": "tablet", "strength": "0.25mg",
     "drug_class": "cardiac_glycoside", "indication": ["atrial_fibrillation"]},
    
    {"_key": "furosemide_40mg", "name": "Lasix", "generic_name": "Furosemide",
     "brand_names": ["Lasix"], "dosage_form": "tablet", "strength": "40mg",
     "drug_class": "loop_diuretic", "indication": ["edema", "heart_failure"]},
    
    # Diabetes
    {"_key": "metformin_1000mg", "name": "Glucophage", "generic_name": "Metformin",
     "brand_names": ["Glucophage"], "dosage_form": "tablet", "strength": "1000mg",
     "drug_class": "biguanide", "indication": ["type_2_diabetes"]},
    
    {"_key": "glipizide_5mg", "name": "Glucotrol", "generic_name": "Glipizide",
     "brand_names": ["Glucotrol"], "dosage_form": "tablet", "strength": "5mg",
     "drug_class": "sulfonylurea", "indication": ["type_2_diabetes"]},
    
    {"_key": "insulin_glargine_100units", "name": "Lantus", "generic_name": "Insulin Glargine",
     "brand_names": ["Lantus"], "dosage_form": "injection", "strength": "100units/mL",
     "drug_class": "long_acting_insulin", "indication": ["diabetes"]},
    
    # Antibiotics
    {"_key": "amoxicillin_500mg", "name": "Amoxicillin", "generic_name": "Amoxicillin",
     "brand_names": ["Amoxil"], "dosage_form": "capsule", "strength": "500mg",
     "drug_class": "penicillin", "indication": ["bacterial_infections"]},
    
    {"_key": "azithromycin_250mg", "name": "Zithromax", "generic_name": "Azithromycin",
     "brand_names": ["Zithromax"], "dosage_form": "tablet", "strength": "250mg",
     "drug_class": "macrolide", "indication": ["bacterial_infections"]},
    
    {"_key": "ciprofloxacin_500mg", "name": "Cipro", "generic_name": "Ciprofloxacin",
     "brand_names": ["Cipro"], "dosage_form": "tablet", "strength": "500mg",
     "drug_class": "fluoroquinolone", "indication": ["bacterial_infections"]},
    
    # Mental Health
    {"_key": "sertraline_50mg", "name": "Zoloft", "generic_name": "Sertraline",
     "brand_names": ["Zoloft"], "dosage_form": "tablet", "strength": "50mg",
     "drug_class": "ssri", "indication": ["depression", "anxiety"]},
    
    {"_key": "fluoxetine_20mg", "name": "Prozac", "generic_name": "Fluoxetine",
     "brand_names": ["Prozac"], "dosage_form": "capsule", "strength": "20mg",
     "drug_class": "ssri", "indication": ["depression"]},
    
    # Pain
    {"_key": "acetaminophen_500mg", "name": "Tylenol", "generic_name": "Acetaminophen",
     "brand_names": ["Tylenol"], "dosage_form": "tablet", "strength": "500mg",
     "drug_class": "analgesic", "indication": ["pain", "fever"]},
    
    {"_key": "tramadol_50mg", "name": "Ultram", "generic_name": "Tramadol",
     "brand_names": ["Ultram"], "dosage_form": "tablet", "strength": "50mg",
     "drug_class": "opioid_analgesic", "indication": ["moderate_pain"]},
    
    {"_key": "alprazolam_0_5mg", "name": "Xanax", "generic_name": "Alprazolam",
     "brand_names": ["Xanax"], "dosage_form": "tablet", "strength": "0.5mg",
     "drug_class": "benzodiazepine", "indication": ["anxiety"]},
]

DRUG_COMPOUND_EDGES = [
    {"_from": "drugs/warfarin_5mg", "_to": "compounds/warfarin", "is_active_ingredient": True},
    {"_from": "drugs/aspirin_81mg", "_to": "compounds/acetylsalicylic_acid", "is_active_ingredient": True},
    {"_from": "drugs/aspirin_325mg", "_to": "compounds/acetylsalicylic_acid", "is_active_ingredient": True},
    {"_from": "drugs/clopidogrel_75mg", "_to": "compounds/clopidogrel", "is_active_ingredient": True},
    {"_from": "drugs/ibuprofen_200mg", "_to": "compounds/ibuprofen", "is_active_ingredient": True},
    {"_from": "drugs/naproxen_500mg", "_to": "compounds/naproxen", "is_active_ingredient": True},
    {"_from": "drugs/lisinopril_10mg", "_to": "compounds/lisinopril", "is_active_ingredient": True},
    {"_from": "drugs/metoprolol_50mg", "_to": "compounds/metoprolol", "is_active_ingredient": True},
    {"_from": "drugs/carvedilol_25mg", "_to": "compounds/carvedilol", "is_active_ingredient": True},
    {"_from": "drugs/atorvastatin_40mg", "_to": "compounds/atorvastatin", "is_active_ingredient": True},
    {"_from": "drugs/amlodipine_5mg", "_to": "compounds/amlodipine", "is_active_ingredient": True},
    {"_from": "drugs/digoxin_0_25mg", "_to": "compounds/digoxin", "is_active_ingredient": True},
    {"_from": "drugs/furosemide_40mg", "_to": "compounds/furosemide", "is_active_ingredient": True},
    {"_from": "drugs/metformin_1000mg", "_to": "compounds/metformin", "is_active_ingredient": True},
    {"_from": "drugs/glipizide_5mg", "_to": "compounds/glipizide", "is_active_ingredient": True},
    {"_from": "drugs/insulin_glargine_100units", "_to": "compounds/insulin_glargine", "is_active_ingredient": True},
    {"_from": "drugs/amoxicillin_500mg", "_to": "compounds/amoxicillin", "is_active_ingredient": True},
    {"_from": "drugs/azithromycin_250mg", "_to": "compounds/azithromycin", "is_active_ingredient": True},
    {"_from": "drugs/ciprofloxacin_500mg", "_to": "compounds/ciprofloxacin", "is_active_ingredient": True},
    {"_from": "drugs/sertraline_50mg", "_to": "compounds/sertraline", "is_active_ingredient": True},
    {"_from": "drugs/fluoxetine_20mg", "_to": "compounds/fluoxetine", "is_active_ingredient": True},
    {"_from": "drugs/acetaminophen_500mg", "_to": "compounds/acetaminophen", "is_active_ingredient": True},
    {"_from": "drugs/tramadol_50mg", "_to": "compounds/tramadol", "is_active_ingredient": True},
    {"_from": "drugs/alprazolam_0_5mg", "_to": "compounds/alprazolam", "is_active_ingredient": True},
]

INTERACTION_EDGES = [
    # SEVERE - Warfarin + NSAIDs (bleeding risk)
    {
        "_from": "compounds/warfarin", "_to": "compounds/acetylsalicylic_acid",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Increased risk of bleeding due to additive antiplatelet and anticoagulant effects",
        "mechanism": "Warfarin inhibits clotting factors while aspirin inhibits platelet aggregation",
        "clinical_management": "Avoid combination. If necessary, use 81mg aspirin and monitor INR closely.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    {
        "_from": "compounds/warfarin", "_to": "compounds/ibuprofen",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Significantly increased bleeding risk",
        "mechanism": "Combined anticoagulation and antiplatelet effects plus GI irritation",
        "clinical_management": "Avoid combination. Consider acetaminophen instead.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    {
        "_from": "compounds/warfarin", "_to": "compounds/naproxen",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Major bleeding risk with combined use",
        "mechanism": "Dual antiplatelet/anticoagulant effects",
        "clinical_management": "Avoid combination if possible.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    {
        "_from": "compounds/warfarin", "_to": "compounds/clopidogrel",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Markedly increased bleeding risk",
        "mechanism": "Warfarin prevents clot formation while clopidogrel prevents platelet aggregation",
        "clinical_management": "Use only when specifically indicated (e.g., mechanical valve). Requires close monitoring.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    
    # MODERATE - NSAIDs combined
    {
        "_from": "compounds/acetylsalicylic_acid", "_to": "compounds/ibuprofen",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "Increased GI bleeding risk and reduced aspirin cardioprotection",
        "mechanism": "Ibuprofen blocks aspirin's COX-1 access, both cause GI damage",
        "clinical_management": "Separate by 2+ hours. Consider alternative analgesic.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    
    # Warfarin + Antibiotics (INR changes)
    {
        "_from": "compounds/warfarin", "_to": "compounds/azithromycin",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "May increase INR through gut flora disruption",
        "mechanism": "Reduced vitamin K production from gut bacteria",
        "clinical_management": "Monitor INR within 3-5 days of antibiotic start.",
        "evidence_level": "moderate", "onset": "delayed", "documentation": "probable"
    },
    {
        "_from": "compounds/warfarin", "_to": "compounds/ciprofloxacin",
        "severity": "moderate", "interaction_type": "pharmacokinetic",
        "description": "Increases warfarin levels and INR",
        "mechanism": "CYP inhibition reduces warfarin clearance",
        "clinical_management": "Reduce warfarin dose by 10-25%. Check INR frequently.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    
    # Digoxin interactions
    {
        "_from": "compounds/digoxin", "_to": "compounds/furosemide",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "Hypokalemia increases digoxin toxicity risk",
        "mechanism": "Potassium depletion enhances digoxin binding to Na+/K+-ATPase",
        "clinical_management": "Monitor potassium. Maintain K+ >4.0. Consider K+ supplementation.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    {
        "_from": "compounds/digoxin", "_to": "compounds/azithromycin",
        "severity": "moderate", "interaction_type": "pharmacokinetic",
        "description": "May increase digoxin levels 30-50%",
        "mechanism": "P-glycoprotein inhibition reduces digoxin elimination",
        "clinical_management": "Monitor digoxin levels. Watch for toxicity signs.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    
    # SSRI + Tramadol (Serotonin syndrome)
    {
        "_from": "compounds/sertraline", "_to": "compounds/tramadol",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Risk of serotonin syndrome",
        "mechanism": "Both increase serotonergic activity",
        "clinical_management": "Avoid combination. Educate on serotonin syndrome symptoms.",
        "evidence_level": "moderate", "onset": "rapid", "documentation": "probable"
    },
    {
        "_from": "compounds/fluoxetine", "_to": "compounds/tramadol",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Serotonin syndrome risk plus increased tramadol levels",
        "mechanism": "Serotonergic effects plus CYP2D6 inhibition",
        "clinical_management": "Avoid. Consider alternative analgesic.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    
    # SSRI + NSAIDs (GI bleeding)
    {
        "_from": "compounds/sertraline", "_to": "compounds/ibuprofen",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "Increased GI bleeding risk",
        "mechanism": "SSRIs impair platelet function, NSAIDs damage mucosa",
        "clinical_management": "Consider PPI prophylaxis. Use lowest NSAID dose.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    {
        "_from": "compounds/fluoxetine", "_to": "compounds/acetylsalicylic_acid",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "Increased bleeding risk",
        "mechanism": "Both impair platelet function via different mechanisms",
        "clinical_management": "Monitor for bruising/bleeding. Consider PPI.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    
    # Beta blockers + Diabetes (mask hypoglycemia)
    {
        "_from": "compounds/metoprolol", "_to": "compounds/glipizide",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "Beta blockers mask hypoglycemia symptoms",
        "mechanism": "Blocks adrenergic warning signs (tremor, palpitations)",
        "clinical_management": "Educate patient. Increase glucose monitoring.",
        "evidence_level": "moderate", "onset": "delayed", "documentation": "probable"
    },
    {
        "_from": "compounds/carvedilol", "_to": "compounds/insulin_glargine",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "May mask hypoglycemic symptoms",
        "mechanism": "Blocks adrenergic hypoglycemia response",
        "clinical_management": "Patient education on atypical symptoms.",
        "evidence_level": "moderate", "onset": "delayed", "documentation": "probable"
    },
    
    # Fluoroquinolones + Diabetes
    {
        "_from": "compounds/ciprofloxacin", "_to": "compounds/glipizide",
        "severity": "moderate", "interaction_type": "pharmacodynamic",
        "description": "May cause unpredictable glucose changes",
        "mechanism": "Direct effect on pancreatic beta cells",
        "clinical_management": "Monitor glucose closely. FDA black box warning.",
        "evidence_level": "moderate", "onset": "rapid", "documentation": "probable"
    },
    
    # Benzodiazepine + Opioid
    {
        "_from": "compounds/alprazolam", "_to": "compounds/tramadol",
        "severity": "severe", "interaction_type": "pharmacodynamic",
        "description": "Risk of profound sedation, respiratory depression, death",
        "mechanism": "Additive CNS and respiratory depression",
        "clinical_management": "AVOID. FDA black box warning. If unavoidable, lowest doses only.",
        "evidence_level": "high", "onset": "rapid", "documentation": "well-documented"
    },
    {
        "_from": "compounds/alprazolam", "_to": "compounds/fluoxetine",
        "severity": "moderate", "interaction_type": "pharmacokinetic",
        "description": "Increased alprazolam levels and sedation",
        "mechanism": "CYP3A4 inhibition increases alprazolam concentration",
        "clinical_management": "Reduce alprazolam dose by 50%. Monitor for sedation.",
        "evidence_level": "high", "onset": "delayed", "documentation": "well-documented"
    },
    
    # Statin interactions
    {
        "_from": "compounds/atorvastatin", "_to": "compounds/amlodipine",
        "severity": "minor", "interaction_type": "pharmacokinetic",
        "description": "Slightly increased statin levels",
        "mechanism": "CYP3A4 inhibition by amlodipine",
        "clinical_management": "Limit atorvastatin to 20mg. Monitor for muscle pain.",
        "evidence_level": "moderate", "onset": "delayed", "documentation": "probable"
    },
    {
        "_from": "compounds/atorvastatin", "_to": "compounds/azithromycin",
        "severity": "minor", "interaction_type": "pharmacokinetic",
        "description": "May increase rhabdomyolysis risk",
        "mechanism": "CYP3A4 inhibition increases statin exposure",
        "clinical_management": "Consider holding statin during short antibiotic course.",
        "evidence_level": "moderate", "onset": "rapid", "documentation": "probable"
    },
    
    # MINOR interactions (safe combinations shown)
    {
        "_from": "compounds/lisinopril", "_to": "compounds/furosemide",
        "severity": "minor", "interaction_type": "pharmacodynamic",
        "description": "Potential excessive hypotension",
        "mechanism": "Additive BP lowering",
        "clinical_management": "Monitor BP at initiation. Check electrolytes.",
        "evidence_level": "moderate", "onset": "delayed", "documentation": "probable"
    },
    {
        "_from": "compounds/metformin", "_to": "compounds/lisinopril",
        "severity": "minor", "interaction_type": "pharmacodynamic",
        "description": "Theoretical lactic acidosis risk in renal impairment",
        "mechanism": "ACE inhibitor may affect renal function",
        "clinical_management": "Monitor renal function every 3-6 months.",
        "evidence_level": "low", "onset": "delayed", "documentation": "theoretical"
    },
    {
        "_from": "compounds/acetaminophen", "_to": "compounds/lisinopril",
        "severity": "minor", "interaction_type": "pharmacodynamic",
        "description": "High-dose acetaminophen may reduce antihypertensive effect",
        "mechanism": "Prostaglandin-mediated BP changes",
        "clinical_management": "Monitor BP with regular high-dose use.",
        "evidence_level": "low", "onset": "delayed", "documentation": "possible"
    },
]

CONDITION_MODIFIER_EDGES = [
    # ========================================
    # KIDNEY DISEASE MODIFIERS
    # ========================================
    {
        "_from": "compounds/metformin",
        "_to": "conditions/kidney_disease_ckd",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "eGFR < 30 mL/min/1.73m²",
        "description": "Metformin is contraindicated in patients with eGFR <30 mL/min/1.73m². Risk of lactic acidosis, a potentially fatal complication.",
        "mechanism": "Reduced renal clearance leads to metformin accumulation, causing lactic acidosis",
        "clinical_management": "Discontinue metformin immediately. Consider DPP-4 inhibitor (sitagliptin), GLP-1 agonist, or insulin as alternative.",
        "evidence_level": "high",
        "guideline": "FDA Black Box Warning",
        "monitoring": "Check eGFR before starting and at least annually"
    },
    {
        "_from": "compounds/ibuprofen",
        "_to": "conditions/kidney_disease_ckd",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "Any stage CKD",
        "description": "NSAIDs can cause acute kidney injury and accelerate CKD progression.",
        "mechanism": "Inhibition of prostaglandin synthesis reduces renal blood flow and GFR",
        "clinical_management": "Avoid all NSAIDs. Use acetaminophen (max 3g/day) for pain management.",
        "evidence_level": "high",
        "guideline": "KDIGO CKD Guidelines"
    },
    {
        "_from": "compounds/naproxen",
        "_to": "conditions/kidney_disease_ckd",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "Any stage CKD",
        "description": "NSAID use in CKD increases risk of acute kidney injury and disease progression",
        "mechanism": "Prostaglandin inhibition compromises renal hemodynamics",
        "clinical_management": "Avoid. Use acetaminophen or topical analgesics instead.",
        "evidence_level": "high"
    },
    {
        "_from": "compounds/digoxin",
        "_to": "conditions/kidney_disease_ckd",
        "modifier_type": "dose_adjustment",
        "severity": "caution",
        "threshold": "eGFR < 50 mL/min/1.73m²",
        "description": "Reduced renal clearance leads to digoxin accumulation and toxicity risk",
        "mechanism": "Digoxin is primarily renally cleared; impaired clearance increases levels",
        "clinical_management": "Reduce dose by 50% in severe CKD (eGFR <30). Monitor digoxin levels closely (target 0.5-1.0 ng/mL, not 0.8-2.0). Watch for toxicity: nausea, vision changes, arrhythmias.",
        "evidence_level": "high",
        "monitoring": "Check digoxin level 1-2 weeks after dose change, then every 3-6 months"
    },
    {
        "_from": "compounds/lisinopril",
        "_to": "conditions/kidney_disease_ckd",
        "modifier_type": "monitoring_required",
        "severity": "caution",
        "threshold": "All stages",
        "description": "ACE inhibitors may cause acute decrease in GFR and hyperkalemia in CKD",
        "mechanism": "Reduced efferent arteriole tone decreases glomerular filtration pressure",
        "clinical_management": "Monitor K+ and creatinine within 1-2 weeks of starting or dose change. Acceptable for creatinine to increase up to 30%. Hold if K+ >5.5 mEq/L.",
        "evidence_level": "high"
    },
    
    # ========================================
    # DIABETES MODIFIERS
    # ========================================
    {
        "_from": "compounds/metoprolol",
        "_to": "conditions/diabetes_type_2",
        "modifier_type": "warning",
        "severity": "caution",
        "threshold": "Patients on insulin or sulfonylureas",
        "description": "Beta-blockers mask warning signs of hypoglycemia (tremor, tachycardia) in diabetic patients",
        "mechanism": "Beta-adrenergic blockade prevents catecholamine-mediated symptoms of hypoglycemia",
        "clinical_management": "Educate patient on atypical hypoglycemia symptoms (sweating, hunger, confusion still occur). Increase glucose monitoring frequency. Sweating is NOT blocked by beta-blockers.",
        "evidence_level": "moderate",
        "monitoring": "More frequent blood glucose checks, especially during dose adjustments"
    },
    {
        "_from": "compounds/carvedilol",
        "_to": "conditions/diabetes_type_2",
        "modifier_type": "warning",
        "severity": "caution",
        "threshold": "Insulin-treated diabetes",
        "description": "Non-selective beta-blocker may mask hypoglycemic symptoms and prolong recovery from hypoglycemia",
        "mechanism": "Blocks both beta-1 and beta-2 receptors, affecting glucose recovery mechanisms",
        "clinical_management": "Patient education on masked hypoglycemia. Monitor blood glucose more frequently. May delay recovery from hypoglycemia.",
        "evidence_level": "moderate"
    },
    {
        "_from": "compounds/ciprofloxacin",
        "_to": "conditions/diabetes_type_2",
        "modifier_type": "warning",
        "severity": "caution",
        "threshold": "All diabetic patients",
        "description": "Fluoroquinolones may cause unpredictable glucose changes (both hypo and hyperglycemia)",
        "mechanism": "Direct effect on pancreatic beta cells causing dysregulated insulin release",
        "clinical_management": "Monitor blood glucose closely during fluoroquinolone therapy. Be prepared to adjust diabetes medication. FDA black box warning for severe hypoglycemia.",
        "evidence_level": "moderate",
        "guideline": "FDA 2018 Safety Communication"
    },
    
    # ========================================
    # LIVER DISEASE MODIFIERS
    # ========================================
    {
        "_from": "compounds/warfarin",
        "_to": "conditions/liver_disease_cirrhosis",
        "modifier_type": "dose_adjustment",
        "severity": "caution",
        "threshold": "Cirrhosis or elevated liver enzymes",
        "description": "Liver disease impairs synthesis of vitamin K-dependent clotting factors, increasing bleeding risk with warfarin",
        "mechanism": "Reduced production of factors II, VII, IX, X plus warfarin's anticoagulant effect",
        "clinical_management": "Start with 50% of normal dose. Monitor INR more frequently (every 3-5 days initially, then weekly). Target INR may need adjustment. Consider DOAC as alternative.",
        "evidence_level": "high",
        "monitoring": "INR every 3-5 days until stable, then weekly to biweekly"
    },
    {
        "_from": "compounds/acetaminophen",
        "_to": "conditions/liver_disease_cirrhosis",
        "modifier_type": "dose_adjustment",
        "severity": "critical",
        "threshold": "Any liver disease",
        "description": "Hepatotoxicity risk even at therapeutic doses in patients with liver disease",
        "mechanism": "Impaired hepatic metabolism leads to accumulation of toxic NAPQI metabolite",
        "clinical_management": "Limit to <2g/day in mild liver disease. AVOID completely in severe liver disease or active hepatitis. Consider alternative analgesic (low-dose opioid if needed).",
        "evidence_level": "high",
        "guideline": "FDA Liver Toxicity Warning"
    },
    {
        "_from": "compounds/atorvastatin",
        "_to": "conditions/liver_disease_cirrhosis",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "Active liver disease or unexplained persistent transaminase elevation",
        "description": "Statins contraindicated in active liver disease due to hepatotoxicity risk",
        "mechanism": "Statins metabolized by liver; impaired function increases toxicity risk",
        "clinical_management": "AVOID in active liver disease. If stable chronic disease, may use with caution and close monitoring of LFTs.",
        "evidence_level": "high"
    },
    
    # ========================================
    # PREGNANCY MODIFIERS
    # ========================================
    {
        "_from": "compounds/warfarin",
        "_to": "conditions/pregnancy",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "All trimesters (especially first trimester)",
        "description": "Warfarin is teratogenic, causing fetal warfarin syndrome (nasal hypoplasia, skeletal abnormalities) and CNS abnormalities",
        "mechanism": "Crosses placenta; interferes with vitamin K-dependent proteins in fetal development",
        "clinical_management": "Switch to LMWH (enoxaparin, dalteparin) IMMEDIATELY upon pregnancy confirmation. LMWH does not cross placenta and is safe in pregnancy.",
        "evidence_level": "high",
        "guideline": "FDA Pregnancy Category X",
        "alternative_drugs": ["enoxaparin", "dalteparin"]
    },
    {
        "_from": "compounds/lisinopril",
        "_to": "conditions/pregnancy",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "Second and third trimester (avoid in first as well)",
        "description": "ACE inhibitors cause fetal renal dysgenesis, oligohydramnios, pulmonary hypoplasia, and fetal/neonatal death",
        "mechanism": "Disrupts fetal renin-angiotensin system critical for kidney development",
        "clinical_management": "Discontinue IMMEDIATELY upon pregnancy confirmation. Switch to methyldopa (first-line), labetalol, or nifedipine for BP control in pregnancy.",
        "evidence_level": "high",
        "guideline": "FDA Pregnancy Category D (2nd/3rd trimester)",
        "alternative_drugs": ["methyldopa", "labetalol", "nifedipine"]
    },
    {
        "_from": "compounds/ibuprofen",
        "_to": "conditions/pregnancy",
        "modifier_type": "contraindication",
        "severity": "critical",
        "threshold": "After 30 weeks gestation",
        "description": "NSAIDs after 30 weeks can cause premature closure of fetal ductus arteriosus and oligohydramnios",
        "mechanism": "Prostaglandin inhibition affects fetal circulation and amniotic fluid production",
        "clinical_management": "Avoid after 30 weeks. Use acetaminophen for pain/fever instead (safe in pregnancy).",
        "evidence_level": "high",
        "alternative_drugs": ["acetaminophen"]
    },
    
    # ========================================
    # ELDERLY (AGE ≥65) MODIFIERS
    # ========================================
    {
        "_from": "compounds/alprazolam",
        "_to": "conditions/elderly_age_65plus",
        "modifier_type": "warning",
        "severity": "caution",
        "threshold": "Age ≥65 years",
        "description": "Benzodiazepines increase fall risk, cognitive impairment, delirium, and paradoxical agitation in elderly",
        "mechanism": "Increased CNS sensitivity, prolonged half-life due to reduced clearance, increased risk of accumulation",
        "clinical_management": "AVOID if possible (AGS Beers Criteria - strong recommendation). If necessary, use lowest dose, short-acting agents preferred (lorazepam, oxazepam). Consider non-benzo alternatives (trazodone, gabapentin for anxiety).",
        "evidence_level": "high",
        "guideline": "AGS Beers Criteria 2023",
        "alternative_drugs": ["trazodone", "gabapentin", "buspirone"]
    },
    {
        "_from": "compounds/tramadol",
        "_to": "conditions/elderly_age_65plus",
        "modifier_type": "dose_adjustment",
        "severity": "caution",
        "threshold": "Age ≥65 years",
        "description": "Increased risk of falls, confusion, constipation, and serotonin syndrome in elderly",
        "mechanism": "Reduced clearance, increased CNS sensitivity",
        "clinical_management": "Start with 50% of usual dose. Max 300mg/day (vs 400mg in younger adults). Avoid if history of falls. Monitor for confusion.",
        "evidence_level": "moderate"
    },
    {
        "_from": "compounds/digoxin",
        "_to": "conditions/elderly_age_65plus",
        "modifier_type": "dose_adjustment",
        "severity": "caution",
        "threshold": "Age ≥65 years",
        "description": "Reduced renal clearance and smaller volume of distribution increase digoxin toxicity risk",
        "mechanism": "Age-related decline in GFR and lean body mass",
        "clinical_management": "Use lower doses (0.125mg/day or less). Target levels 0.5-1.0 ng/mL (NOT 0.8-2.0). Monitor levels more frequently.",
        "evidence_level": "high"
    }
]

# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

def connect_to_arango():
    """Connect to ArangoDB and return database handle"""
    try:
        print("📡 Connecting to ArangoDB...")
        client = ArangoClient(hosts=ARANGO_HOST)
        
        # Connect to _system database first
        sys_db = client.db('_system', username=ARANGO_USER, password=ARANGO_PASSWORD)
        
        # Check if our database exists, create if not
        if not sys_db.has_database(ARANGO_DB):
            print(f"   Creating database: {ARANGO_DB}")
            sys_db.create_database(ARANGO_DB)
        
        # Connect to our database
        db = client.db(ARANGO_DB, username=ARANGO_USER, password=ARANGO_PASSWORD)
        print("✅ Connected successfully!")
        return db
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your .env file has correct credentials")
        print("2. Verify your password in ArangoDB Cloud")
        print("3. Make sure deployment is running")
        sys.exit(1)

def create_collections(db):
    """Create all necessary collections"""
    print("\n📦 Creating collections...")
    
    collections_created = []
    
    # Document collections
    doc_collections = ['drugs', 'compounds', 'conditions']
    for coll_name in doc_collections:
        if not db.has_collection(coll_name):
            db.create_collection(coll_name)
            collections_created.append(coll_name)
            print(f"   ✓ Created: {coll_name}")
        else:
            print(f"   ⊙ Exists: {coll_name}")
    
    # Edge collections
    edge_collections = ['drug_contains_compound', 'compound_interacts_with', 'condition_modifiers']
    for coll_name in edge_collections:
        if not db.has_collection(coll_name):
            db.create_collection(coll_name, edge=True)
            collections_created.append(coll_name)
            print(f"   ✓ Created: {coll_name} (edge)")
        else:
            print(f"   ⊙ Exists: {coll_name} (edge)")
    
    return collections_created

def create_graph(db):
    """Create the drug interaction graph"""
    print("\n🕸️  Creating graph...")
    
    graph_name = 'drug_interaction_graph'
    
    if db.has_graph(graph_name):
        print(f"   ⊙ Graph '{graph_name}' already exists")
        return
    
    # Define edge definitions
    edge_definitions = [
        {
            'edge_collection': 'drug_contains_compound',
            'from_vertex_collections': ['drugs'],
            'to_vertex_collections': ['compounds']
        },
        {
            'edge_collection': 'compound_interacts_with',
            'from_vertex_collections': ['compounds'],
            'to_vertex_collections': ['compounds']
        },
        {
            'edge_collection': 'condition_modifiers',
            'from_vertex_collections': ['compounds'],
            'to_vertex_collections': ['conditions']
        }
    ]
    
    db.create_graph(
        name=graph_name,
        edge_definitions=edge_definitions
    )
    
    print(f"   ✓ Created graph: {graph_name}")

def create_indexes(db):
    """Create indexes for better query performance"""
    print("\n⚡ Creating indexes...")
    
    # Index on drug names for search
    drugs = db.collection('drugs')
    if 'idx_drug_name' not in [idx['name'] for idx in drugs.indexes()]:
        drugs.add_hash_index(fields=['name'], unique=False, name='idx_drug_name')
        print("   ✓ Created index: drugs.name")
    
    # Index on compound names
    compounds = db.collection('compounds')
    if 'idx_compound_name' not in [idx['name'] for idx in compounds.indexes()]:
        compounds.add_hash_index(fields=['name'], unique=False, name='idx_compound_name')
        print("   ✓ Created index: compounds.name")
    
    # Index on interaction severity
    interactions = db.collection('compound_interacts_with')
    if 'idx_severity' not in [idx['name'] for idx in interactions.indexes()]:
        interactions.add_skiplist_index(fields=['severity'], unique=False, name='idx_severity')
        print("   ✓ Created index: interactions.severity")

def populate_data(db):
    """Populate database with sample data"""
    print("\n💉 Populating data...")
    
    # Insert compounds
    compounds = db.collection('compounds')
    compound_count = compounds.count()
    if compound_count == 0:
        compounds.insert_many(COMPOUNDS_DATA)
        print(f"   ✓ Inserted {len(COMPOUNDS_DATA)} compounds")
    else:
        print(f"   ⊙ Compounds already exist ({compound_count} documents)")
    
    # Insert drugs
    drugs = db.collection('drugs')
    drug_count = drugs.count()
    if drug_count == 0:
        drugs.insert_many(DRUGS_DATA)
        print(f"   ✓ Inserted {len(DRUGS_DATA)} drugs")
    else:
        print(f"   ⊙ Drugs already exist ({drug_count} documents)")
    
    # Insert drug-compound relationships
    drug_compounds = db.collection('drug_contains_compound')
    dc_count = drug_compounds.count()
    if dc_count == 0:
        drug_compounds.insert_many(DRUG_COMPOUND_EDGES)
        print(f"   ✓ Inserted {len(DRUG_COMPOUND_EDGES)} drug-compound relationships")
    else:
        print(f"   ⊙ Drug-compound relationships already exist ({dc_count} edges)")
    
    # Insert interactions
    interactions = db.collection('compound_interacts_with')
    interaction_count = interactions.count()
    if interaction_count == 0:
        interactions.insert_many(INTERACTION_EDGES)
        print(f"   ✓ Inserted {len(INTERACTION_EDGES)} interactions")
    else:
        print(f"   ⊙ Interactions already exist ({interaction_count} edges)")
    
    # Insert conditions
    conditions = db.collection('conditions')
    condition_count = conditions.count()
    if condition_count == 0:
        conditions.insert_many(CONDITIONS_DATA)
        print(f"   ✓ Inserted {len(CONDITIONS_DATA)} conditions")
    else:
        print(f"   ⊙ Conditions already exist ({condition_count} documents)")
    
    # Insert condition modifiers
    condition_mods = db.collection('condition_modifiers')
    cm_count = condition_mods.count()
    if cm_count == 0:
        condition_mods.insert_many(CONDITION_MODIFIER_EDGES)
        print(f"   ✓ Inserted {len(CONDITION_MODIFIER_EDGES)} condition modifiers")
    else:
        print(f"   ⊙ Condition modifiers already exist ({cm_count} edges)")

def print_summary(db):
    """Print database summary"""
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY")
    print("="*60)
    
    # Collection counts
    print(f"   Drugs: {db.collection('drugs').count()}")
    print(f"   Compounds: {db.collection('compounds').count()}")
    print(f"   Conditions: {db.collection('conditions').count()}")
    print(f"   Drug-Compound Links: {db.collection('drug_contains_compound').count()}")
    print(f"   Interactions: {db.collection('compound_interacts_with').count()}")
    print(f"   Condition Modifiers: {db.collection('condition_modifiers').count()}")
    
    # Interaction severity breakdown
    query = """
    FOR interaction IN compound_interacts_with
        COLLECT severity = interaction.severity WITH COUNT INTO count
        SORT severity
        RETURN {severity, count}
    """
    
    print("\n   Interactions by Severity:")
    for result in db.aql.execute(query):
        print(f"      {result['severity'].capitalize()}: {result['count']}")
    
    # Condition modifiers breakdown
    query2 = """
    FOR modifier IN condition_modifiers
        COLLECT type = modifier.modifier_type WITH COUNT INTO count
        SORT count DESC
        RETURN {type, count}
    """
    
    print("\n   Condition Modifiers by Type:")
    for result in db.aql.execute(query2):
        print(f"      {result['type'].capitalize()}: {result['count']}")
    
    print("\n" + "="*60)

def verify_setup(db):
    """Run a test query to verify everything works"""
    print("\n🧪 Running test query...")
    
    query = """
    FOR drug IN drugs
        FILTER drug._key == 'warfarin_5mg'
        FOR compound IN OUTBOUND drug drug_contains_compound
            FOR interaction IN OUTBOUND compound compound_interacts_with
                FILTER interaction.severity == 'severe'
                RETURN {
                    drug: drug.name,
                    interacts_with: interaction.name,
                    severity: interaction.severity
                }
    """
    
    try:
        results = list(db.aql.execute(query))
        print(f"   ✓ Test query successful! Found {len(results)} severe interactions for Warfarin")
        if results:
            print(f"   Example: Warfarin + {results[0]['interacts_with']}")
    except Exception as e:
        print(f"   ⚠️  Test query failed: {e}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main setup function"""
    try:
        # Connect
        db = connect_to_arango()
        
        # Create schema
        create_collections(db)
        create_graph(db)
        create_indexes(db)
        
        # Load data
        populate_data(db)
        
        # Verify
        print_summary(db)
        verify_setup(db)
        
        print("\n✨ Setup complete! Your database is ready.")
        print(f"\nNext steps:")
        print(f"1. Start your backend: cd backend && uvicorn app.main:app --reload")
        print(f"2. Start your frontend: cd frontend && npm run dev")
        print(f"3. Open http://localhost:5173 in your browser")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

