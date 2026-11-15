---
name: Aegis Tactical HUD
colors:
  surface: '#0f141a'
  surface-dim: '#0f141a'
  surface-bright: '#353941'
  surface-container-lowest: '#0a0e15'
  surface-container-low: '#181c23'
  surface-container: '#1c2027'
  surface-container-high: '#262a31'
  surface-container-highest: '#31353c'
  on-surface: '#dfe2ec'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dfe2ec'
  inverse-on-surface: '#2c3138'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dce6'
  primary: '#e3fdff'
  on-primary: '#00373a'
  primary-container: '#00f3ff'
  on-primary-container: '#006b71'
  inverse-primary: '#00696f'
  secondary: '#b3c5ff'
  on-secondary: '#002b75'
  secondary-container: '#0266ff'
  on-secondary-container: '#f9f7ff'
  tertiary: '#fff6fd'
  on-tertiary: '#4e0078'
  tertiary-container: '#f1d1ff'
  on-tertiary-container: '#9500df'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ff6ff'
  primary-fixed-dim: '#00dce6'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#dae1ff'
  secondary-fixed-dim: '#b3c5ff'
  on-secondary-fixed: '#001849'
  on-secondary-fixed-variant: '#003fa4'
  tertiary-fixed: '#f4d9ff'
  tertiary-fixed-dim: '#e5b5ff'
  on-tertiary-fixed: '#30004b'
  on-tertiary-fixed-variant: '#7000a8'
  background: '#0f141a'
  on-background: '#dfe2ec'
  surface-variant: '#31353c'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: 0.08em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: 0.06em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: 0.06em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: 0.04em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: 0.04em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.01em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.12em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.14em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 9px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.18em
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1.5rem
  margin-lg: 2.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies an ultra-advanced executive military and aerospace heads-up display (HUD). Conceived at the intersection of holographic optics, orbital command telemetry, and cyber-defense command centers, it translates complex operational metrics into razor-sharp, luminescent data visualisations.

The visual style blends **Dark Neon Holography**, **Glassmorphic Optics**, and **Precision Technical Geometry**. Elements project out of a deep vacuum abyss with millimeter-grade lines, chamfered framing, tactile glass enclosures, and phosphorescent photon blooms. 

Target audience: Aerospace commanders, cyber-warfare tacticians, and executive orbital operators demanding instantaneous visual processing, military-grade situational awareness, and total informational clarity.

## Colors

The palette simulates optical laser projections on dark-tinted cockpit visor acrylic.

- **Deep Space Void (`#04070D`)**: Primary backdrop absorbency, representing total vacuum.
- **Sub-Surface Translucent Navy (`#08101E` at 70-85% alpha)**: Glassmorphic structural panels with backdrop filtration.
- **Hyper-Cyan Primary (`#00F3FF`)**: Active HUD readouts, standard reticles, navigational trajectories, and focal interactive states.
- **Electric Blue Secondary (`#0066FF`)**: System telemetry, sub-grids, structural scaffolding, and inactive conduits.
- **Tactical Magenta Alert (`#B026FF`)**: Strategic critical alerts, priority anomalies, and threat vectors.
- **Quantum Emerald Auxiliary (`#00FFA3`)**: Verified telemetry, operational stability, and nominal structural diagnostics.
- **Hazard Amber Auxiliary (`#FFB800`)**: Cautionary thresholds, telemetry sync latency, and defensive standby.

All luminous colors must incorporate variable bloom values: crisp interior core with atmospheric phosphor bleeding.

## Typography

Typography prioritizes rapid alphanumeric disambiguation under mission-critical visual strain. 

- **Space Grotesk** serves as the commanding display face, conveying advanced aerospace industrialism and geometric rigidity. Set titles and sector labels in uppercase with pronounced letter-spacing.
- **Inter** provides neutral, high-density clarity for narrative reports, debriefings, and logs where character distinction cannot be compromised.
- **JetBrains Mono** delivers fixed-pitch technical precision for coordinates, timestamp vectors, encryption ciphers, and raw operational telemetry. Always format tactical labels in full capitals.

## Layout & Spacing

The structural layout utilizes a dense, tactical **12-column dynamic modular matrix** overlaid with millimeter micro-grids (rendered as faint `rgba(0, 243, 255, 0.03)` repeating dot/cross patterns).

- **Margins**: Controlled perimeter margins frame the viewport like a cockpit windshield or helmet visor, preventing information bleed to edge bezels.
- **Responsive Adaptations**:
  - **Desktop (1440px+)**: Multi-viewport command split screen; persistent orbital telemetry side-rails and centralized holographic tactical maps.
  - **Tablet / Combat Slate (768px - 1439px)**: 8-column layout; secondary panels collapse into drawer overlays; critical telemetry collapses to upper HUD status bands.
  - **Mobile / Field Device (<768px)**: 4-column single-stack stream; micro-gutters (`space-sm`); tactical tabs swap viewports between Sector Maps, Diagnostics, and Vector Commands.

