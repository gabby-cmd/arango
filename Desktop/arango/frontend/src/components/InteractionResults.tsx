import { useState } from 'react';
import { Shield, Loader2, AlertCircle } from 'lucide-react';
import InteractionCard from './InteractionCard';
import type { InteractionResult, SeverityFilter } from '../types';

interface InteractionResultsProps {
  result: InteractionResult | null;
  isLoading: boolean;
  error: string | null;
  selectedDrugsCount: number;
}

export default function InteractionResults({
  result,
  isLoading,
  error,
  selectedDrugsCount,
}: InteractionResultsProps) {
  const [severityFilter, setSeverityFilter] = useState<SeverityFilter>('all');

  // Empty state - show when no result and not loading/error
  if (!result && !isLoading && !error) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Shield className="w-16 h-16 text-gray-300 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Analyze</h3>
          <p className="text-sm text-gray-500 max-w-sm">
            {selectedDrugsCount === 0 
              ? "Add at least two medications and click 'Check Interactions' to analyze potential drug interactions."
              : selectedDrugsCount === 1
              ? "Add at least one more medication to check for interactions."
              : `You have ${selectedDrugsCount} medications selected. Click 'Check Interactions' to analyze potential drug interactions.`
            }
          </p>
        </div>
      </div>
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <div className="flex flex-col items-center justify-center py-12">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
          <p className="text-gray-600 font-medium">Analyzing interactions...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Error</h3>
          <p className="text-sm text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  // No results state
  if (result && result.interactions_found === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Shield className="w-16 h-16 text-green-500 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Interactions Found</h3>
          <p className="text-sm text-gray-500">
            No known interactions detected between the selected medications.
          </p>
          {result.query_time_ms && (
            <p className="text-xs text-gray-400 mt-2">
              Analyzed in {result.query_time_ms}ms
            </p>
          )}
        </div>
      </div>
    );
  }

  // Results state - this should only be reached if result exists
  if (!result) {
    // Fallback - should not reach here, but show ready state
    return (
      <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Shield className="w-16 h-16 text-gray-300 mb-4" />
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Analyze</h3>
          <p className="text-sm text-gray-500 max-w-sm">
            Click 'Check Interactions' to analyze potential drug interactions.
          </p>
        </div>
      </div>
    );
  }

  // Filter interactions by severity
  const filteredInteractions = result.interactions.filter((interaction) => {
    if (severityFilter === 'all') return true;
    return interaction.severity === severityFilter;
  });

  // Count interactions by severity
  const counts = {
    all: result.interactions.length,
    severe: result.interactions.filter(i => i.severity === 'severe').length,
    moderate: result.interactions.filter(i => i.severity === 'moderate').length,
    minor: result.interactions.filter(i => i.severity === 'minor').length,
  };

  const getSeverityBadgeColor = (severity: string) => {
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

  return (
    <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      {/* Summary Card */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-900">Interaction Analysis</h3>
          {result.highest_severity && (
            <span
              className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityBadgeColor(result.highest_severity)}`}
            >
              {result.highest_severity.toUpperCase()}
            </span>
          )}
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-2xl font-bold text-gray-900">{result.interactions_found}</p>
            <p className="text-xs text-gray-500">Total Interactions</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">{result.query_time_ms}ms</p>
            <p className="text-xs text-gray-500">Query Time</p>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-4 border-b border-gray-200">
        {(['all', 'severe', 'moderate', 'minor'] as SeverityFilter[]).map((filter) => (
          <button
            key={filter}
            onClick={() => setSeverityFilter(filter)}
            className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 ${
              severityFilter === filter
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {filter.charAt(0).toUpperCase() + filter.slice(1)}
            {counts[filter] > 0 && (
              <span className="ml-2 px-2 py-0.5 bg-gray-100 rounded-full text-xs">
                {counts[filter]}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Interactions List */}
      <div className="space-y-4 max-h-[600px] overflow-y-auto">
        {filteredInteractions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No {severityFilter === 'all' ? '' : severityFilter} interactions found.</p>
          </div>
        ) : (
          filteredInteractions.map((interaction, index) => (
            <InteractionCard key={index} interaction={interaction} />
          ))
        )}
      </div>
    </div>
  );
}

