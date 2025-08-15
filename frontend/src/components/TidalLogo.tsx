import React from 'react'

interface TidalLogoProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export const TidalLogo: React.FC<TidalLogoProps> = ({ size = 'md', className = '' }) => {
  const dimensions = {
    sm: { width: 24, height: 24, fontSize: 'text-xs' },
    md: { width: 32, height: 32, fontSize: 'text-sm' },
    lg: { width: 40, height: 40, fontSize: 'text-base' }
  }

  const { width, height } = dimensions[size]

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Purple square with white atomic logo */}
      <div 
        className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-lg flex items-center justify-center"
        style={{ width: `${width}px`, height: `${height}px` }}
      >
        <svg 
          width={width * 0.6} 
          height={height * 0.6} 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Atomic/molecular structure - simplified version */}
          <g stroke="white" strokeWidth="1.5" fill="none">
            {/* Center circle */}
            <circle cx="12" cy="12" r="2" fill="white" />
            
            {/* Orbiting circles */}
            <circle cx="6" cy="12" r="1.5" fill="white" />
            <circle cx="18" cy="12" r="1.5" fill="white" />
            <circle cx="12" cy="6" r="1.5" fill="white" />
            <circle cx="12" cy="18" r="1.5" fill="white" />
            
            {/* Orbital paths */}
            <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(0 12 12)" />
            <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(60 12 12)" />
            <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(120 12 12)" />
          </g>
        </svg>
      </div>
      
      {/* TIDAL text */}
      <span className={`font-bold text-gray-900 ${dimensions[size].fontSize}`} style={{ letterSpacing: '0.1em' }}>
        TIDAL
      </span>
    </div>
  )
}

export const TidalLogoCompact: React.FC<{ size?: number; className?: string }> = ({ 
  size = 32, 
  className = '' 
}) => {
  return (
    <div 
      className={`bg-gradient-to-br from-purple-600 to-purple-700 rounded-lg flex items-center justify-center ${className}`}
      style={{ width: `${size}px`, height: `${size}px` }}
    >
      <svg 
        width={size * 0.6} 
        height={size * 0.6} 
        viewBox="0 0 24 24" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <g stroke="white" strokeWidth="1.5" fill="none">
          <circle cx="12" cy="12" r="2" fill="white" />
          <circle cx="6" cy="12" r="1.5" fill="white" />
          <circle cx="18" cy="12" r="1.5" fill="white" />
          <circle cx="12" cy="6" r="1.5" fill="white" />
          <circle cx="12" cy="18" r="1.5" fill="white" />
          <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(0 12 12)" />
          <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(60 12 12)" />
          <ellipse cx="12" cy="12" rx="8" ry="4" transform="rotate(120 12 12)" />
        </g>
      </svg>
    </div>
  )
}