import React, { useState } from 'react'
import { MarketScanRequest, FormErrors } from '../../services/types'

interface MarketScanFormProps {
  onSubmit: (data: MarketScanRequest) => Promise<void>
  isSubmitting: boolean
}

export const MarketScanForm: React.FC<MarketScanFormProps> = ({ 
  onSubmit, 
  isSubmitting 
}) => {
  const [formData, setFormData] = useState<MarketScanRequest>({
    client_name: '',
    client_email: '',
    company_domain: '',
    job_title: '',
    job_description: '',
    hiring_challenges: ''
  })

  const [errors, setErrors] = useState<FormErrors>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})

  const validateField = (name: string, value: string): string | undefined => {
    switch (name) {
      case 'client_name':
        if (!value.trim()) return 'Your name is required'
        if (value.trim().length < 2) return 'Name must be at least 2 characters'
        return undefined

      case 'client_email':
        if (!value.trim()) return 'Email is required'
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) return 'Please enter a valid email address'
        return undefined

      case 'company_domain':
        if (!value.trim()) return 'Company domain is required'
        // Remove protocol if present and validate basic domain format
        const cleanDomain = value.replace(/^https?:\/\//, '').trim()
        const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/
        if (!domainRegex.test(cleanDomain)) return 'Please enter a valid domain (e.g., yourcompany.com)'
        return undefined

      case 'job_title':
        if (!value.trim()) return 'Job title is required'
        if (value.trim().length < 3) return 'Job title must be at least 3 characters'
        return undefined

      case 'job_description':
        if (!value.trim()) return 'Job description is required'
        if (value.trim().length < 50) return 'Job description must be at least 50 characters'
        if (value.trim().length > 5000) return 'Job description must be less than 5000 characters'
        return undefined

      default:
        return undefined
    }
  }

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }))
    }
  }

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    
    setTouched(prev => ({
      ...prev,
      [name]: true
    }))

    const error = validateField(name, value)
    setErrors(prev => ({
      ...prev,
      [name]: error
    }))
  }

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}
    
    Object.entries(formData).forEach(([key, value]) => {
      if (key !== 'hiring_challenges') { // hiring_challenges is optional
        const error = validateField(key, value)
        if (error) {
          newErrors[key] = error
        }
      }
    })

    setErrors(newErrors)
    setTouched({
      client_name: true,
      client_email: true, 
      company_domain: true,
      job_title: true,
      job_description: true
    })

    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    // Clean up company domain
    const cleanedData = {
      ...formData,
      company_domain: formData.company_domain.replace(/^https?:\/\//, '').trim().toLowerCase()
    }

    await onSubmit(cleanedData)
  }

  const getFieldError = (fieldName: string): string | undefined => {
    return touched[fieldName] ? errors[fieldName] : undefined
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6" id="market-scan-form">
      {/* Personal Information */}
      <div className="grid md:grid-cols-3 gap-6">
        <div>
          <label htmlFor="client_name" className="block text-sm font-medium text-gray-700 mb-2">
            Your Name *
          </label>
          <input
            type="text"
            id="client_name"
            name="client_name"
            value={formData.client_name}
            onChange={handleInputChange}
            onBlur={handleBlur}
            className={`form-input ${getFieldError('client_name') ? 'field-error' : ''}`}
            placeholder="Sean Agatep"
            disabled={isSubmitting}
          />
          {getFieldError('client_name') && (
            <div className="error-message">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {getFieldError('client_name')}
            </div>
          )}
        </div>

        <div>
          <label htmlFor="client_email" className="block text-sm font-medium text-gray-700 mb-2">
            Your Email *
          </label>
          <input
            type="email"
            id="client_email"
            name="client_email"
            value={formData.client_email}
            onChange={handleInputChange}
            onBlur={handleBlur}
            className={`form-input ${getFieldError('client_email') ? 'field-error' : ''}`}
            placeholder="e.g., john@company.com"
            disabled={isSubmitting}
          />
          {getFieldError('client_email') && (
            <div className="error-message">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {getFieldError('client_email')}
            </div>
          )}
        </div>

        <div>
          <label htmlFor="company_domain" className="block text-sm font-medium text-gray-700 mb-2">
            Company Domain *
          </label>
          <input
            type="text"
            id="company_domain"
            name="company_domain"
            value={formData.company_domain}
            onChange={handleInputChange}
            onBlur={handleBlur}
            className={`form-input ${getFieldError('company_domain') ? 'field-error' : ''}`}
            placeholder="e.g., yourcompany.com"
            disabled={isSubmitting}
          />
          {getFieldError('company_domain') && (
            <div className="error-message">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {getFieldError('company_domain')}
            </div>
          )}
        </div>
      </div>

      {/* Job Information */}
      <div>
        <label htmlFor="job_title" className="block text-sm font-medium text-gray-700 mb-2">
          Job Title You're Hiring For *
        </label>
        <input
          type="text"
          id="job_title"
          name="job_title"
          value={formData.job_title}
          onChange={handleInputChange}
          onBlur={handleBlur}
          className={`form-input ${getFieldError('job_title') ? 'field-error' : ''}`}
          placeholder="e.g., Shopify Admin"
          disabled={isSubmitting}
        />
        {getFieldError('job_title') && (
          <div className="error-message">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {getFieldError('job_title')}
          </div>
        )}
      </div>

      <div>
        <label htmlFor="job_description" className="block text-sm font-medium text-gray-700 mb-2">
          Job Description (or a list of Roles & Responsibilities) *
        </label>
        <textarea
          id="job_description"
          name="job_description"
          rows={6}
          value={formData.job_description}
          onChange={handleInputChange}
          onBlur={handleBlur}
          className={`form-textarea ${getFieldError('job_description') ? 'field-error' : ''}`}
          placeholder="Paste your job description or list key responsibilities..."
          disabled={isSubmitting}
        />
        <div className="flex justify-between items-center mt-1">
          {getFieldError('job_description') ? (
            <div className="error-message">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {getFieldError('job_description')}
            </div>
          ) : (
            <div></div>
          )}
          <span className="text-xs text-gray-500">
            {formData.job_description.length}/5000 characters
          </span>
        </div>
      </div>

      <div>
        <label htmlFor="hiring_challenges" className="block text-sm font-medium text-gray-700 mb-2">
          Current Hiring Challenges (Optional)
        </label>
        <textarea
          id="hiring_challenges"
          name="hiring_challenges"
          rows={3}
          value={formData.hiring_challenges}
          onChange={handleInputChange}
          className="form-textarea"
          placeholder="What specific challenges are you facing in finding the right candidate?"
          disabled={isSubmitting}
        />
        <p className="mt-1 text-xs text-gray-500">
          Help us provide better recommendations by sharing any specific challenges or requirements.
        </p>
      </div>

      {/* Submit Button */}
      <div className="flex justify-center pt-4">
        <button
          type="submit"
          disabled={isSubmitting}
          className="bg-gradient-to-r from-tidal-600 to-blue-600 hover:from-tidal-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold px-8 py-3 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-tidal-500 focus:ring-offset-2 disabled:cursor-not-allowed min-w-[200px] flex items-center justify-center space-x-2"
        >
          {isSubmitting ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Analyze Salary Expectations</span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span>Analyze Salary Expectations</span>
            </>
          )}
        </button>
      </div>

      {/* Form Footer */}
      <div className="text-center text-xs text-gray-500 pt-4 border-t border-gray-200">
        <p>
          By submitting this form, you agree to receive market analysis results and occasional updates from Tidal.
          <br />
          We respect your privacy and never share your information with third parties.
        </p>
      </div>
    </form>
  )
}