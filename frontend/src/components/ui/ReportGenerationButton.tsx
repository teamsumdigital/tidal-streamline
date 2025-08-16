/**
 * Report Generation Button Component
 * Handles professional Tidal report generation with progress states
 */

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiService } from '../../services/api'

interface ReportGenerationButtonProps {
  scanId: string
  clientName: string
  roleTitle: string
  className?: string
}

interface ReportGenerationState {
  status: 'idle' | 'generating' | 'success' | 'error'
  reportUrl?: string
  previewUrl?: string
  reportId?: string
  error?: string
  progress?: number
}

export const ReportGenerationButton: React.FC<ReportGenerationButtonProps> = ({
  scanId,
  clientName,
  roleTitle,
  className = ''
}) => {
  const navigate = useNavigate()
  const [state, setState] = useState<ReportGenerationState>({ status: 'idle' })

  const generateReport = () => {
    // Navigate directly to data export page
    navigate(`/scan/${scanId}/export`)
  }

  // Always show the simple button that navigates to export page
  return (
    <button
      onClick={generateReport}
      className={`inline-flex items-center justify-center w-full bg-white text-[#7B61FF] font-semibold px-4 py-3 rounded-lg hover:bg-gray-50 transition-all duration-200 group ${className}`}
    >
      <span className="mr-2">📊</span>
      Generate Report
      <span className="ml-2 group-hover:translate-x-0.5 transition-transform">→</span>
    </button>
  )
}