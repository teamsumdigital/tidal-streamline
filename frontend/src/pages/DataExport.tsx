import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiService } from '../services/api'
import { MarketScanResponse } from '../services/types'

export const DataExport: React.FC = () => {
  const { scanId } = useParams<{ scanId: string }>()
  const [scan, setScan] = useState<MarketScanResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [copiedField, setCopiedField] = useState<string | null>(null)

  useEffect(() => {
    const fetchScan = async () => {
      if (!scanId) return

      try {
        const response = await apiService.getMarketScan(scanId)
        setScan(response)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load scan data')
      } finally {
        setLoading(false)
      }
    }

    fetchScan()
  }, [scanId])

  const copyToClipboard = async (text: string, fieldName: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedField(fieldName)
      setTimeout(() => setCopiedField(null), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const downloadCSV = () => {
    if (!scan) return
    
    const allFields = extractAllFields(scan)
    
    // Create CSV headers
    const headers = ['Field Name', 'Value', 'Category', 'Description']
    
    // Create CSV rows
    const rows = allFields.map(field => [
      field.field,
      formatValue(field.value).replace(/"/g, '""'), // Escape quotes
      field.category,
      field.description.replace(/"/g, '""') // Escape quotes
    ])
    
    // Combine headers and rows
    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')
    
    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `tidal-market-scan-${scan.job_title.replace(/\s+/g, '-').toLowerCase()}-${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  // NEW: Backend CSV Export with all 134 fields including candidates
  const downloadFullCSV = async () => {
    if (!scan || !scanId) return
    
    try {
      setLoading(true)
      const csvBlob = await apiService.exportMarketScanCSV(scanId, 'template')
      
      // Create and download file
      const link = document.createElement('a')
      const url = URL.createObjectURL(csvBlob)
      link.setAttribute('href', url)
      link.setAttribute('download', `tidal-full-export-${scan.job_title.replace(/\s+/g, '-').toLowerCase()}-${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export full CSV')
    } finally {
      setLoading(false)
    }
  }

  const downloadTemplateCSV = () => {
    if (!scan) return
    
    const allFields = extractAllFields(scan)
    const fieldMap = allFields.reduce((acc, field) => {
      acc[field.field] = formatValue(field.value)
      return acc
    }, {} as Record<string, string>)
    
    // Template-optimized CSV format for Canva bulk import
    const templateData = {
      // Company & Role
      company_name: fieldMap.company_domain || 'N/A',
      position_title: fieldMap.job_title || 'N/A',
      scan_date: new Date(scan.created_at).toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      }),
      analysis_confidence: fieldMap.confidence_score || 'N/A',
      
      // Primary Salary Data
      us_salary: fieldMap.united_states_mid_salary || 'N/A',
      us_salary_min: fieldMap.united_states_low_salary || 'N/A',
      us_salary_max: fieldMap.united_states_high_salary || 'N/A',
      
      ph_salary: fieldMap.philippines_mid_salary || 'N/A',
      ph_salary_min: fieldMap.philippines_low_salary || 'N/A',
      ph_salary_max: fieldMap.philippines_high_salary || 'N/A',
      ph_savings_percent: fieldMap.philippines_savings_vs_us || 'N/A',
      
      latam_salary: fieldMap.latin_america_mid_salary || 'N/A',
      latam_salary_min: fieldMap.latin_america_low_salary || 'N/A',
      latam_salary_max: fieldMap.latin_america_high_salary || 'N/A',
      latam_savings_percent: fieldMap.latin_america_savings_vs_us || 'N/A',
      
      sa_salary: fieldMap.south_africa_mid_salary || 'N/A',
      sa_salary_min: fieldMap.south_africa_low_salary || 'N/A',
      sa_salary_max: fieldMap.south_africa_high_salary || 'N/A',
      sa_savings_percent: fieldMap.south_africa_savings_vs_us || 'N/A',
      
      // Skills
      required_skills: fieldMap.must_have_skills || 'N/A',
      preferred_skills: fieldMap.nice_to_have_skills || 'N/A',
      certifications: fieldMap.certification_recommendations || 'N/A',
      tech_skills: fieldMap.technical_skills || 'N/A',
      marketing_skills: fieldMap.marketing_skills || 'N/A',
      analytics_skills: fieldMap.analytical_skills || 'N/A',
      
      // Job Analysis
      role_complexity: fieldMap.complexity_score || 'N/A',
      seniority_level: fieldMap.experience_level || 'N/A',
      experience_years: fieldMap.years_experience_required || 'N/A',
      remote_suitability: fieldMap.remote_work_suitability || 'N/A',
      best_regions: fieldMap.recommended_regions || 'N/A',
      main_duties: fieldMap.key_responsibilities || 'N/A',
      role_challenges: fieldMap.unique_challenges || 'N/A',
      
      // Additional Insights
      high_demand_regions: fieldMap.high_demand_regions || 'N/A',
      competitive_factors: fieldMap.competitive_factors || 'N/A',
      cost_efficiency: fieldMap.cost_efficiency || 'N/A',
      salary_factors: fieldMap.salary_factors || 'N/A'
    }
    
    // Create CSV with template variables as headers
    const headers = Object.keys(templateData)
    const values = Object.values(templateData).map(value => 
      String(value).replace(/"/g, '""') // Escape quotes
    )
    
    const csvContent = [
      headers.join(','),
      values.map(value => `"${value}"`).join(',')
    ].join('\n')
    
    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', `market-scan-template-${scan.job_title.replace(/\s+/g, '-').toLowerCase()}-${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const copyAllFieldsAsJSON = async () => {
    if (!scan || !scanId) return
    
    try {
      // Get the same complete data as CSV export
      const csvBlob = await apiService.exportMarketScanCSV(scanId, 'template')
      const csvText = await csvBlob.text()
      
      // Parse CSV to JSON
      const lines = csvText.split('\n').filter(line => line.trim())
      if (lines.length < 2) throw new Error('Invalid CSV data')
      
      const headers = lines[0].split(',').map(header => header.replace(/"/g, ''))
      const values = lines[1].split(',').map(value => value.replace(/"/g, ''))
      
      const jsonData: Record<string, string> = {}
      headers.forEach((header, index) => {
        jsonData[header] = values[index] || 'N/A'
      })
      
      await navigator.clipboard.writeText(JSON.stringify(jsonData, null, 2))
      setCopiedField('all-json')
      setTimeout(() => setCopiedField(null), 3000)
    } catch (err) {
      console.error('Failed to copy complete JSON: ', err)
      setError(err instanceof Error ? err.message : 'Failed to copy complete JSON data')
    }
  }

  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return 'N/A'
    if (typeof value === 'object') return JSON.stringify(value, null, 2)
    if (typeof value === 'boolean') return value ? 'Yes' : 'No'
    return String(value)
  }

  const extractAllFields = (scan: MarketScanResponse) => {
    const fields: Array<{ category: string; field: string; value: any; description: string }> = []

    // Basic Information
    fields.push(
      { category: 'Basic Info', field: 'company_domain', value: scan.company_domain, description: 'Client company domain' },
      { category: 'Basic Info', field: 'job_title', value: scan.job_title, description: 'Position title being analyzed' },
      { category: 'Basic Info', field: 'status', value: scan.status, description: 'Analysis completion status' },
      { category: 'Basic Info', field: 'created_at', value: new Date(scan.created_at).toLocaleDateString(), description: 'Analysis creation date' },
      { category: 'Basic Info', field: 'confidence_score', value: scan.confidence_score ? `${Math.round(scan.confidence_score * 100)}%` : 'N/A', description: 'AI confidence in recommendations' }
    )

    // Salary Data
    if (scan.salary_recommendations?.salary_recommendations) {
      const salaryRecs = scan.salary_recommendations.salary_recommendations
      Object.entries(salaryRecs).forEach(([regionName, salaryData]) => {
        const safeName = regionName.replace(/\s+/g, '_').toLowerCase()
        fields.push(
          { category: 'Salary Data', field: `${safeName}_region`, value: regionName, description: `Region name - ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_currency`, value: salaryData.currency, description: `Currency for ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_low_salary`, value: salaryData.low, description: `Minimum salary range for ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_mid_salary`, value: salaryData.mid, description: `Average salary for ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_high_salary`, value: salaryData.high, description: `Maximum salary range for ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_period`, value: salaryData.period, description: `Salary period for ${regionName}` },
          { category: 'Salary Data', field: `${safeName}_savings_vs_us`, value: salaryData.savings_vs_us ? `${salaryData.savings_vs_us}%` : 'N/A', description: `Cost savings vs US rates for ${regionName}` }
        )
      })
      
      // Additional salary recommendations metadata
      if (scan.salary_recommendations.recommended_pay_band) {
        fields.push({ category: 'Salary Data', field: 'recommended_pay_band', value: scan.salary_recommendations.recommended_pay_band, description: 'Recommended salary band (low/mid/high)' })
      }
      
      if (scan.salary_recommendations.factors_considered) {
        fields.push({ category: 'Salary Data', field: 'factors_considered', value: scan.salary_recommendations.factors_considered.join(', '), description: 'Factors considered in salary calculation' })
      }
      
      if (scan.salary_recommendations.market_insights) {
        const insights = scan.salary_recommendations.market_insights
        fields.push(
          { category: 'Salary Data', field: 'high_demand_regions', value: insights.high_demand_regions?.join(', '), description: 'Regions with high demand for this role' },
          { category: 'Salary Data', field: 'competitive_factors', value: insights.competitive_factors?.join(', '), description: 'Factors affecting competitiveness' },
          { category: 'Salary Data', field: 'cost_efficiency', value: insights.cost_efficiency, description: 'Cost efficiency analysis' }
        )
      }
    }

    // Skills Data
    if (scan.skills_recommendations) {
      const skills = scan.skills_recommendations
      
      if (skills.must_have_skills) {
        fields.push({ category: 'Skills', field: 'must_have_skills', value: skills.must_have_skills.join(', '), description: 'Essential required skills' })
      }
      
      if (skills.nice_to_have_skills) {
        fields.push({ category: 'Skills', field: 'nice_to_have_skills', value: skills.nice_to_have_skills.join(', '), description: 'Preferred additional skills' })
      }
      
      if (skills.certification_recommendations) {
        fields.push({ category: 'Skills', field: 'certification_recommendations', value: skills.certification_recommendations.join(', '), description: 'Relevant certifications' })
      }
      
      if (skills.skill_categories) {
        Object.entries(skills.skill_categories).forEach(([categoryName, categorySkills]) => {
          const safeName = categoryName.replace(/\s+/g, '_').toLowerCase()
          fields.push({ category: 'Skills', field: `${safeName}_skills`, value: categorySkills.join(', '), description: `${categoryName} related skills` })
        })
      }
    }

    // Job Analysis
    if (scan.job_analysis) {
      const analysis = scan.job_analysis
      fields.push(
        { category: 'Job Analysis', field: 'complexity_score', value: analysis.complexity_score, description: 'Role complexity rating (1-10)' },
        { category: 'Job Analysis', field: 'role_category', value: analysis.role_category, description: 'Primary job category' },
        { category: 'Job Analysis', field: 'experience_level', value: analysis.experience_level, description: 'Required experience level' },
        { category: 'Job Analysis', field: 'years_experience_required', value: analysis.years_experience_required, description: 'Years of experience required' },
        { category: 'Job Analysis', field: 'remote_work_suitability', value: analysis.remote_work_suitability, description: 'Remote work suitability' },
        { category: 'Job Analysis', field: 'key_responsibilities', value: analysis.key_responsibilities?.join('; '), description: 'Main job responsibilities' },
        { category: 'Job Analysis', field: 'unique_challenges', value: analysis.unique_challenges, description: 'Unique challenges for this role' },
        { category: 'Job Analysis', field: 'recommended_regions', value: analysis.recommended_regions?.join(', '), description: 'Best region recommendations' },
        { category: 'Job Analysis', field: 'salary_factors', value: analysis.salary_factors?.join(', '), description: 'Factors affecting salary' }
      )
      
      // Job analysis skills (separate from skills_recommendations)
      if (analysis.must_have_skills) {
        fields.push({ category: 'Job Analysis', field: 'analysis_must_have_skills', value: analysis.must_have_skills.join(', '), description: 'Must-have skills from job analysis' })
      }
      
      if (analysis.nice_to_have_skills) {
        fields.push({ category: 'Job Analysis', field: 'analysis_nice_to_have_skills', value: analysis.nice_to_have_skills.join(', '), description: 'Nice-to-have skills from job analysis' })
      }
    }

    // Additional metadata
    if (scan.processing_time_seconds) {
      fields.push({ category: 'Metadata', field: 'processing_time', value: `${scan.processing_time_seconds}s`, description: 'Time taken to complete analysis' })
    }
    
    if (scan.similar_scans_count) {
      fields.push({ category: 'Metadata', field: 'similar_scans_count', value: scan.similar_scans_count, description: 'Number of similar roles analyzed for comparison' })
    }

    return fields
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F7F7F9] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin w-8 h-8 border-4 border-[#7B61FF] border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-[#555555]">Loading data export...</p>
        </div>
      </div>
    )
  }

  if (error || !scan) {
    return (
      <div className="min-h-screen bg-[#F7F7F9] flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-[#1A1A1A] mb-4">Export Not Available</h2>
          <p className="text-[#555555] mb-6">{error || 'Scan data not found'}</p>
          <Link to="/" className="bg-[#7B61FF] text-white px-6 py-3 rounded-lg font-semibold">
            Back to Calculator
          </Link>
        </div>
      </div>
    )
  }

  const allFields = extractAllFields(scan)
  const categories = Array.from(new Set(allFields.map(f => f.category)))

  return (
    <div className="min-h-screen bg-[#F7F7F9]">
      {/* Header */}
      <div className="bg-white border-b border-[#E5E5E7]">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
          {/* Breadcrumb */}
          <div className="flex items-center gap-2 text-sm text-[#555555] mb-4">
            <Link to="/" className="hover:text-[#7B61FF] transition-colors">Payroll Calculator</Link>
            <span>/</span>
            <Link to={`/scan/${scanId}`} className="hover:text-[#7B61FF] transition-colors">Results</Link>
            <span>/</span>
            <span className="text-[#1A1A1A] font-medium">Data Export</span>
          </div>
          
          {/* Complete Purple Header Section */}
          <div className="bg-gradient-to-r from-[#7B61FF] to-[#9F7FFF] rounded-xl p-8 text-white">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  Export Ready
                </h1>
                <p className="text-lg text-white/90 mb-4">
                  {scan.job_title} • {new Date(scan.created_at).toLocaleDateString()}
                </p>
                <p className="text-white/80">
                  Export complete market scan data for client presentations and Canva templates
                </p>
              </div>
              
              {/* Template Fields Count */}
              <div className="text-center">
                <div className="text-4xl font-bold text-white">{allFields.length + 92}</div>
                <div className="text-sm text-white/80">Template Fields</div>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex flex-wrap gap-3 mt-6 pt-6 border-t border-white/20">
              <button
                onClick={downloadFullCSV}
                disabled={loading}
                className="bg-gradient-to-r from-[#FF6B61] to-[#FF8E87] text-white font-semibold px-6 py-3 rounded-lg hover:from-[#E55B51] hover:to-[#E57E77] transition-all flex items-center gap-2 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
{loading ? '⏳ Exporting...' : `🚀 Complete Export (${allFields.length + 92} Fields)`}
              </button>
              
              <button
                onClick={copyAllFieldsAsJSON}
                className={`font-semibold px-6 py-3 rounded-lg transition-colors flex items-center gap-2 ${
                  copiedField === 'all-json' 
                    ? 'bg-green-100 text-green-700 border border-green-300' 
                    : 'bg-white text-[#7B61FF] border border-white hover:bg-white/10'
                }`}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                {copiedField === 'all-json' ? '✓ Copied JSON' : 'Copy All as JSON'}
              </button>
              
              <Link
                to={`/scan/${scanId}`}
                className="bg-white/10 text-white border border-white/30 font-semibold px-6 py-3 rounded-lg hover:bg-white/20 transition-colors"
              >
                ← Back to Results
              </Link>
            </div>
          </div>
        </div>
      </div>


      {/* Data Tables */}
      <div className="max-w-7xl mx-auto px-6 lg:px-8 pb-12">
        <div className="space-y-8">
          {categories.map(category => {
            const categoryFields = allFields.filter(f => f.category === category)
            
            return (
              <div key={category} className="bg-white rounded-xl border border-[#E5E5E7] overflow-hidden">
                <div className="bg-[#F7F7F9] px-6 py-4 border-b border-[#E5E5E7]">
                  <h2 className="text-xl font-bold text-[#1A1A1A]">{category}</h2>
                  <p className="text-sm text-[#555555] mt-1">{categoryFields.length} fields available</p>
                </div>
                
                <div className="overflow-x-auto">
                  <table className="w-full table-fixed">
                    <thead className="bg-[#F7F7F9]">
                      <tr>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7] w-1/4">
                          Field Name
                        </th>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7] w-1/4">
                          Value
                        </th>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7] w-5/12">
                          Description
                        </th>
                        <th className="text-center px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7] w-1/12">
                          Copy
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {categoryFields.map((field, index) => (
                        <tr key={field.field} className={index % 2 === 0 ? 'bg-white' : 'bg-[#F7F7F9]'}>
                          <td className="px-6 py-4 text-sm font-medium text-[#1A1A1A] border-b border-[#E5E5E7] w-1/4">
                            <code className="bg-[#7B61FF]/10 text-[#7B61FF] px-2 py-1 rounded text-xs font-mono break-words">
                              {field.field}
                            </code>
                          </td>
                          <td className="px-6 py-4 text-sm text-[#555555] border-b border-[#E5E5E7] w-1/4">
                            <div className="break-words">
                              {formatValue(field.value)}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-[#555555] border-b border-[#E5E5E7] w-5/12">
                            <div className="break-words">
                              {field.description}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-center border-b border-[#E5E5E7] w-1/12">
                            <button
                              onClick={() => copyToClipboard(formatValue(field.value), field.field)}
                              className={`px-3 py-1 rounded text-xs font-medium transition-all ${
                                copiedField === field.field
                                  ? 'bg-green-100 text-green-700'
                                  : 'bg-[#7B61FF]/10 text-[#7B61FF] hover:bg-[#7B61FF]/20'
                              }`}
                            >
                              {copiedField === field.field ? '✓ Copied' : 'Copy'}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )
          })}
        </div>

      </div>
    </div>
  )
}