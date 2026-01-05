/**
 * TypeScript types for the Drug Interaction Checker application
 */

export interface Drug {
  _key: string;
  name: string;
  generic_name: string;
  brand_names: string[];
  strength: string;
  dosage_form: string;
  drug_class: string;
  indication: string[];
}

export interface Interaction {
  compound_1: string;
  compound_2: string;
  affected_drugs: string[];
  severity: 'severe' | 'moderate' | 'minor';
  interaction_type: string;
  description: string;
  mechanism: string;
  clinical_management: string;
  evidence_level: string;
  onset: string;
  documentation: string;
}

export interface InteractionResult {
  interactions_found: number;
  highest_severity: string | null;
  query_time_ms: number;
  interactions: Interaction[];
}

export interface Stats {
  total_drugs: number;
  total_compounds: number;
  total_interactions: number;
  interactions_by_severity: {
    severe?: number;
    moderate?: number;
    minor?: number;
  };
}

export type SeverityFilter = 'all' | 'severe' | 'moderate' | 'minor';

export interface DemoScenario {
  name: string;
  description: string;
  drug_keys: string[];
}

export interface ConditionWarning {
  drug_name: string;
  drug_key: string;
  compound_name: string;
  condition_name: string;
  condition_key: string;
  modifier_type: 'contraindication' | 'warning' | 'dose_adjustment' | 'monitoring_required';
  severity: 'critical' | 'caution';
  threshold?: string;
  description: string;
  mechanism?: string;
  clinical_management: string;
  evidence_level?: string;
  guideline?: string;
  monitoring?: string;
  alternative_drugs?: string[];
}

export interface ConditionWarningsResult {
  warnings_found: number;
  query_time_ms: number;
  warnings: ConditionWarning[];
}

