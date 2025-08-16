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
          
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <h1 className="text-3xl font-bold text-[#1A1A1A] mb-2">
                Canva Template Data Export
              </h1>
              <p className="text-lg text-[#555555] mb-4">
                Copy and paste these fields into your Canva Market Scan template variables
              </p>
              <div className="flex items-center gap-6 text-sm text-[#555555]">
                <div className="flex items-center gap-2">
                  <span>📊</span>
                  <span>{allFields.length} total fields</span>
                </div>
                <div className="flex items-center gap-2">
                  <span>📁</span>
                  <span>{categories.length} categories</span>
                </div>
                <div className="flex items-center gap-2">
                  <span>💼</span>
                  <span>{scan.job_title}</span>
                </div>
              </div>
            </div>
            
            <div className="flex gap-3">
              <Link
                to={`/scan/${scanId}`}
                className="bg-white text-[#7B61FF] border border-[#7B61FF] font-semibold px-6 py-3 rounded-lg hover:bg-[#7B61FF]/5 transition-colors"
              >
                ← Back to Results
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Data Tables */}
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
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
                  <table className="w-full">
                    <thead className="bg-[#F7F7F9]">
                      <tr>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7]">
                          Field Name
                        </th>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7]">
                          Value
                        </th>
                        <th className="text-left px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7]">
                          Description
                        </th>
                        <th className="text-center px-6 py-3 text-sm font-semibold text-[#1A1A1A] border-b border-[#E5E5E7]">
                          Copy
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {categoryFields.map((field, index) => (
                        <tr key={field.field} className={index % 2 === 0 ? 'bg-white' : 'bg-[#F7F7F9]'}>
                          <td className="px-6 py-4 text-sm font-medium text-[#1A1A1A] border-b border-[#E5E5E7]">
                            <code className="bg-[#7B61FF]/10 text-[#7B61FF] px-2 py-1 rounded text-xs font-mono">
                              {field.field}
                            </code>
                          </td>
                          <td className="px-6 py-4 text-sm text-[#555555] border-b border-[#E5E5E7] max-w-md">
                            <div className="break-words">
                              {formatValue(field.value)}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-sm text-[#555555] border-b border-[#E5E5E7]">
                            {field.description}
                          </td>
                          <td className="px-6 py-4 text-center border-b border-[#E5E5E7]">
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

        {/* Usage Instructions */}
        <div className="mt-12 bg-gradient-to-r from-[#7B61FF] to-[#9F7FFF] rounded-xl p-8 text-white">
          <h3 className="text-xl font-bold mb-4">📋 How to Use This Data</h3>
          <div className="grid md:grid-cols-2 gap-6 text-sm">
            <div>
              <h4 className="font-semibold mb-2">For Canva Templates:</h4>
              <ol className="space-y-1 opacity-90">
                <li>1. Click "Copy" next to any field value</li>
                <li>2. In Canva, click on your template text element</li>
                <li>3. Paste the copied value (Cmd+V / Ctrl+V)</li>
                <li>4. Repeat for all required template variables</li>
              </ol>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Field Naming Convention:</h4>
              <ul className="space-y-1 opacity-90">
                <li>• <code className="bg-white/20 px-1 rounded">basic_info_*</code> - Company and job details</li>
                <li>• <code className="bg-white/20 px-1 rounded">region_*</code> - Salary data by region</li>
                <li>• <code className="bg-white/20 px-1 rounded">skills_*</code> - Required skills and tools</li>
                <li>• <code className="bg-white/20 px-1 rounded">analysis_*</code> - Job complexity insights</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}