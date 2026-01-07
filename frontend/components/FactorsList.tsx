import React from 'react'

interface FactorsListProps {
  factors: string[]
  warnings: string[]
}

export const FactorsList: React.FC<FactorsListProps> = ({ factors, warnings }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Strengths */}
      {factors.length > 0 && (
        <div className="bg-green-50 rounded-lg p-6 border border-green-200">
          <h3 className="text-lg font-bold text-green-800 mb-4">✅ Strengths</h3>
          <ul className="space-y-3">
            {factors.map((factor, idx) => (
              <li key={idx} className="text-green-700 flex items-start">
                <span className="mr-3">•</span>
                <span>{factor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="bg-red-50 rounded-lg p-6 border border-red-200">
          <h3 className="text-lg font-bold text-red-800 mb-4">⚠️ Warnings</h3>
          <ul className="space-y-3">
            {warnings.map((warning, idx) => (
              <li key={idx} className="text-red-700 flex items-start">
                <span className="mr-3">•</span>
                <span>{warning}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
