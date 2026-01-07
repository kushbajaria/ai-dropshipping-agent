import React from 'react'

interface RecommendationBadgeProps {
  recommendation: string
  probability: number
}

export const RecommendationBadge: React.FC<RecommendationBadgeProps> = ({
  recommendation,
  probability,
}) => {
  let bgColor = 'bg-red-100 border-red-300'
  let textColor = 'text-red-800'
  let progressColor = 'bg-red-500'

  if (recommendation.includes('STRONG BUY') || recommendation.includes('BUY')) {
    bgColor = 'bg-green-100 border-green-300'
    textColor = 'text-green-800'
    progressColor = 'bg-green-500'
  } else if (recommendation.includes('CONSIDER') || recommendation.includes('RISKY')) {
    bgColor = 'bg-yellow-100 border-yellow-300'
    textColor = 'text-yellow-800'
    progressColor = 'bg-yellow-500'
  }

  return (
    <div className={`border-2 rounded-lg p-6 ${bgColor}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className={`text-2xl font-bold ${textColor}`}>{recommendation}</h3>
        <div className={`text-4xl font-bold ${textColor}`}>{probability}%</div>
      </div>
      <div className="w-full bg-gray-300 rounded-full h-3 overflow-hidden">
        <div
          className={`h-full ${progressColor} transition-all duration-500`}
          style={{ width: `${probability}%` }}
        />
      </div>
      <p className={`text-sm ${textColor} mt-2`}>Success Probability</p>
    </div>
  )
}
