import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { TidalLogo, TidalLogoCompact } from './TidalLogo'

interface LayoutProps {
  children: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()
  const isAdminRoute = location.pathname.startsWith('/dashboard') || location.pathname.startsWith('/admin')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Title */}
            <div className="flex items-center space-x-4">
              <Link to="/" className="flex items-center">
                <TidalLogo size="md" />
              </Link>
              
              {/* Subtitle based on current route */}
              <div className="hidden md:flex items-center">
                <div className="w-px h-6 bg-gray-300 mx-4"></div>
                <span className="text-sm text-gray-600">
                  {isAdminRoute ? 'Admin Dashboard' : 'Payroll Calculator'}
                </span>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center space-x-4">
              {!isAdminRoute ? (
                <Link 
                  to="/dashboard" 
                  className="text-sm text-gray-600 hover:text-tidal-600 transition-colors duration-200"
                >
                  Team Dashboard
                </Link>
              ) : (
                <Link 
                  to="/" 
                  className="text-sm text-gray-600 hover:text-tidal-600 transition-colors duration-200"
                >
                  Client Portal
                </Link>
              )}
              
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <span>by</span>
                <a 
                  href="https://hiretidal.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-tidal-600 hover:text-tidal-700 font-medium"
                >
                  hiretidal.com
                </a>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Company Info */}
            <div>
              <div className="flex items-center mb-4">
                <TidalLogo size="md" />
              </div>
              <p className="text-sm text-gray-600 mb-4">
                Precision Placement for E-Commerce Teams.<br />
                Increase Output. Save on Payroll. Scale Confidently.
              </p>
              <p className="text-xs text-gray-500">
                connect@hiretidal.com
              </p>
            </div>

            {/* Features */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Features</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• AI-Powered Job Analysis</li>
                <li>• Regional Salary Benchmarks</li>
                <li>• Skills Recommendations</li>
                <li>• Candidate Matching</li>
                <li>• Market Insights</li>
              </ul>
            </div>

            {/* Regions */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Global Reach</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>🇺🇸 United States</li>
                <li>🇵🇭 Philippines</li>
                <li>🌎 Latin America</li>
                <li>🇿🇦 South Africa</li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="mt-8 pt-8 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center">
            <p className="text-xs text-gray-500">
              © 2025 Tidal. All rights reserved. Built for global recruiting excellence.
            </p>
            <div className="flex items-center space-x-4 mt-4 sm:mt-0">
              <span className="text-xs text-gray-400">Powered by</span>
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <span>OpenAI</span>
                <span>•</span>
                <span>Supabase</span>
                <span>•</span>
                <span>React</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}