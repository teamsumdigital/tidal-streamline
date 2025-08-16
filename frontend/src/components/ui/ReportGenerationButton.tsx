/**
 * Report Generation Button Component
 * Handles professional Tidal report generation with progress states
 */

import React, { useState } from 'react'
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
  const [state, setState] = useState<ReportGenerationState>({ status: 'idle' })

  const generateReport = async () => {
    setState({ status: 'generating', progress: 10 })

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setState(prev => ({
          ...prev,
          progress: Math.min((prev.progress || 10) + 15, 90)
        }))
      }, 800)

      const response = await apiService.generateReport({
        scan_id: scanId,
        client_name: clientName,
        report_format: 'canva',
        include_candidate_profiles: true
      })

      clearInterval(progressInterval)

      if (response.success) {
        setState({
          status: 'success',
          reportUrl: response.download_url,
          previewUrl: response.preview_url,
          reportId: response.report_id,
          progress: 100
        })

        // Auto-download after brief success display
        setTimeout(() => {
          if (response.download_url) {
            window.open(response.download_url, '_blank')
          }
        }, 1500)
      } else {
        throw new Error(response.error || 'Report generation failed')
      }
    } catch (error) {
      setState({
        status: 'error',
        error: error instanceof Error ? error.message : 'Failed to generate report'
      })
    }
  }

  const resetState = () => {
    setState({ status: 'idle' })
  }

  // Idle State - Ready to Generate
  if (state.status === 'idle') {
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

  // Generating State - Show Progress
  if (state.status === 'generating') {
    return (
      <div className={`bg-white rounded-lg p-4 ${className}`}>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-[#7B61FF] border-t-transparent rounded-full animate-spin"></div>
            <span className="text-[#7B61FF] font-medium text-sm">Generating Market Scan...</span>
          </div>
          <span className="text-xs text-[#555555]">{state.progress}%</span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
          <div 
            className="bg-gradient-to-r from-[#7B61FF] to-[#9F7FFF] h-2 rounded-full transition-all duration-500"
            style={{ width: `${state.progress}%` }}
          ></div>
        </div>
        
        <div className="text-xs text-[#555555] space-y-1">
          {state.progress && state.progress < 30 && (
            <div className="flex items-center gap-2">
              <span className="w-1 h-1 bg-[#7B61FF] rounded-full animate-pulse"></span>
              Mapping data to Tidal template...
            </div>
          )}
          {state.progress && state.progress >= 30 && state.progress < 60 && (
            <div className="flex items-center gap-2">
              <span className="w-1 h-1 bg-[#7B61FF] rounded-full animate-pulse"></span>
              Creating branded design elements...
            </div>
          )}
          {state.progress && state.progress >= 60 && state.progress < 90 && (
            <div className="flex items-center gap-2">
              <span className="w-1 h-1 bg-[#7B61FF] rounded-full animate-pulse"></span>
              Generating final report pages...
            </div>
          )}
          {state.progress && state.progress >= 90 && (
            <div className="flex items-center gap-2">
              <span className="w-1 h-1 bg-green-500 rounded-full"></span>
              Finalizing download link...
            </div>
          )}
        </div>
      </div>
    )
  }

  // Success State - Report Ready
  if (state.status === 'success') {
    return (
      <div className={`bg-white rounded-lg p-4 ${className}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-green-500">✅</span>
          <span className="text-green-700 font-medium text-sm">Market Scan Generated!</span>
        </div>
        
        <div className="space-y-2">
          {state.previewUrl && (
            <button
              onClick={() => window.open(state.previewUrl, '_blank')}
              className="flex items-center justify-center w-full bg-[#7B61FF]/10 text-[#7B61FF] font-medium px-3 py-2 rounded text-sm hover:bg-[#7B61FF]/20 transition-colors"
            >
              <span className="mr-2">👁️</span>
              Preview Market Scan
            </button>
          )}
          
          <button
            onClick={() => state.reportUrl && window.open(state.reportUrl, '_blank')}
            className="flex items-center justify-center w-full bg-[#7B61FF] text-white font-medium px-3 py-2 rounded text-sm hover:bg-[#6B51E5] transition-colors"
          >
            <span className="mr-2">⬇️</span>
            Download Market Scan
          </button>
          
          <button
            onClick={resetState}
            className="flex items-center justify-center w-full text-[#555555] text-xs hover:text-[#1A1A1A] transition-colors"
          >
            Generate New Market Scan
          </button>
        </div>
      </div>
    )
  }

  // Error State - Show Error Message
  if (state.status === 'error') {
    return (
      <div className={`bg-white rounded-lg p-4 ${className}`}>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-red-500">❌</span>
          <span className="text-red-700 font-medium text-sm">Market Scan Failed</span>
        </div>
        
        <p className="text-red-600 text-xs mb-3">
          {state.error || 'Unable to generate market scan. Please try again.'}
        </p>
        
        <div className="space-y-2">
          <button
            onClick={generateReport}
            className="flex items-center justify-center w-full bg-[#7B61FF] text-white font-medium px-3 py-2 rounded text-sm hover:bg-[#6B51E5] transition-colors"
          >
            <span className="mr-2">🔄</span>
            Try Again
          </button>
          
          <button
            onClick={resetState}
            className="flex items-center justify-center w-full text-[#555555] text-xs hover:text-[#1A1A1A] transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    )
  }

  return null
}