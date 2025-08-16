import React, { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { MarketScanRequest, FormErrors } from '../../services/types'

interface MarketScanFormProps {
  onSubmit: (data: MarketScanRequest) => Promise<void>
  isSubmitting: boolean
  isSuccess?: boolean
}

interface FormData {
  client_name: string
  client_email: string
  company_domain: string
  job_title: string
  job_description: string
  hiring_challenges: string
}

interface FieldProps {
  name: keyof FormData
  label: string
  placeholder: string
  type?: 'text' | 'email' | 'textarea'
  required?: boolean
  rows?: number
  maxLength?: number
  helpText?: string
  icon?: React.ReactNode
}

const InputField: React.FC<FieldProps & {
  register: any
  errors: any
  isSubmitting: boolean
  watch: any
}> = ({ 
  name, 
  label, 
  placeholder, 
  type = 'text', 
  required = false, 
  rows, 
  maxLength,
  helpText,
  icon,
  register, 
  errors, 
  isSubmitting,
  watch
}) => {
  const hasError = !!errors[name]
  const value = watch(name)
  const Component = type === 'textarea' ? 'textarea' : 'input'
  
  return (
    <div className="group">
      <label 
        htmlFor={name} 
        className="block text-sm font-semibold text-dark-navy-text mb-2 transition-colors duration-200 group-focus-within:text-tidal-purple"
      >
        <span className="flex items-center gap-2">
          {icon && <span className="text-medium-gray-text">{icon}</span>}
          {label}
          {required && <span className="text-tidal-purple">*</span>}
        </span>
      </label>
      
      <div className="relative">
        <Component
          {...register(name, {
            required: required && `${label} is required`,
            minLength: name === 'client_name' ? { value: 2, message: 'Name must be at least 2 characters' } :
                      name === 'job_title' ? { value: 3, message: 'Job title must be at least 3 characters' } :
                      name === 'job_description' ? { value: 50, message: 'Job description must be at least 50 characters' } : undefined,
            maxLength: maxLength ? { value: maxLength, message: `Maximum ${maxLength} characters allowed` } : undefined,
            pattern: name === 'client_email' ? {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: 'Please enter a valid email address'
            } : name === 'company_domain' ? {
              value: /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
              message: 'Please enter a valid domain (e.g., yourcompany.com)'
            } : undefined
          })}
          id={name}
          type={type === 'textarea' ? undefined : type}
          rows={rows}
          placeholder={placeholder}
          disabled={isSubmitting}
          className={`
            w-full px-4 py-3 border-2 rounded-xl text-dark-navy-text placeholder-medium-gray-text 
            transition-all duration-300 ease-out resize-none
            focus:outline-none focus:ring-4 focus:ring-tidal-purple/20 focus:border-tidal-purple 
            disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
            ${hasError 
              ? 'border-red-300 bg-red-50/50 focus:border-red-500 focus:ring-red-500/20' 
              : 'border-card-border-gray bg-white hover:border-tidal-purple/30 focus:border-tidal-purple'
            }
            ${isSubmitting ? 'opacity-50' : ''}
          `}
        />
        
        {/* Success state indicator */}
        {!hasError && value && value.length > 0 && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="w-5 h-5 bg-success-green rounded-full flex items-center justify-center">
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        )}
      </div>
      
      {/* Error message */}
      {hasError && (
        <div className="mt-2 flex items-center gap-2 text-red-600 text-sm animate-slideInUp">
          <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="font-medium">{errors[name]?.message}</span>
        </div>
      )}
      
      {/* Help text */}
      {helpText && !hasError && (
        <p className="mt-2 text-xs text-medium-gray-text">
          {helpText}
        </p>
      )}
      
      {/* Character count for job description */}
      {name === 'job_description' && maxLength && (
        <div className="mt-2 flex justify-end">
          <span className={`text-xs transition-colors duration-200 ${
            (value?.length || 0) > maxLength * 0.8 
              ? 'text-yellow-600' 
              : 'text-medium-gray-text'
          }`}>
            {value?.length || 0}/{maxLength} characters
          </span>
        </div>
      )}
    </div>
  )
}

