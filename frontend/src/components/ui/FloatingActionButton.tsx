/**
 * Floating Action Button Component
 * Provides quick access to primary actions from anywhere on the page
 */

import React, { useState } from 'react'
import { Link } from 'react-router-dom'

interface FloatingActionButtonProps {
  className?: string
}

export const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({
  className = ''
}) => {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className={`fixed bottom-6 right-6 z-50 ${className}`}>
      {/* Expanded Actions */}
      {isExpanded && (
        <div className="absolute bottom-16 right-0 bg-white rounded-lg shadow-2xl border border-[#E5E5E7] p-3 space-y-2 min-w-[200px] animate-slideInUp">
          <Link
            to="/"
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#F7F7F9] transition-colors group"
            onClick={() => setIsExpanded(false)}
          >
            <div className="w-8 h-8 bg-[#7B61FF]/10 rounded-lg flex items-center justify-center">
              <span className="text-sm">🔍</span>
            </div>
            <div>
              <div className="font-medium text-[#1A1A1A] text-sm">New Market Scan</div>
              <div className="text-xs text-[#555555]">Create fresh analysis</div>
            </div>
          </Link>
          
          <Link
            to="/admin"
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#F7F7F9] transition-colors group"
            onClick={() => setIsExpanded(false)}
          >
            <div className="w-8 h-8 bg-[#00C6A2]/10 rounded-lg flex items-center justify-center">
              <span className="text-sm">📊</span>
            </div>
            <div>
              <div className="font-medium text-[#1A1A1A] text-sm">View All Scans</div>
              <div className="text-xs text-[#555555]">Browse history</div>
            </div>
          </Link>
          
          <a
            href="mailto:connect@hiretidal.com?subject=New Market Scan Request"
            className="flex items-center gap-3 p-3 rounded-lg hover:bg-[#F7F7F9] transition-colors group"
            onClick={() => setIsExpanded(false)}
          >
            <div className="w-8 h-8 bg-[#FF6B6B]/10 rounded-lg flex items-center justify-center">
              <span className="text-sm">💬</span>
            </div>
            <div>
              <div className="font-medium text-[#1A1A1A] text-sm">Contact Expert</div>
              <div className="text-xs text-[#555555]">Get personal help</div>
            </div>
          </a>
        </div>
      )}

      {/* Main FAB */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className={`w-14 h-14 bg-[#7B61FF] text-white rounded-full shadow-2xl hover:bg-[#6B51E5] transition-all duration-200 flex items-center justify-center group ${
          isExpanded ? 'rotate-45' : 'hover:scale-110'
        }`}
      >
        {isExpanded ? (
          <span className="text-2xl">×</span>
        ) : (
          <span className="text-xl group-hover:scale-110 transition-transform">+</span>
        )}
      </button>
    </div>
  )
}

/**
 * Simple Floating New Scan Button
 * Quick access to create a new market scan
 */

export const FloatingNewScanButton: React.FC<{ className?: string }> = ({
  className = ''
}) => {
  return (
    <Link
      to="/"
      className={`fixed bottom-6 right-6 z-50 w-14 h-14 bg-[#7B61FF] text-white rounded-full shadow-2xl hover:bg-[#6B51E5] hover:scale-110 transition-all duration-200 flex items-center justify-center group ${className}`}
      title="Create New Market Scan"
    >
      <span className="text-xl group-hover:rotate-90 transition-transform">🔍</span>
    </Link>
  )
}