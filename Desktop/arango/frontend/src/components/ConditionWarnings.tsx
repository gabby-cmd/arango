import { AlertTriangle, AlertCircle, Info } from 'lucide-react';
import type { ConditionWarning } from '../types';

interface ConditionWarningsProps {
  warnings: ConditionWarning[];
}

export default function ConditionWarnings({ warnings }: ConditionWarningsProps) {
  if (warnings.length === 0) return null;

  const getSeverityIcon = (severity: string) => {
    return severity === 'critical' ? AlertTriangle : AlertCircle;
  };

  const getSeverityColor = (severity: string) => {
    return severity === 'critical' 
      ? 'red'
      : 'orange';
  };

  return (
    <div className="space-y-3 mb-6">
      <h3 className="text-lg font-semibold text-gray-900">
        Condition-Based Warnings ({warnings.length})
      </h3>
      
      {warnings.map((warning, index) => {
        const Icon = getSeverityIcon(warning.severity);
        const isCritical = warning.severity === 'critical';
        
        return (
          <div
            key={index}
            className={`${
              isCritical 
                ? 'bg-red-50 border-l-4 border-red-600' 
                : 'bg-orange-50 border-l-4 border-orange-600'
            } p-4 rounded-r-lg`}
          >
            <div className="flex gap-3">
              <Icon className={`w-5 h-5 ${
                isCritical ? 'text-red-600' : 'text-orange-600'
              } flex-shrink-0 mt-0.5`} />
              <div className="flex-1">
                {/* Header */}
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className={`font-bold uppercase text-sm ${
                      isCritical ? 'text-red-900' : 'text-orange-900'
                    }`}>
                      {warning.modifier_type === 'contraindication' 
                        ? 'CONTRAINDICATION' 
                        : warning.modifier_type.toUpperCase().replace('_', ' ')}
                    </h4>
                    <div className="text-sm text-gray-700 mt-1">
                      <span className="font-semibold">{warning.drug_name}</span>
                      {' + '}
                      <span className="font-semibold">{warning.condition_name}</span>
                    </div>
                  </div>
                  {warning.threshold && (
                    <div className={`text-xs px-2 py-1 rounded ${
                      isCritical ? 'bg-red-100' : 'bg-orange-100'
                    }`}>
                      {warning.threshold}
                    </div>
                  )}
                </div>

                {/* Description */}
                <p className={`text-sm mb-3 ${
                  isCritical ? 'text-red-800' : 'text-orange-800'
                }`}>
                  {warning.description}
                </p>

                {/* Clinical Management - Highlighted */}
                <div className={`rounded-lg p-3 mb-3 ${
                  isCritical 
                    ? 'bg-red-100 border border-red-200' 
                    : 'bg-orange-100 border border-orange-200'
                }`}>
                  <div className="flex items-start gap-2">
                    <Info className={`w-4 h-4 flex-shrink-0 mt-0.5 ${
                      isCritical ? 'text-red-700' : 'text-orange-700'
                    }`} />
                    <div>
                      <h5 className={`font-semibold text-sm mb-1 ${
                        isCritical ? 'text-red-900' : 'text-orange-900'
                      }`}>
                        Clinical Management
                      </h5>
                      <p className={`text-sm ${
                        isCritical ? 'text-red-800' : 'text-orange-800'
                      }`}>
                        {warning.clinical_management}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Additional Details */}
                <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-600">
                  {warning.mechanism && (
                    <div>
                      <span className="font-semibold">Mechanism:</span> {warning.mechanism}
                    </div>
                  )}
                  {warning.evidence_level && (
                    <div>
                      <span className="font-semibold">Evidence:</span> {warning.evidence_level}
                    </div>
                  )}
                  {warning.guideline && (
                    <div>
                      <span className="font-semibold">Guideline:</span> {warning.guideline}
                    </div>
                  )}
                </div>

                {/* Alternative Drugs */}
                {warning.alternative_drugs && warning.alternative_drugs.length > 0 && (
                  <div className="mt-2 text-sm">
                    <span className={`font-semibold ${
                      isCritical ? 'text-red-900' : 'text-orange-900'
                    }`}>Alternatives:</span>
                    <span className={`ml-1 ${
                      isCritical ? 'text-red-800' : 'text-orange-800'
                    }`}>
                      {warning.alternative_drugs.join(', ')}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

