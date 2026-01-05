import { useState } from 'react';
import { Shield } from 'lucide-react';
import DrugSearch from './components/DrugSearch';
import InteractionResults from './components/InteractionResults';
import ConditionSelector from './components/ConditionSelector';
import ConditionWarnings from './components/ConditionWarnings';
import type { Drug, InteractionResult, ConditionWarning } from './types';

function App() {
  const [selectedDrugs, setSelectedDrugs] = useState<Drug[]>([]);
  const [interactionResult, setInteractionResult] = useState<InteractionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedConditions, setSelectedConditions] = useState<string[]>([]);
  const [conditionWarnings, setConditionWarnings] = useState<ConditionWarning[]>([]);

  const handleDrugSelect = (drug: Drug) => {
    if (!selectedDrugs.find(d => d._key === drug._key)) {
      setSelectedDrugs([...selectedDrugs, drug]);
    }
  };

  const handleDrugRemove = (drugKey: string) => {
    setSelectedDrugs(selectedDrugs.filter(d => d._key !== drugKey));
    // Clear results when drugs are removed
    if (selectedDrugs.length <= 2) {
      setInteractionResult(null);
    }
  };

  const handleCheckInteractions = async () => {
    if (selectedDrugs.length < 2) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const drugKeys = selectedDrugs.map(d => d._key);
      const { checkInteractions, checkConditionWarnings } = await import('./services/api');
      
      // Check drug-drug interactions
      const interactionResult = await checkInteractions(drugKeys);
      setInteractionResult(interactionResult);
      
      // Check condition-based warnings if conditions are selected
      if (selectedConditions.length > 0) {
        const warningsResult = await checkConditionWarnings(drugKeys, selectedConditions);
        setConditionWarnings(warningsResult.warnings);
      } else {
        setConditionWarnings([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check interactions');
      setInteractionResult(null);
      setConditionWarnings([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleConditionToggle = (condition: string) => {
    setSelectedConditions(prev =>
      prev.includes(condition)
        ? prev.filter(c => c !== condition)
        : [...prev, condition]
    );
    // Clear condition warnings when conditions change
    setConditionWarnings([]);
  };

  const handleDemoScenario = (drugs: Drug[]) => {
    setSelectedDrugs(drugs);
    setInteractionResult(null);
    setError(null);
    setConditionWarnings([]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Drug Interaction Checker</h1>
              <p className="text-sm text-gray-500">Professional medication safety analysis tool</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Drug Search */}
          <div className="space-y-4">
            <DrugSearch
              selectedDrugs={selectedDrugs}
              onDrugSelect={handleDrugSelect}
              onDrugRemove={handleDrugRemove}
              onCheckInteractions={handleCheckInteractions}
              onDemoScenario={handleDemoScenario}
              isLoading={isLoading}
            />
            <ConditionSelector
              selectedConditions={selectedConditions}
              onConditionToggle={handleConditionToggle}
            />
          </div>

          {/* Right Panel - Results */}
          <div className="space-y-6">
            {conditionWarnings.length > 0 && (
              <ConditionWarnings warnings={conditionWarnings} />
            )}
            <InteractionResults
              result={interactionResult}
              isLoading={isLoading}
              error={error}
              selectedDrugsCount={selectedDrugs.length}
            />
          </div>
        </div>
      </main>

      {/* Footer Disclaimer */}
      <footer className="mt-12 pb-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-xs text-gray-500 text-center">
            Disclaimer: This tool is for educational purposes only. Always consult a healthcare provider before making medication changes.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
