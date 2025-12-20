# Research: Fix Docusaurus Build Issues and Landing Page

## Current State Analysis

### Project Structure
- **Configuration**: `docusaurus.config.js` - Contains site configuration with baseUrl: '/physical-ai-robotics-textbook/'
- **Documentation**: `docs/index.md` - Current landing page content
- **Styling**: `src/css/custom.css` - Custom styles
- **Sidebar**: `sidebars.js` - Navigation structure
- **Components**: `src/components/` - Custom React components

### Key Issues Identified

1. **Broken Links**:
   - Current configuration has `onBrokenLinks: 'throw'` which causes build failures
   - Base URL is set to `/physical-ai-robotics-textbook/` which may cause path issues

2. **Homepage**:
   - Current homepage is at `docs/index.md`
   - Needs to be moved to a proper landing page at root (`src/pages/index.js`)

3. **Navigation**:
   - GitHub link exists in navbar at line 77-80 in config
   - Logo is referenced as `img/logo.svg` which may be missing

4. **Build Configuration**:
   - Site is configured for GitHub Pages deployment
   - Base URL may need adjustment for Vercel deployment

## Decisions & Rationale

### Decision: Configuration Fix
**Rationale**: The `onBrokenLinks: 'throw'` setting prevents deployment. Need to temporarily set to 'warn' while fixing links.

### Decision: Homepage Implementation
**Rationale**: Docusaurus allows custom pages in `src/pages/`. Need to create `src/pages/index.js` with hero section and CTA.

### Decision: Navigation Cleanup
**Rationale**: Remove GitHub link from navbar and update logo to text-based or placeholder.

## Implementation Strategy

1. Fix configuration issues in `docusaurus.config.js`
2. Create new landing page in `src/pages/index.js`
3. Update navigation in config file
4. Create README.md for repository

## Dependencies & Best Practices

- Docusaurus v3.x patterns for custom pages
- React components for landing page
- Docusaurus Link component for navigation
- GitHub Pages vs Vercel deployment considerations