import { useState } from 'react';
import { ChevronDown, ChevronUp, AlertTriangle, Info } from 'lucide-react';
import type { Interaction } from '../types';

interface InteractionCardProps {
  interaction: Interaction;
}

export default function InteractionCard({ interaction }: InteractionCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'severe':
        return 'bg-red-600 text-white';
      case 'moderate':
        return 'bg-orange-500 text-white';
      case 'minor':
        return 'bg-yellow-400 text-gray-900';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const getInteractionTypeColor = (type: string) => {
    if (type.includes('pharmacodynamic')) return 'bg-purple-100 text-purple-700';
    if (type.includes('pharmacokinetic')) return 'bg-blue-100 text-blue-700';
    return 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle
              className={`w-5 h-5 ${
                interaction.severity === 'severe'
                  ? 'text-red-600'
                  : interaction.severity === 'moderate'
                  ? 'text-orange-500'
                  : 'text-yellow-500'
              }`}
            />
            <h4 className="font-semibold text-gray-900">
              {interaction.compound_1} ↔ {interaction.compound_2}
            </h4>
          </div>
          <div className="flex flex-wrap gap-2 mb-2">
            <span
              className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(interaction.severity)}`}
            >
              {interaction.severity.toUpperCase()}
            </span>
            <span
              className={`px-2 py-1 rounded text-xs font-medium ${getInteractionTypeColor(interaction.interaction_type)}`}
            >
              {interaction.interaction_type}
            </span>
          </div>
          {interaction.affected_drugs.length > 0 && (
            <div className="text-sm text-gray-600">
              <span className="font-medium">Affected drugs:</span>{' '}
              {interaction.affected_drugs.join(', ')}
            </div>
          )}
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
          aria-label={isExpanded ? 'Collapse' : 'Expand'}
        >
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-500" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-500" />
          )}
        </button>
      </div>

      {/* Description (always visible) */}
      <div className="mb-3">
        <p className="text-sm text-gray-700 leading-relaxed">{interaction.description}</p>
      </div>

      {/* Expandable Details */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-gray-200 space-y-4 animate-in fade-in slide-in-from-top-2">
          {/* Mechanism */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Info className="w-4 h-4 text-gray-500" />
              <h5 className="text-sm font-semibold text-gray-900">Mechanism of Action</h5>
            </div>
            <p className="text-sm text-gray-600 pl-6">{interaction.mechanism}</p>
          </div>

          {/* Clinical Management (highlighted) */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded">
            <h5 className="text-sm font-semibold text-blue-900 mb-1">Clinical Management</h5>
            <p className="text-sm text-blue-800">{interaction.clinical_management}</p>
          </div>

          {/* Evidence & Onset */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Evidence Level:</span>{' '}
              <span className="text-gray-600">{interaction.evidence_level}</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Onset:</span>{' '}
              <span className="text-gray-600">{interaction.onset}</span>
            </div>
            <div className="col-span-2">
              <span className="font-medium text-gray-700">Documentation:</span>{' '}
              <span className="text-gray-600">{interaction.documentation}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

