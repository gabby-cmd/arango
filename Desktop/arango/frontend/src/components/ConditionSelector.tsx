import { Check } from 'lucide-react';

interface ConditionSelectorProps {
  selectedConditions: string[];
  onConditionToggle: (condition: string) => void;
}

const CONDITIONS = [
  {
    key: 'kidney_disease_ckd',
    label: 'Chronic Kidney Disease (CKD)',
    description: 'Impaired kidney function'
  },
  {
    key: 'diabetes_type_2',
    label: 'Diabetes Type 2',
    description: 'Insulin resistance'
  },
  {
    key: 'liver_disease_cirrhosis',
    label: 'Liver Disease / Cirrhosis',
    description: 'Chronic liver damage'
  },
  {
    key: 'pregnancy',
    label: 'Pregnancy',
    description: 'Currently pregnant'
  },
  {
    key: 'elderly_age_65plus',
    label: 'Elderly (Age ≥65)',
    description: 'Advanced age'
  }
];

export default function ConditionSelector({
  selectedConditions,
  onConditionToggle
}: ConditionSelectorProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
      <label className="block text-sm font-medium text-gray-700 mb-3">
        Patient Conditions (Optional)
      </label>
      <div className="space-y-2">
        {CONDITIONS.map((condition) => {
          const isSelected = selectedConditions.includes(condition.key);
          return (
            <button
              key={condition.key}
              onClick={() => onConditionToggle(condition.key)}
              className={`w-full text-left px-3 py-2 rounded-md border transition-all ${
                isSelected
                  ? 'bg-blue-50 border-blue-300 ring-1 ring-blue-500'
                  : 'bg-white border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-start gap-2">
                <div
                  className={`mt-0.5 w-5 h-5 rounded flex items-center justify-center border-2 transition-all ${
                    isSelected
                      ? 'bg-blue-600 border-blue-600'
                      : 'bg-white border-gray-300'
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 text-white" />}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900 text-sm">
                    {condition.label}
                  </div>
                  <div className="text-xs text-gray-500">
                    {condition.description}
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
      {selectedConditions.length > 0 && (
        <div className="mt-3 text-xs text-gray-600 bg-blue-50 p-2 rounded">
          {selectedConditions.length} condition(s) selected - will check for contraindications
        </div>
      )}
    </div>
  );
}

