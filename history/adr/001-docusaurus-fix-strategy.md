# ADR: Docusaurus Build Fix and Landing Page Strategy

## Status
Proposed

## Date
2025-12-20

## Context
The AI/Humanoid Robotics textbook website is experiencing build failures due to broken internal links and has an inadequate landing page experience. The current configuration has `onBrokenLinks: 'throw'` which prevents deployment, and the homepage is located at `docs/index.md` rather than a proper custom landing page. The site needs to maintain compatibility with GitHub Pages while potentially supporting Vercel deployment.

## Decision
We will implement a multi-faceted approach to fix the Docusaurus site:

1. **Configuration Fix**: Temporarily set `onBrokenLinks: 'warn'` in `docusaurus.config.js` while systematically fixing broken links, then revert to `'throw'` to maintain quality.

2. **Landing Page Strategy**: Create a custom landing page at `src/pages/index.js` that extracts content from the current `docs/index.md` and adds a hero section with a "Start Learning" call-to-action button.

3. **Navigation Cleanup**: Remove the GitHub link from the navigation bar and replace the missing logo with a text-based logo related to "Robotics Textbook".

4. **Deployment Strategy**: Maintain GitHub Pages compatibility while ensuring configuration works for Vercel deployment.

## Consequences

### Positive
- Site will build successfully without broken link errors
- Improved user experience with engaging landing page
- Better navigation without distracting GitHub link
- Professional appearance with proper branding
- Maintains compatibility with existing documentation structure
- Clear path for users to begin learning

### Negative
- Requires refactoring of existing navigation structure
- May need to update internal links to maintain consistency
- Temporary setting of `onBrokenLinks: 'warn'` could mask new issues during development

### Risks
- Changes to base URL configuration could break existing deep links
- Migration of homepage content requires careful testing across all pages
- Navigation changes might affect user workflows for those expecting GitHub link

## Alternatives

### Alternative 1: Minimal Fix Approach
- Only fix broken links without changing homepage or navigation
- Keep existing `docs/index.md` as homepage
- Maintain current navigation structure

### Alternative 2: Complete Redesign
- Redesign entire site architecture
- Implement custom React components for all pages
- Use different static site generator

### Alternative 3: Incremental Approach
- Fix broken links first
- Deploy with temporary fixes
- Implement landing page and navigation changes in separate releases

## References
- `specs/003-fix-docusaurus-build/plan.md`
- `specs/003-fix-docusaurus-build/research.md`
- `docusaurus.config.js`
- `docs/index.md`