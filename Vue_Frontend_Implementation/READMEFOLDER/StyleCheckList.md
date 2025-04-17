# Vue Frontend Style Checklist

This document provides a comprehensive style checklist for the Vue.js frontend implementation of the Loan Application System V2. Use this checklist to ensure consistency across the application.

## Color Palette

### Primary Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Primary | `#1976D2` | Primary actions, links, active states |
| Primary Light | `#42A5F5` | Hover states, backgrounds, secondary elements |
| Primary Dark | `#0D47A1` | Focus states, text on light backgrounds |

### Secondary Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Secondary | `#424242` | Secondary actions, headers, footers |
| Secondary Light | `#616161` | Hover states for secondary elements |
| Secondary Dark | `#212121` | Text, icons on light backgrounds |

### Accent Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Accent | `#82B1FF` | Highlights, call-to-action elements |
| Success | `#4CAF50` | Success messages, approved status |
| Warning | `#FFC107` | Warning messages, pending status |
| Error | `#FF5252` | Error messages, rejected status |
| Info | `#2196F3` | Information messages, submitted status |

### Neutral Colors

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| White | `#FFFFFF` | Backgrounds, text on dark surfaces |
| Grey 50 | `#FAFAFA` | Alternative backgrounds |
| Grey 100 | `#F5F5F5` | Dividers, borders |
| Grey 200 | `#EEEEEE` | Disabled states |
| Grey 300 | `#E0E0E0` | Borders, dividers |
| Grey 400 | `#BDBDBD` | Disabled text |
| Grey 500 | `#9E9E9E` | Placeholder text |
| Grey 600 | `#757575` | Secondary text |
| Grey 700 | `#616161` | Primary text |
| Grey 800 | `#424242` | Headings |
| Grey 900 | `#212121` | Emphasis text |
| Black | `#000000` | Text on light surfaces |

## Typography

### Font Family

- Primary Font: `'Roboto', sans-serif`
- Monospace Font: `'Roboto Mono', monospace` (for code blocks, numbers)

### Font Sizes

| Name | Size | Usage |
|------|------|-------|
| Display Large | 57px | Hero sections |
| Display Medium | 45px | Major headings |
| Display Small | 36px | Section headings |
| Headline Large | 32px | Page titles |
| Headline Medium | 28px | Major section headings |
| Headline Small | 24px | Section headings |
| Title Large | 22px | Card titles, modal headers |
| Title Medium | 16px | Strong emphasis, table headers |
| Title Small | 14px | Minor headings, labels |
| Body Large | 16px | Primary body text |
| Body Medium | 14px | Secondary body text |
| Body Small | 12px | Captions, helper text |
| Label Large | 14px | Button text, primary labels |
| Label Medium | 12px | Secondary labels |
| Label Small | 11px | Tertiary labels, metadata |

### Font Weights

- Light: 300
- Regular: 400
- Medium: 500
- Bold: 700

## Spacing

### Base Unit

- Base spacing unit: `8px`

### Spacing Scale

| Name | Size | Usage |
|------|------|-------|
| xs | 4px | Minimal spacing, icon padding |
| sm | 8px | Small elements, tight spacing |
| md | 16px | Standard spacing between elements |
| lg | 24px | Generous spacing, section padding |
| xl | 32px | Major section spacing |
| xxl | 48px | Page sections |
| xxxl | 64px | Major page sections |

### Component Spacing

- Card padding: `16px`
- Form field margin: `16px` (bottom)
- Section margin: `32px` (bottom)
- Page padding: `24px`

## Borders & Shadows

### Border Radius

| Name | Size | Usage |
|------|------|-------|
| None | 0 | Tables, dividers |
| Small | 4px | Buttons, inputs, chips |
| Medium | 8px | Cards, dialogs |
| Large | 16px | Floating action buttons |
| Pill | 9999px | Pills, badges |

### Shadows

| Name | Value | Usage |
|------|-------|-------|
| None | none | Flat elements |
| Low | `0 2px 4px rgba(0,0,0,0.1)` | Subtle elevation (cards) |
| Medium | `0 4px 8px rgba(0,0,0,0.12)` | Medium elevation (dialogs, dropdowns) |
| High | `0 8px 16px rgba(0,0,0,0.14)` | High elevation (modals) |
| Focus | `0 0 0 3px rgba(25,118,210,0.4)` | Focus states |

