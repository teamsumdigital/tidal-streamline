# CandidateCard Component

A comprehensive, accessible React component for displaying candidate profiles in the Tidal Streamline application. Built following atomic design principles and Tidal's frontend development standards.

## Features

- **TypeScript Support**: Fully typed with CandidateProfile interface
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation
- **Responsive Design**: Mobile-first approach with responsive breakpoints
- **Loading States**: Skeleton loading animation for better UX
- **Brand Consistency**: Uses Tidal color palette and design system
- **Interactive Elements**: Video intro links and contact buttons
- **Regional Savings Display**: Highlights cost savings vs US rates

## Usage

### Basic Implementation

```tsx
import { CandidateCard } from './components/ui'
import { CandidateProfile } from './services/types'

const candidate: CandidateProfile = {
  id: '1',
  name: 'Maria Santos',
  role_category: 'Ecommerce Manager',
  experience_years: '5-7 years',
  region: 'Philippines',
  skills: ['Shopify', 'Google Ads', 'Facebook Ads'],
  bio: 'Experienced ecommerce manager...',
  hourly_rate: 25,
  video_url: 'https://example.com/video',
  availability: 'Full-time',
  english_proficiency: 'Fluent',
  timezone: 'GMT+8'
}

function CandidateList() {
  const handleContact = (candidate: CandidateProfile) => {
    // Handle contact logic
    console.log('Contact:', candidate.name)
  }

  return (
    <CandidateCard
      candidate={candidate}
      onContactClick={handleContact}
      regionalSavings={65}
    />
  )
}
```

### Loading State

```tsx
<CandidateCard
  candidate={{} as CandidateProfile}
  onContactClick={() => {}}
  isLoading={true}
/>
```

### Grid Layout

```tsx
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  {candidates.map((candidate) => (
    <CandidateCard
      key={candidate.id}
      candidate={candidate}
      onContactClick={handleContact}
      regionalSavings={calculateSavings(candidate.region)}
    />
  ))}
</div>
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `candidate` | `CandidateProfile` | Yes | Complete candidate profile data |
| `onContactClick` | `(candidate: CandidateProfile) => void` | Yes | Handler for contact button clicks |
| `regionalSavings` | `number` | No | Percentage savings vs US rates |
| `isLoading` | `boolean` | No | Shows skeleton loading state |
| `className` | `string` | No | Additional CSS classes |

## CandidateProfile Interface

```typescript
interface CandidateProfile {
  id: string
  name: string
  role_category: string
  experience_years: string
  region: string
  skills: string[]
  bio: string
  video_url?: string
  resume_url?: string
  portfolio_url?: string
  hourly_rate?: number
  availability: string
  english_proficiency: string
  timezone: string
}
```

## Accessibility Features

- **Keyboard Navigation**: All interactive elements are keyboard accessible
- **ARIA Labels**: Descriptive labels for screen readers
- **Focus Management**: Clear focus indicators and logical tab order
- **Semantic HTML**: Proper heading hierarchy and landmark elements
- **Color Contrast**: Meets WCAG AA standards

## Design Tokens

The component uses Tidal's design system:

- **Colors**: `tidal-50` through `tidal-900` for brand colors
- **Typography**: Inter font family with proper weight hierarchy
- **Spacing**: Tailwind spacing scale (4, 6, 8, 12, 16)
- **Shadows**: Card shadow system for depth

## Browser Support

- Modern browsers with ES2017+ support
- Mobile Safari iOS 12+
- Chrome 70+
- Firefox 60+
- Edge 79+

## Performance

- **Bundle Size**: ~3KB gzipped
- **Render Time**: Optimized for lists of 100+ candidates
- **Memory Usage**: Minimal re-renders with proper memoization

## Demo

Visit `/demo/candidate-card` in development to see all component variations and states.

## Testing

The component includes comprehensive test coverage:

- Unit tests for all props and states
- Accessibility testing with Jest and Testing Library
- Visual regression tests for design consistency
- Keyboard navigation testing

## Related Components

- **CandidateList**: Container component for candidate grids
- **ContactModal**: Modal triggered by contact button
- **SkillBadge**: Individual skill display component