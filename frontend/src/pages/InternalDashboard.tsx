import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { SystemStats, MarketScanSummary } from '../services/types'

export const InternalDashboard: React.FC = () => {
  const [stats, setStats] = useState<SystemStats | null>(null)
  const [recentScans, setRecentScans] = useState<MarketScanSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsResponse, scansResponse] = await Promise.all([
          apiService.getSystemStats(),
          apiService.getMarketScans({ page: 1, page_size: 10 })
        ])
        
        setStats(statsResponse)
        setRecentScans(scansResponse.scans)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-64 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card text-center">
          <h2 className="text-xl font-bold text-red-600 mb-4">Dashboard Error</h2>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Tidal Team Dashboard</h1>
        <p className="text-gray-600 mt-2">Monitor market scan performance and coach the system.</p>
      </div>

      {/* Stats Overview */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card text-center">
            <div className="text-3xl font-bold text-tidal-600 mb-2">{stats.total_scans}</div>
            <div className="text-sm text-gray-600">Total Scans</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">{stats.completed_scans}</div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-yellow-600 mb-2">{stats.pending_scans}</div>
            <div className="text-sm text-gray-600">Processing</div>
          </div>
          <div className="card text-center">
            <div className="text-3xl font-bold text-gray-600 mb-2">
              {stats.average_processing_time.toFixed(1)}s
            </div>
            <div className="text-sm text-gray-600">Avg Processing</div>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Market Scans</h2>
          <div className="space-y-4">
            {recentScans.map((scan) => (
              <div key={scan.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <h3 className="font-semibold text-gray-900">{scan.job_title}</h3>
                  <p className="text-sm text-gray-600">{scan.client_name} • {scan.company_domain}</p>
                  <p className="text-xs text-gray-500">{new Date(scan.created_at).toLocaleDateString()}</p>
                </div>
                <div className="text-right">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    scan.status === 'completed' ? 'bg-green-100 text-green-800' :
                    scan.status === 'analyzing' ? 'bg-yellow-100 text-yellow-800' :
                    scan.status === 'failed' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {scan.status}
                  </span>
                  <Link 
                    to={`/scan/${scan.id}`}
                    className="block text-xs text-tidal-600 hover:text-tidal-700 mt-1"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Roles */}
        {stats && (
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Popular Role Categories</h2>
            <div className="space-y-4">
              {stats.top_role_categories.map((role, index) => (
                <div key={role.role} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-tidal-100 text-tidal-700 rounded-full flex items-center justify-center text-sm font-bold mr-3">
                      {index + 1}
                    </div>
                    <span className="font-medium text-gray-900">{role.role}</span>
                  </div>
                  <span className="text-sm text-gray-600">{role.count} scans</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="mt-8 card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
            <h3 className="font-semibold text-gray-900 mb-2">Review Quality Metrics</h3>
            <p className="text-sm text-gray-600">Check recommendation accuracy and confidence scores</p>
          </button>
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
            <h3 className="font-semibold text-gray-900 mb-2">Manage Failed Scans</h3>
            <p className="text-sm text-gray-600">Investigate and resolve processing errors</p>
          </button>
          <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left">
            <h3 className="font-semibold text-gray-900 mb-2">Retrain Model</h3>
            <p className="text-sm text-gray-600">Improve recommendations with latest data</p>
          </button>
        </div>
      </div>

      {/* System Health */}
      <div className="mt-8 grid md:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">System Health</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">API Status</span>
              <span className="flex items-center text-green-600">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Healthy
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Database</span>
              <span className="flex items-center text-green-600">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Connected
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">AI Service</span>
              <span className="flex items-center text-green-600">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Available
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Data Quality</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Historical Scans</span>
              <span className="text-gray-900 font-semibold">200+ records</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Candidate Profiles</span>
              <span className="text-gray-900 font-semibold">50+ profiles</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Regional Coverage</span>
              <span className="text-gray-900 font-semibold">4 regions</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}