## Elevation & Depth

Visual hierarchy does not rely on traditional drop shadows. Elevation is achieved through **luminescence intensity**, **chromatic saturation**, and **optical glass tiers**:

1. **Backdrop Layer (0)**: Solid `#04070D` base overlaid with a calibrated 24px micro-dot holographic projection grid.
2. **Structural Chassis (1)**: Dark glass surfaces (`rgba(8, 16, 30, 0.65)`) with `backdrop-filter: blur(16px)` and 1px ghost borders (`rgba(0, 243, 255, 0.15)`).
3. **Elevated Panels & Diagnostics (2)**: Tinted glass (`rgba(10, 24, 46, 0.8)`) with `backdrop-filter: blur(24px)` framed by dual-tone borders: hairline outer cyan border with an inner corner accent bracket.
4. **Interactive Overlays & Critical Alerts (3)**: Floating targeting pods with intense neon outer phosphorescence (`box-shadow: 0 0 20px rgba(0, 243, 255, 0.35), inset 0 0 15px rgba(0, 243, 255, 0.1)`).
5. **Tactical Threat Modals (4)**: Magenta emergency lockouts illuminated with dual-layer bloom (`box-shadow: 0 0 35px rgba(176, 38, 255, 0.5)`).

## Shapes

The HUD rejects organic roundness in favor of **angular, faceted, and chamfered geometries** that echo stealth aerospace surfaces and military targeting reticles.

- **Radii**: Absolute zero curvature (`roundedness: 0`).
- **Chamfered Offsets**: Panels utilize 45-degree clipped corners (cut corners via CSS `clip-path: polygon(...)`) with variable corner-cut sizes (4px to 12px depending on panel scale).
- **Corner Brackets**: Key cards feature distinct L-shaped targeting brackets at outer vertices with a stroke thickness of 1.5px.
- **Hairline Dividers**: Micro-segmented rule dividers with center chevron gaps or crosshair nodes.

## Components

### Buttons & Trigger Actuators
- **Primary**: Hyper-Cyan wireframe button with cut corners, 1px solid `#00F3FF`, fill `rgba(0, 243, 255, 0.12)`, font `JetBrains Mono` bold uppercase with `letter-spacing: 0.12em`. Hover creates an intense flash transition to full `#00F3FF` fill with black text and an exterior cyan glow (`box-shadow: 0 0 18px #00F3FF`).
- **Secondary**: Semi-translucent dark slate fill with electric blue border (`#0066FF`), subtle hover bloom.
- **Destructive/Emergency**: Magenta `#B026FF` border and phosphor pulsing glow with striped diagonal caution lines (`repeating-linear-gradient`).

### Tactical Chips & Status Badges
- Ultra-compact, border-bracketed tags set in `label-sm`.
- Prefixed with systemic telemetry indicators: e.g., `[SYS::NOMINAL]` in Quantum Emerald (`#00FFA3`), `[WARN::ALT]` in Hazard Amber (`#FFB800`), or `[LOCK::TARGET]` in Hyper-Cyan (`#00F3FF`).
- Background: 10% opacity match of the indicator color; 1px subtle matching border.

### HUD Cards & Modular Enclosures
- Dark semi-transparent acrylic panes with 45-degree clipped top-right or diagonal corner notches.
- Framed with 1px border lines and accentuated corner ticks (`+` marks or `L` vertices).
- Header contains a monospace ID code (e.g., `SEC-09 // TELEMETRY`) alongside a horizontal signal bar indicator.

### Telemetry Lists & Data Grids
- Alternating rows rendered with subtle `rgba(0, 243, 255, 0.02)` zebra bands.
- Cell dividers use 1px dotted borders (`rgba(0, 102, 255, 0.2)`).
- Data alignment strictly tabular using `JetBrains Mono` figures for rapid eye scanning.

### Input Fields & Command Terminals
- Deep black fill (`#020408`) with an inset terminal shadow.
- Cyan hairline bottom border or four-corner bracket framing.
- Flashing block cursor (`▋`) in `#00F3FF`. Monospace placeholder text with `0.1em` letter spacing.

### Checkboxes, Toggles & Reticle Switches
- **Checkboxes**: Diamond or chamfered square wireframes. Active state fills with a solid cyan diamond and a localized glow dot.
- **Switches**: Horizontal vector slide rails with angled segment thumbs that leave an illuminated trace wire behind them.

### Sector Radar & Reticle Targets (Specialty Component)
- Concentric circular or octagonal coordinate wireframes with 360-degree radial degree markings.
- Sweeping radar gradient line with subtle persistence phosphor decay.