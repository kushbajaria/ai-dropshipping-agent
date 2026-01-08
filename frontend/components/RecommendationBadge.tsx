import React from 'react'

interface RecommendationBadgeProps {
  recommendation: string
  probability: number
}

export const RecommendationBadge: React.FC<RecommendationBadgeProps> = ({
  recommendation,
  probability,
}) => {
  let bgColor = 'bg-red-50 border-red-200'
  let textColor = 'text-red-900'
  let badgeColor = 'text-red-600'
  let icon = '🔴'
  let progressColor = 'bg-red-500'

  if (recommendation.includes('STRONG BUY') || recommendation.includes('EXCELLENT')) {
    bgColor = 'bg-emerald-50 border-emerald-200'
    textColor = 'text-emerald-900'
    badgeColor = 'text-emerald-600'
    icon = '🟢'
    progressColor = 'bg-emerald-500'
  } else if (recommendation.includes('BUY') || recommendation.includes('Good')) {
    bgColor = 'bg-emerald-50 border-emerald-200'
    textColor = 'text-emerald-900'
    badgeColor = 'text-emerald-600'
    icon = '🟢'
    progressColor = 'bg-emerald-500'
  } else if (recommendation.includes('CONSIDER') || recommendation.includes('Acceptable')) {
    bgColor = 'bg-amber-50 border-amber-200'
    textColor = 'text-amber-900'
    badgeColor = 'text-amber-600'
    icon = '🟡'
    progressColor = 'bg-amber-500'
  } else if (recommendation.includes('RISKY')) {
    bgColor = 'bg-orange-50 border-orange-200'
    textColor = 'text-orange-900'
    badgeColor = 'text-orange-600'
    icon = '⚠️'
    progressColor = 'bg-orange-500'
  }

  return (
    <div className={`border-2 rounded-2xl p-8 ${bgColor}`}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className={`text-sm font-semibold ${badgeColor} uppercase mb-1`}>Recommendation</p>
          <h2 className={`text-3xl font-bold ${textColor}`}>
            {icon} {recommendation}
          </h2>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-600 uppercase mb-1">Success Probability</p>
          <p className={`text-5xl font-bold ${badgeColor}`}>{probability}%</p>
        </div>
      </div>
      <div className="w-full bg-slate-300 rounded-full h-3 overflow-hidden">
        <div
          className={`h-full ${progressColor} transition-all duration-500`}
          style={{ width: `${probability}%` }}
        />
      </div>
      <p className={`text-xs text-slate-600 mt-3`}>Based on profit analysis, competition, and market trends</p>
    </div>
  )
}

