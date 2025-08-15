# Market Scan Results UI Components

This directory contains the complete set of UI components for the Tidal MarketScanResults page, following the exact PRD design requirements and brand guidelines.

## Components Overview

### 1. SkillsSection.tsx
**Purpose**: Displays recommended skills and tools with must-have vs nice-to-have categorization

**Features**:
- Pill-shaped skill badges with Tidal brand colors
- Must-have skills (Tidal Purple) vs Nice-to-have skills (Tidal Aqua)
- Certification recommendations section
- Responsive grid layout
- Smooth fade-in animations
- Loading skeleton states

**Props**:
```typescript
interface SkillsSectionProps {
  skillsRecommendation?: SkillsRecommendation
  className?: string
  isLoading?: boolean
}
```

### 2. JobAnalysisSection.tsx
**Purpose**: Job analysis summary display with scannable format and proper hierarchy

**Features**:
- Most important insights displayed first (complexity, experience, remote suitability)
- Responsive insight cards with icons and color coding
- Detailed sections for responsibilities, challenges, and salary factors
- Dark navy text for headings per PRD requirements
- Animated reveal effects

**Props**:
```typescript
interface JobAnalysisSectionProps {
  jobAnalysis?: JobAnalysis
  className?: string
  isLoading?: boolean
}
```

### 3. NextStepsSection.tsx
**Purpose**: Next steps guidance with clear action-oriented copy

**Features**:
- Priority-based step cards (high, medium, low)
- Timeframe indicators for each step
- Tidal purple accent elements
- Action buttons with hover animations
- Contact section with gradient background
- Clear action-oriented microcopy

**Props**:
```typescript
interface NextStepsSectionProps {
  customSteps?: NextStep[]
  className?: string
  isLoading?: boolean
  onContactTidal?: () => void
  onBookCall?: () => void
}
```

### 4. CTASection.tsx
**Purpose**: Call-to-action blocks with purple gradient backgrounds

**Features**:
- Multiple layout options (horizontal, vertical, grid)
- Purple gradient backgrounds for primary CTAs
- Bold white text with hover animations
- Feature lists with checkmarks
- Trust indicators (stats and badges)
- "Book Strategy Call" styling as specified

**Props**:
```typescript
interface CTASectionProps {
  title?: string
  subtitle?: string
  ctaItems?: CTAItem[]
  className?: string
  isLoading?: boolean
  layout?: 'horizontal' | 'vertical' | 'grid'
}
```

## Design System Compliance

### Color Palette (Exact PRD Colors)
- **Tidal Purple**: `#7B61FF` - Primary buttons, CTAs, gradients
- **Tidal Aqua**: `#00C6A2` - Savings %, highlights, positive labels
- **Dark Navy Text**: `#1A1A1A` - Primary headings
- **Medium Gray Text**: `#555555` - Secondary text
- **Light Gray Background**: `#F7F7F9` - Section backgrounds
- **Card Border Gray**: `#E5E5E7` - Card outlines

### Responsive Breakpoints
- **Desktop**: 1200px+ (generous padding 40px+)
- **Tablet**: 768-1199px
- **Mobile**: <768px (minimum 24px padding)

### Typography Hierarchy
- **Section Titles**: Bold, large sans-serif (Inter font)
- **Subheadings**: Medium weight, sentence case
- **Body Text**: 16-18px, medium gray for secondary text

### Animation Standards
- **Fade-in animations**: 0.6s ease-out
- **Staggered reveals**: 100-200ms delays between items
- **Hover effects**: Scale transforms and color transitions
- **Loading skeletons**: Pulse animations for all content areas

## Section Hierarchy (PRD Requirements)

The components must appear in this exact order on the MarketScanResults page:

1. **Region Cards** (pay ranges) - Horizontal layout
2. **Skills Section** - Must appear immediately after region cards
3. **Job Analysis Section** - Key insights with scannable format
4. **Next Steps Section** - Action-oriented guidance
5. **CTA Section** - Call-to-action blocks

## Usage Example

```tsx
import { 
  RegionCards, 
  SkillsSection, 
  JobAnalysisSection, 
  NextStepsSection, 
  CTASection 
} from '../components/ui'

function MarketScanResultsPage() {
  return (
    <div>
      {/* 1. Region Cards - FIRST */}
      <RegionCards salaryRecommendations={data.salary} />
      
      {/* 2. Skills Section - SECOND */}
      <SkillsSection skillsRecommendation={data.skills} />
      
      {/* 3. Job Analysis - THIRD */}
      <JobAnalysisSection jobAnalysis={data.analysis} />
      
      {/* 4. Next Steps - FOURTH */}
      <NextStepsSection onBookCall={handleBookCall} />
      
      {/* 5. CTA Section - FIFTH */}
      <CTASection layout="horizontal" />
    </div>
  )
}
```

## Demo Component

**MarketScanResultsDemo.tsx** provides a complete showcase of all components working together with sample data, demonstrating:

- Proper section hierarchy
- Responsive behavior
- Loading states
- Interactive features
- Brand color implementation
- Accessibility features

To view the demo:
```bash
# Import and use in your route
import { MarketScanResultsDemo } from '../components/ui'
```

## Accessibility Features

All components include:
- **ARIA labels** for interactive elements and icons
- **Semantic HTML** structure with proper heading hierarchy
- **Keyboard navigation** support
- **Color contrast** compliance with WCAG guidelines
- **Screen reader** friendly content structure

## Performance Optimizations

- **Loading states** with skeleton animations
- **Optimized animations** using CSS transforms
- **Responsive images** and icons
- **Minimal re-renders** with React.memo where appropriate
- **Efficient CSS** using Tailwind utility classes

## Future Enhancements

- **Framer Motion** integration for advanced animations
- **Intersection Observer** for scroll-triggered animations
- **A/B testing** support for different CTA variations
- **Analytics tracking** for user interactions
- **Dark mode** support with theme switching