### Border Styles

| Name | Value | Usage |
|------|-------|-------|
| None | none | Most elements |
| Thin | `1px solid #E0E0E0` | Cards, dividers |
| Medium | `2px solid #E0E0E0` | Active states |
| Thick | `3px solid #E0E0E0` | Emphasis |

## Components

### Buttons

#### Primary Button

- Background: Primary (`#1976D2`)
- Text: White (`#FFFFFF`)
- Border Radius: Small (4px)
- Padding: `8px 16px`
- Font: Label Large (14px), Medium (500)
- Hover: Primary Light (`#42A5F5`)
- Active: Primary Dark (`#0D47A1`)
- Disabled: Grey 300 (`#E0E0E0`), Grey 500 text (`#9E9E9E`)

#### Secondary Button

- Background: White (`#FFFFFF`)
- Text: Primary (`#1976D2`)
- Border: `1px solid #1976D2`
- Border Radius: Small (4px)
- Padding: `8px 16px`
- Font: Label Large (14px), Medium (500)
- Hover: Primary 10% opacity background
- Active: Primary 20% opacity background
- Disabled: Grey 300 (`#E0E0E0`), Grey 500 text (`#9E9E9E`)

#### Text Button

- Background: Transparent
- Text: Primary (`#1976D2`)
- Border Radius: Small (4px)
- Padding: `8px 16px`
- Font: Label Large (14px), Medium (500)
- Hover: Primary 10% opacity background
- Active: Primary 20% opacity background
- Disabled: Grey 500 text (`#9E9E9E`)

### Form Elements

#### Text Input

- Background: White (`#FFFFFF`)
- Text: Grey 900 (`#212121`)
- Border: `1px solid #E0E0E0`
- Border Radius: Small (4px)
- Padding: `12px 16px`
- Font: Body Medium (14px), Regular (400)
- Focus: Border Primary (`#1976D2`), Shadow Focus
- Error: Border Error (`#FF5252`)
- Disabled: Background Grey 100 (`#F5F5F5`), Text Grey 500 (`#9E9E9E`)

#### Select

- Same as Text Input
- Dropdown Icon: Grey 600 (`#757575`)

#### Checkbox

- Border: `2px solid #9E9E9E`
- Border Radius: Small (4px)
- Size: 18px × 18px
- Checked: Background Primary (`#1976D2`), White check icon
- Focus: Shadow Focus
- Disabled: Grey 300 (`#E0E0E0`)

#### Radio Button

- Border: `2px solid #9E9E9E`
- Border Radius: Pill (9999px)
- Size: 18px × 18px
- Checked: Border Primary (`#1976D2`), Primary dot
- Focus: Shadow Focus
- Disabled: Grey 300 (`#E0E0E0`)

### Cards

- Background: White (`#FFFFFF`)
- Border Radius: Medium (8px)
- Shadow: Low
- Padding: `16px`
- Title: Title Large (22px), Medium (500)
- Subtitle: Body Medium (14px), Regular (400)
- Hover: Shadow Medium (optional)

### Tables

- Header Background: Grey 100 (`#F5F5F5`)
- Header Text: Grey 800 (`#424242`)
- Header Font: Title Medium (16px), Medium (500)
- Row Border: `1px solid #E0E0E0`
- Row Hover: Grey 50 (`#FAFAFA`)
- Cell Padding: `12px 16px`
- Cell Text: Body Medium (14px), Regular (400)
- Striped Rows: Alternate Grey 50 (`#FAFAFA`) (optional)

### Dialogs

- Background: White (`#FFFFFF`)
- Border Radius: Medium (8px)
- Shadow: High
- Padding: `24px`
- Title: Headline Small (24px), Medium (500)
- Content: Body Large (16px), Regular (400)
- Actions: Right-aligned, 16px top margin

### Alerts

#### Success Alert

- Background: Success 10% opacity
- Border-left: `4px solid #4CAF50`
- Text: Grey 900 (`#212121`)
- Icon: Success (`#4CAF50`)