export const MarketScanForm: React.FC<MarketScanFormProps> = ({ 
  onSubmit, 
  isSubmitting,
  isSuccess = false
}) => {
  const [showSuccess, setShowSuccess] = useState(false)
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isValid }, 
    watch,
    reset 
  } = useForm<FormData>({
    mode: 'onChange',
    defaultValues: {
      client_name: '',
      client_email: '',
      company_domain: '',
      job_title: '',
      job_description: '',
      hiring_challenges: ''
    }
  })

  // Watch for success state changes
  useEffect(() => {
    if (isSuccess) {
      setShowSuccess(true)
      const timer = setTimeout(() => {
        setShowSuccess(false)
        reset()
      }, 5000)
      return () => clearTimeout(timer)
    }
  }, [isSuccess, reset])

  // Check for pre-filled data from localStorage (Quick Scan feature)
  useEffect(() => {
    const prefillData = localStorage.getItem('tidal_prefill_scan')
    if (prefillData) {
      try {
        const data = JSON.parse(prefillData)
        if (data.prefilled) {
          // Pre-fill the form with existing scan data
          reset({
            client_name: '',
            client_email: '',
            company_domain: data.company_domain || '',
            job_title: data.job_title || '',
            job_description: data.job_description || '',
            hiring_challenges: ''
          })
          
          // Clear the localStorage after pre-filling
          localStorage.removeItem('tidal_prefill_scan')
          
          // Show a helpful message
          console.log('Pre-filled form with similar calculation data')
        }
      } catch (error) {
        console.error('Error parsing pre-fill data:', error)
        localStorage.removeItem('tidal_prefill_scan')
      }
    }
  }, [reset])

  const onFormSubmit = async (data: FormData) => {
    // Clean up company domain
    const cleanedData: MarketScanRequest = {
      ...data,
      company_domain: data.company_domain.replace(/^https?:\/\//, '').trim().toLowerCase()
    }

    await onSubmit(cleanedData)
  }

  // Success state component
  if (showSuccess) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12 animate-slideInUp">
        <div className="w-20 h-20 bg-success-green rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-2xl font-bold text-dark-navy-text mb-4">
          🎉 Your Market Scan is Processing!
        </h3>
        <p className="text-lg text-medium-gray-text mb-6">
          We're analyzing your job requirements and gathering salary insights across all regions. 
          You'll receive detailed results via email shortly.
        </p>
        <div className="bg-tidal-purple/5 border border-tidal-purple/20 rounded-lg p-4">
          <p className="text-sm text-tidal-purple font-medium">
            💡 Pro tip: Check your email in the next 5-10 minutes for comprehensive salary recommendations!
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">

      <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-8" id="market-scan-form">
        {/* Personal Information Section */}
        <div className="bg-white rounded-2xl border border-card-border-gray p-8 shadow-sm">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-tidal-purple/10 rounded-lg flex items-center justify-center">
              <span className="text-xl">👤</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-dark-navy-text">Your Information</h3>
              <p className="text-sm text-medium-gray-text">Tell us about yourself and your company</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 tablet:grid-cols-3 gap-6">
            <InputField
              name="client_name"
              label="Your Name"
              placeholder="e.g., Sean Agatep"
              required
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="👤"
            />
            
            <InputField
              name="client_email"
              label="Work Email"
              placeholder="e.g., sean@yourcompany.com"
              type="email"
              required
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="📧"
              helpText="We'll send your detailed salary analysis here"
            />
            
            <InputField
              name="company_domain"
              label="Company Website"
              placeholder="e.g., yourcompany.com"
              required
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="🌐"
              helpText="No need to include https://"
            />
          </div>
        </div>

        {/* Job Information Section */}
        <div className="bg-white rounded-2xl border border-card-border-gray p-8 shadow-sm">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-tidal-aqua/10 rounded-lg flex items-center justify-center">
              <span className="text-xl">📊</span>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-dark-navy-text">Role Details</h3>
              <p className="text-sm text-medium-gray-text">Help us understand what you're looking to hire</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <InputField
              name="job_title"
              label="Job Title You're Hiring For"
              placeholder="e.g., Shopify Store Manager, Marketing Assistant, Customer Success Specialist"
              required
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="🎯"
            />
            
            <InputField
              name="job_description"
              label="Job Description & Responsibilities"
              placeholder="Paste your job description or list the key responsibilities and requirements for this role..."
              type="textarea"
              rows={6}
              maxLength={5000}
              required
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="📝"
              helpText="The more detail you provide, the more accurate your salary recommendations will be"
            />
            
            <InputField
              name="hiring_challenges"
              label="Current Hiring Challenges"
              placeholder="e.g., Hard to find candidates with specific tech stack experience, Budget constraints, Timeline pressure..."
              type="textarea"
              rows={3}
              register={register}
              errors={errors}
              isSubmitting={isSubmitting}
              watch={watch}
              icon="🎯"
              helpText="Optional: Share any specific challenges to get more targeted recommendations"
            />
          </div>
        </div>

        {/* What You'll Get Section */}
        <div className="bg-gradient-to-br from-tidal-purple/5 to-tidal-aqua/5 rounded-2xl border border-tidal-purple/20 p-8">
          <div className="text-center mb-6">
            <h3 className="text-xl font-semibold text-dark-navy-text mb-2">
              What You'll Receive
            </h3>
            <p className="text-medium-gray-text">Your comprehensive market analysis will include:</p>
          </div>
          
          <div className="grid grid-cols-1 tablet:grid-cols-2 gap-4">
            {[
              { icon: "💰", text: "Salary ranges for US, Philippines & Latin America" },
              { icon: "📊", text: "Cost savings analysis by region" },
              { icon: "🎯", text: "Must-have vs nice-to-have skills breakdown" },
              { icon: "🌍", text: "Regional hiring recommendations" },
              { icon: "⚡", text: "Role complexity and timeline insights" },
              { icon: "📈", text: "Market competitiveness factors" }
            ].map((item, index) => (
              <div key={index} className="flex items-center gap-3 text-sm text-dark-navy-text">
                <span className="text-lg">{item.icon}</span>
                <span className="font-medium">{item.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center pt-4">
          <button
            type="submit"
            disabled={isSubmitting || !isValid}
            className={`
              group relative overflow-hidden bg-tidal-purple hover:bg-gradient-purple-end 
              disabled:bg-gray-400 text-white font-semibold px-8 py-4 rounded-xl 
              transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-tidal-purple/30 
              disabled:cursor-not-allowed min-w-[280px] shadow-lg hover:shadow-xl
              ${!isSubmitting && isValid ? 'hover:scale-105 transform' : ''}
              ${isSubmitting ? 'animate-pulse' : ''}
            `}
          >
            {/* Loading overlay */}
            {isSubmitting && (
              <div className="absolute inset-0 bg-gradient-to-r from-tidal-purple to-gradient-purple-end opacity-90 flex items-center justify-center">
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Analyzing Market Data...</span>
                </div>
              </div>
            )}
            
            {/* Button content */}
            <div className={`flex items-center justify-center gap-3 ${isSubmitting ? 'opacity-0' : 'opacity-100'}`}>
              <span className="text-xl">🔍</span>
              <span className="font-semibold">Analyze Role</span>
              <svg 
                className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </button>
          
          <p className="mt-4 text-sm text-medium-gray-text">
            ⚡ Results delivered in 5-10 minutes • 🔒 Your data is secure and private
          </p>
        </div>

        {/* Form Footer */}
        <div className="text-center pt-8 border-t border-card-border-gray">
          <p className="text-xs text-medium-gray-text max-w-2xl mx-auto leading-relaxed">
            By submitting this form, you'll receive your market analysis results and occasional insights from Tidal. 
            We respect your privacy and never share your information with third parties. 
            <br />
            <span className="text-tidal-purple font-medium">100% free, no credit card required.</span>
          </p>
        </div>
      </form>
    </div>
  )
}