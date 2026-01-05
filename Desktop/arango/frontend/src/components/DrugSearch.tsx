import { useState, useEffect, useRef } from 'react';
import { Search, X, Zap, Loader2, Pill } from 'lucide-react';
import { searchDrugs, getDrugByKey } from '../services/api';
import type { Drug, DemoScenario } from '../types';

interface DrugSearchProps {
  selectedDrugs: Drug[];
  onDrugSelect: (drug: Drug) => void;
  onDrugRemove: (drugKey: string) => void;
  onCheckInteractions: () => void;
  onDemoScenario: (drugs: Drug[]) => void;
  isLoading: boolean;
}

const DEMO_SCENARIOS: DemoScenario[] = [
  {
    name: 'Safe Combination',
    description: 'Lisinopril, Metformin, Atorvastatin',
    drug_keys: ['lisinopril_10mg', 'metformin_1000mg', 'atorvastatin_40mg'],
  },
  {
    name: 'Dangerous Combo',
    description: 'Warfarin + Aspirin + Ibuprofen',
    drug_keys: ['warfarin_5mg', 'aspirin_325mg', 'ibuprofen_200mg'],
  },
  {
    name: 'Moderate Risk',
    description: 'Sertraline + Ibuprofen + Tramadol',
    drug_keys: ['sertraline_50mg', 'ibuprofen_200mg', 'tramadol_50mg'],
  },
  {
    name: 'Complex Polypharmacy',
    description: '5 medications with multiple interactions',
    drug_keys: ['warfarin_5mg', 'metoprolol_50mg', 'furosemide_40mg', 'digoxin_0_25mg', 'atorvastatin_40mg'],
  },
];

const getDrugClassColor = (drugClass: string): string => {
  const colors: Record<string, string> = {
    anticoagulant: 'bg-blue-600',
    nsaid: 'bg-red-500',
    antibiotic: 'bg-yellow-500',
    ssri: 'bg-purple-500',
    beta_blocker: 'bg-indigo-500',
    biguanide: 'bg-green-600',
    statin: 'bg-pink-500',
    ace_inhibitor: 'bg-teal-500',
    antiplatelet: 'bg-orange-500',
    calcium_channel_blocker: 'bg-cyan-500',
    loop_diuretic: 'bg-emerald-500',
    cardiac_glycoside: 'bg-rose-500',
    long_acting_insulin: 'bg-violet-500',
    sulfonylurea: 'bg-amber-500',
    penicillin: 'bg-sky-500',
    macrolide: 'bg-lime-500',
    fluoroquinolone: 'bg-fuchsia-500',
    analgesic: 'bg-stone-500',
    opioid_analgesic: 'bg-red-600',
    benzodiazepine: 'bg-slate-500',
  };
  return colors[drugClass.toLowerCase()] || 'bg-gray-500';
};