#### Warning Alert

- Background: Warning 10% opacity
- Border-left: `4px solid #FFC107`
- Text: Grey 900 (`#212121`)
- Icon: Warning (`#FFC107`)

#### Error Alert

- Background: Error 10% opacity
- Border-left: `4px solid #FF5252`
- Text: Grey 900 (`#212121`)
- Icon: Error (`#FF5252`)

#### Info Alert

- Background: Info 10% opacity
- Border-left: `4px solid #2196F3`
- Text: Grey 900 (`#212121`)
- Icon: Info (`#2196F3`)

### Badges

- Size: Small
- Border Radius: Pill (9999px)
- Font: Label Small (11px), Medium (500)
- Padding: `2px 8px`
- Colors: Match status colors (Success, Warning, Error, Info)

### Chips

- Background: Grey 100 (`#F5F5F5`)
- Text: Grey 800 (`#424242`)
- Border Radius: Pill (9999px)
- Font: Label Medium (12px), Regular (400)
- Padding: `4px 12px`
- Hover: Grey 200 (`#EEEEEE`)
- Active: Grey 300 (`#E0E0E0`)
- With Icon: 8px padding between icon and text

### Icons

- Size: 24px × 24px (default)
- Color: Match text color or specific semantic color
- Button Icons: 20px × 20px
- Small Icons: 16px × 16px
- Large Icons: 32px × 32px

## Layout

### Container Widths

- Small: 600px max-width
- Medium: 960px max-width
- Large: 1280px max-width
- Extra Large: 1440px max-width

### Grid System

- 12-column grid
- Gutter: 24px
- Breakpoints:
  - xs: < 600px
  - sm: ≥ 600px
  - md: ≥ 960px
  - lg: ≥ 1280px
  - xl: ≥ 1440px

### Page Structure

- Header Height: 64px
- Sidebar Width: 256px
- Content Padding: 24px
- Footer Height: 48px

## Animation

### Durations

- Extra Fast: 100ms
- Fast: 200ms
- Normal: 300ms
- Slow: 500ms
- Extra Slow: 800ms

### Easing

- Standard: `cubic-bezier(0.4, 0.0, 0.2, 1)`
- Decelerate: `cubic-bezier(0.0, 0.0, 0.2, 1)`
- Accelerate: `cubic-bezier(0.4, 0.0, 1, 1)`

### Transitions

- Fade: Opacity 0 to 1
- Slide: Transform translateY or translateX
- Scale: Transform scale
- Combined: Combination of the above

## Accessibility

### Focus States

- Keyboard focus: Shadow Focus (`0 0 0 3px rgba(25,118,210,0.4)`)
- High contrast: Ensure sufficient contrast for focus indicators

### Color Contrast

- Text on background: Minimum 4.5:1 ratio
- Large text on background: Minimum 3:1 ratio
- UI components and graphical objects: Minimum 3:1 ratio

### Text Sizes

- Minimum text size: 12px
- Body text: 14px or 16px
- Ensure text remains readable when zoomed to 200%

## Responsive Design

### Breakpoint Behavior

- **Mobile (< 600px)**
  - Full-width components
  - Stacked layouts
  - Simplified navigation (hamburger menu)
  - Reduced padding (16px)
  - Simplified tables (cards instead of tables)

- **Tablet (600px - 959px)**
  - Two-column layouts
  - Sidebar navigation (collapsible)
  - Standard padding (24px)
  - Responsive tables (horizontal scroll)

- **Desktop (≥ 960px)**
  - Multi-column layouts
  - Full navigation
  - Standard padding (24px)
  - Full tables

### Touch Targets

- Minimum size: 44px × 44px
- Minimum spacing: 8px

## Implementation Checklist

- [ ] Set up Vuetify theme with custom color palette
- [ ] Create typography CSS variables
- [ ] Implement spacing system
- [ ] Create custom component styles
- [ ] Set up responsive breakpoints
- [ ] Implement animation utilities
- [ ] Create accessibility helpers
- [ ] Document style guide usage
- [ ] Create component examples
- [ ] Set up linting rules to enforce style guidelines
