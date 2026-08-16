---
name: Lumina Medical AI (Light Mode)
colors:
  surface: '#FFFFFF'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f4'
  surface-container: '#F8FAFC'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#3f484e'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#E2E8F0'
  outline-variant: '#bfc8cf'
  surface-tint: '#00658b'
  primary: '#006184'
  on-primary: '#ffffff'
  primary-container: '#007ba7'
  on-primary-container: '#f5faff'
  inverse-primary: '#7cd0ff'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#8df1e0'
  on-secondary-container: '#006f63'
  tertiary: '#8a4900'
  on-tertiary: '#ffffff'
  tertiary-container: '#ae5e00'
  on-tertiary-container: '#fff8f5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7cd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#90f4e3'
  secondary-fixed-dim: '#73d8c7'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005047'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
  on-surface-heading: '#1A1A1A'
  on-surface-body: '#475569'
  primary-cyan: '#007BA7'
  success-teal: '#008577'
  warning-amber: '#D97706'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base-unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  container-max: 1200px
---

## Brand & Style
The design system is engineered for a high-stakes medical context where precision, clarity, and trust are paramount. It transitions from its original dark-mode foundation to a **Modern Corporate** light aesthetic, prioritizing a clinical, "lab-clean" environment. 

The visual language is rooted in **Minimalism** with a focus on high legibility and professional authority. By utilizing a crisp white background, the system evokes a sense of hygiene and transparency essential for healthcare AI. The interface avoids decorative excess, relying on generous whitespace and a rigorous grid to convey intelligence and professional care. The target audience—clinicians and patients—should experience an emotional response of security, precision, and modern medical excellence.

## Colors
The palette is centered on a "Medical White" foundation (#FFFFFF) to establish a sterile and trustworthy environment.

- **Primary (Accessible Cyan):** Darkened to #007BA7 to maintain WCAG AA accessibility against white surfaces. Reserved for AI-driven insights, primary actions, and active diagnostic states.
- **Secondary (Teal):** Used for human-centric elements like "Verified Doctor" badges and appointment scheduling.
- **Tertiary (Muted Amber):** Strictly limited to warnings or irregular scan findings.
- **Neutrals:** Uses a sophisticated scale of slates. Headings use **Dark Charcoal (#1A1A1A)** for maximum impact, while body text uses **Slate Gray (#475569)** to reduce cognitive load during long reading sessions.

## Typography
This design system utilizes **Inter** exclusively for its exceptional legibility in technical and data-dense medical contexts.

- **Contrast Strategy:** All headings (`display`, `headline`, `title`) must be rendered in Dark Charcoal to anchor the page. Descriptive content and instructional text (`body`) use Slate Gray to provide a softer reading experience.
- **Scale:** Large display sizes are optimized for high-stakes AI diagnoses, while `label-sm` is strictly for metadata and secondary timestamps.
- **Clarity:** Maintain tight letter-spacing on larger headings to keep the medical aesthetic "crisp" and professional.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a strict 4px baseline rhythm to ensure mathematical precision across the UI.

- **Grid Systems:** A 12-column grid is used for desktop (centered in a 1200px container) and a 4-column grid for mobile.
- **Rhythm:** Vertical spacing is used to define hierarchy. Use `stack-lg` to separate major clinical sections. Use `stack-sm` to bind labels to their inputs or metadata to medical imagery.
- **Margins:** Generous outer margins (`margin-desktop`) are mandatory to maintain the "Minimalist" high-end medical feel and prevent the UI from feeling cramped.

## Elevation & Depth
In this light-mode system, depth is conveyed through **Tonal Layering** and **Low-Contrast Outlines** to maintain a flat, modern clinical aesthetic.

- **Surface 0:** Pure White (#FFFFFF) serves as the global canvas.
- **Surface 1 (Containers):** Very light gray/slate (#F8FAFC) used to differentiate card backgrounds from the main page.
- **Outlines:** Instead of heavy shadows, use 1px solid borders (#E2E8F0) to define element boundaries.
- **Shadows:** Reserved only for floating elements (Modals, Popovers). Use highly diffused, low-opacity shadows (Slate-900 at 8% opacity, 24px blur) to suggest height without adding visual "weight."
- **Glassmorphism:** Navigation headers may use a semi-transparent white background with a 12px backdrop blur to maintain clinical context while scrolling.

## Shapes
The shape language follows the `ROUND_EIGHT` standard to create a sophisticated yet approachable medical environment.

- **Clinical Containers:** Use `rounded-xl` (1.5rem) for cards and diagnostic modules to soften the technical nature of the AI.
- **Interactive Elements:** Buttons and form inputs use `rounded-lg` (1rem), providing a distinct "touchable" feel that remains professional.
- **Data Tags:** Status chips and badges use pill-shapes (full round) to distinguish them from structural layout elements.

## Components
- **Buttons:** Primary buttons use a solid Cyan (#007BA7) fill with White text. Secondary buttons are "ghost" style with a Slate-200 border and Dark Charcoal text.
- **Medical Cards:** The primary container. Features 24px internal padding, `rounded-xl` corners, and a 1px Slate-200 border. Content is divided by subtle horizontal rules.
- **Input Fields:** Use a white background with a Slate-200 border. On focus, the border transitions to Primary Cyan with a subtle 2px soft outer glow.
- **AI Scan Viewer:** A specialized component with a thick Slate-900 frame and a pulsing Cyan scanning indicator. 
- **Status Chips:** Pill-shaped. Use low-saturation background tints (e.g., Success Teal at 10% opacity) with high-saturation text for readability.
- **Icons:** 2px stroke width. Use Slate-500 for standard states and Primary Cyan for AI-specific features or active navigation.