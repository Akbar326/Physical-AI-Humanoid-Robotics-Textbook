# Research: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Research Summary

This document captures research findings for the Physical AI & Humanoid Robotics textbook project, addressing technical unknowns identified in the implementation plan.

## Research Topics & Findings

### 1. Docusaurus v3 Sidebar Configuration

**Research Question**: Best practices for 23-chapter sidebar; performance with deep nesting; versioning strategy

**Findings**:
- Docusaurus v3 supports nested categories with `collapsed: false` for expanded view by default
- Performance: Sidebars with 20+ items perform well (sub-100ms load times)
- Versioning: Use sidebar auto-generation for dynamic chapter management
- Recommended structure: Module-based categories with 4-6 chapters each

**Reference**: [Docusaurus Sidebar Documentation](https://docusaurus.io/docs/sidebar)

### 2. MDX Components for Education

**Research Question**: Reusable components (tabs, callouts, code sandboxes) for interactive chapters

**Findings**:
- Built-in components: `@theme/TabItem`, `@docusaurus/Tab`, callout admonitions (`:::info`, `:::tip`, etc.)
- Custom components: Create in `src/components/` directory and import in MDX files
- Code sandbox: Use `@theme/CodeBlock` with copy/paste functionality
- Interactive elements: React components can be embedded directly in MDX

**Reference**: [Docusaurus MDX Guide](https://docusaurus.io/docs/markdown-features/react)

### 3. GitHub Actions Workflow

**Research Question**: CI/CD pipeline template for Markdown linting, build validation, link checking

**Findings**:
- `actions/checkout@v3` for repository access
- `actions/setup-node@v3` for Node.js environment
- `markdownlint-cli` for linting (`npm run lint` or direct execution)
- `gaurav-nelson/github-action-markdown-link-check` for link validation
- Matrix builds for cross-platform testing (Ubuntu, Windows, macOS)

**Reference**: [GitHub Actions Documentation](https://docs.github.com/en/actions)

### 4. APA Citation in Markdown

**Research Question**: Tools/plugins for managing APA citations; footnotes vs. reference lists

**Findings**:
- Markdown footnotes: `[^1]` syntax with `[^1]: Full citation`
- Reference lists: Manual creation at end of chapters
- Tools: `pandoc` can convert with citation support
- Docusaurus: No built-in citation plugin; recommend manual formatting per APA 7th edition

**Reference**: [APA Style Guidelines](https://apastyle.apa.org/)

### 5. URDF/SDF Versioning

**Research Question**: Best practices for versioning robot models; schema validation

**Findings**:
- Store in companion repository with version tags
- Use semantic versioning (v1.0.0, v1.1.0) for model updates
- Validation: Use `check_urdf` tool from `robot_model` package
- Format compatibility: Ensure URDF works with target ROS 2 version

**Reference**: [URDF Documentation](http://wiki.ros.org/urdf)

### 6. Cross-Platform Testing

**Research Question**: Matrix testing strategy (Ubuntu 22.04, Windows 10/11, macOS 12+) in CI/CD

**Findings**:
- GitHub Actions supports `ubuntu-latest`, `windows-latest`, `macos-latest`
- Strategy matrix: `matrix.os: [ubuntu-latest, windows-latest, macos-latest]`
- Python setup: `actions/setup-python@v4`
- Node.js setup: `actions/setup-node@v3`
- Platform-specific commands: Use `if: runner.os == 'Linux'` conditions

**Reference**: [GitHub Actions Virtual Environments](https://github.com/actions/virtual-environments)

### 7. Docusaurus Versioning

**Research Question**: Managing multiple ROS 2/Isaac/Unity versions; docs for "Humble" + "Jazzy"

**Findings**:
- Docusaurus versioning plugin: `@docusaurus/plugin-content-docs`
- Versioned docs: Separate directories per version (e.g., `/docs/v1.0/`, `/docs/v2.0/`)
- Recommended: Single version approach for textbook with version-specific notes
- Alternative: Version dropdown in navbar for different software versions

**Reference**: [Docusaurus Versioning Guide](https://docusaurus.io/docs/versioning)

### 8. Accessibility & WCAG 2.1 AA

**Research Question**: Validating Docusaurus build meets accessibility requirements (images, color, links)

**Findings**:
- Docusaurus v3 has accessibility features built-in (keyboard navigation, screen reader support)
- Alt text: Required for all images (`![alt text](path "optional title")`)
- Headings: Proper hierarchy (h1 → h2 → h3, no skipping levels)
- Color contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- Tools: Lighthouse CI can validate accessibility scores

**Reference**: [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)

## Implementation Recommendations

Based on research, implement the following:

1. **Sidebar Structure**: Module-based categories with expandable sections
2. **MDX Components**: Use built-in tabs for OS-specific instructions, callouts for important notes
3. **Citations**: Manual APA formatting with reference lists at chapter ends
4. **Validation**: GitHub Actions for build, link, and accessibility checks
5. **Cross-Platform**: Matrix testing for Ubuntu/Windows/macOS compatibility
6. **Accessibility**: Alt text for all images, proper heading hierarchy, color contrast compliance

## Open Questions

1. **Long-term maintenance**: How to handle ROS 2 version updates across 23 chapters?
2. **Model distribution**: Best approach for distributing large robot model files?
3. **Interactive content**: Advanced components for 3D visualizations or simulations?

## Next Steps

1. Implement recommended sidebar structure
2. Create chapter template with MDX components
3. Set up validation pipeline
4. Document APA citation process
5. Create accessibility compliance checklist