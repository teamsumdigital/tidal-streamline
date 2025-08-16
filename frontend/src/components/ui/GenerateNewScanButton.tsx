/**
 * Generate New Market Scan Button Component
 * Provides quick access to create a new market scan from results page
 */

import React from 'react'
import { Link } from 'react-router-dom'

interface GenerateNewScanButtonProps {
  className?: string
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}

export const GenerateNewScanButton: React.FC<GenerateNewScanButtonProps> = ({
  className = '',
  variant = 'primary',
  size = 'md'
}) => {
  const baseClasses = "inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 group"
  
  const variantClasses = {
    primary: "bg-[#7B61FF] text-white hover:bg-[#6B51E5] hover:shadow-lg",
    secondary: "bg-white text-[#7B61FF] border border-[#7B61FF] hover:bg-[#7B61FF]/5",
    outline: "bg-transparent text-[#7B61FF] border border-[#E5E5E7] hover:border-[#7B61FF] hover:bg-[#7B61FF]/5"
  }
  
  const sizeClasses = {
    sm: "px-3 py-2 text-sm",
    md: "px-4 py-3 text-sm",
    lg: "px-6 py-4 text-base"
  }

  return (
    <Link
      to="/"
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      <span className="mr-2">💰</span>
      New Payroll Calculation
      <span className="ml-2 group-hover:translate-x-0.5 transition-transform">→</span>
    </Link>
  )
}

/**
 * Quick Scan Button with Pre-filled Data
 * Allows users to quickly create a similar scan with modified parameters
 */

interface QuickScanButtonProps {
  existingScanData?: {
    job_title?: string
    company_domain?: string
    job_description?: string
  }
  className?: string
}

export const QuickScanButton: React.FC<QuickScanButtonProps> = ({
  existingScanData,
  className = ''
}) => {
  const handleQuickScan = () => {
    // Store existing data in localStorage for pre-filling the form
    if (existingScanData) {
      localStorage.setItem('tidal_prefill_scan', JSON.stringify({
        job_title: existingScanData.job_title || '',
        company_domain: existingScanData.company_domain || '',
        job_description: existingScanData.job_description || '',
        prefilled: true
      }))
    }
    
    // Navigate to home page (the form will auto-fill from localStorage)
    window.location.href = '/'
  }

  return (
    <button
      onClick={handleQuickScan}
      className={`inline-flex items-center justify-center w-full bg-[#00C6A2] text-white font-semibold px-4 py-3 rounded-lg hover:bg-[#00B096] transition-colors group ${className}`}
    >
      <span className="mr-2">⚡</span>
      Quick Similar Calculation
      <span className="ml-2 group-hover:translate-x-0.5 transition-transform">+</span>
    </button>
  )
}

/**
 * Market Scan Actions Component
 * Combines multiple scan-related actions in a clean layout
 */

interface MarketScanActionsProps {
  existingScanData?: {
    job_title?: string
    company_domain?: string
    job_description?: string
  }
  className?: string
}

export const MarketScanActions: React.FC<MarketScanActionsProps> = ({
  existingScanData,
  className = ''
}) => {
  return (
    <div className={`space-y-3 ${className}`}>
      {/* Primary Action - New Calculation */}
      <GenerateNewScanButton variant="primary" />
      
      {/* Secondary Action - Quick Similar Calculation */}
      {existingScanData && (
        <QuickScanButton existingScanData={existingScanData} />
      )}
      
      {/* Tertiary Action - Browse Previous Results */}
      <Link
        to="/admin"
        className="inline-flex items-center justify-center w-full text-[#555555] text-sm hover:text-[#1A1A1A] transition-colors"
      >
        <span className="mr-2">📊</span>
        View Past Results
      </Link>
    </div>
  )
}