export default function DrugSearch({
  selectedDrugs,
  onDrugSelect,
  onDrugRemove,
  onCheckInteractions,
  onDemoScenario,
  isLoading,
}: DrugSearchProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Drug[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [demoScenarioValue, setDemoScenarioValue] = useState('');
  const searchContainerRef = useRef<HTMLDivElement>(null);

  // Debounced search
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setShowResults(false);
      return;
    }

    const timeoutId = setTimeout(async () => {
      setIsSearching(true);
      try {
        const results = await searchDrugs(searchQuery);
        setSearchResults(results);
        setShowResults(true);
      } catch (error) {
        console.error('Search error:', error);
        setSearchResults([]);
      } finally {
        setIsSearching(false);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchQuery]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setShowResults(false);
      }
    };

    if (showResults) {
      // Use click instead of mousedown to avoid interfering with dropdown clicks
      document.addEventListener('click', handleClickOutside, true);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside, true);
    };
  }, [showResults]);

  const handleDemoLoad = async (scenario: DemoScenario) => {
    try {
      const drugs: Drug[] = [];
      
      for (const key of scenario.drug_keys) {
        try {
          const drug = await getDrugByKey(key);
          drugs.push(drug);
        } catch (error) {
          console.error(`Could not find drug with key: ${key}`, error);
        }
      }
      
      if (drugs.length > 0) {
        onDemoScenario(drugs);
        setSearchQuery(''); // Clear search
        setShowResults(false);
      } else {
        console.error('No drugs found for demo scenario');
      }
    } catch (error) {
      console.error('Failed to load demo scenario:', error);
    }
  };

  return (
    <div className="space-y-4">
      {/* Demo Scenarios */}
      <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Demo Scenarios
        </label>
        <select
          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white cursor-pointer"
          value={demoScenarioValue}
          onChange={(e) => {
            const selectedValue = e.target.value;
            setDemoScenarioValue(selectedValue);
            const scenario = DEMO_SCENARIOS.find(s => s.name === selectedValue);
            if (scenario) {
              handleDemoLoad(scenario);
            }
            // Reset to default after a short delay to allow the selection to be visible
            setTimeout(() => {
              setDemoScenarioValue('');
            }, 100);
          }}
        >
          <option value="">Select a demo scenario...</option>
          {DEMO_SCENARIOS.map((scenario) => (
            <option key={scenario.name} value={scenario.name}>
              {scenario.name} - {scenario.description}
            </option>
          ))}
        </select>
      </div>

      {/* Add Medications Card */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">Add Medications</h2>
        </div>

        {/* Search Input */}
        <div className="relative mb-4" ref={searchContainerRef}>
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 z-10" />
          <input
            type="text"
            placeholder="Search medications..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 relative z-10"
          />
          {isSearching && (
            <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 animate-spin z-10" />
          )}
          
          {/* Search Results Dropdown */}
          {showResults && searchResults.length > 0 && (
            <div 
              className="absolute z-[100] w-full mt-1 bg-white border-2 border-blue-200 rounded-md shadow-xl max-h-60 overflow-y-auto"
              style={{ top: '100%' }}
              onClick={(e) => {
                e.stopPropagation();
              }}
              onMouseDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
              }}
            >
              {searchResults.map((drug) => {
                const isDisabled = selectedDrugs.some(d => d._key === drug._key);
                return (
                  <button
                    key={drug._key}
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      if (!isDisabled) {
                        onDrugSelect(drug);
                        setSearchQuery('');
                        setShowResults(false);
                      }
                    }}
                    onMouseDown={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      if (!isDisabled) {
                        onDrugSelect(drug);
                        setSearchQuery('');
                        setShowResults(false);
                      }
                    }}
                    className={`w-full text-left px-4 py-3 transition-colors border-b border-gray-100 last:border-b-0 ${
                      isDisabled 
                        ? 'opacity-50 cursor-not-allowed bg-gray-50' 
                        : 'hover:bg-blue-100 active:bg-blue-200 cursor-pointer'
                    }`}
                    disabled={isDisabled}
                    style={{ pointerEvents: isDisabled ? 'none' : 'auto' }}
                  >
                    <div className="font-medium text-gray-900">{drug.name}</div>
                    <div className="text-sm text-gray-500">{drug.generic_name} • {drug.strength}</div>
                  </button>
                );
              })}
            </div>
          )}
          
          {/* Show message when searching but no results */}
          {showResults && searchResults.length === 0 && searchQuery.trim() && !isSearching && (
            <div className="absolute z-[100] w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg p-4 text-sm text-gray-500">
              No medications found for "{searchQuery}"
            </div>
          )}
        </div>

        {/* Selected Drugs */}
        {selectedDrugs.length > 0 ? (
          <div className="space-y-2 mb-4">
            {selectedDrugs.map((drug) => (
              <div
                key={drug._key}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-md border border-gray-200"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-medium text-gray-900">{drug.name}</span>
                    <span className="text-sm text-gray-500">{drug.strength}</span>
                  </div>
                  <span
                    className={`inline-block px-2 py-0.5 text-xs font-medium text-white rounded ${getDrugClassColor(drug.drug_class)}`}
                  >
                    {drug.drug_class}
                  </span>
                </div>
                <button
                  onClick={() => onDrugRemove(drug._key)}
                  className="ml-2 p-1 hover:bg-gray-200 rounded transition-colors"
                  aria-label="Remove drug"
                >
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-gray-400">
            <Pill className="w-12 h-12 mb-2" />
            <p className="text-sm font-medium">No medications selected</p>
            <p className="text-xs mt-1">Search and add medications above</p>
          </div>
        )}

        {/* Check Interactions Button */}
        <button
          onClick={onCheckInteractions}
          disabled={selectedDrugs.length < 2 || isLoading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Checking Interactions...
            </>
          ) : (
            'Check Interactions'
          )}
        </button>
      </div>
    </div>
  );
}

