# Quality Gates: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-19
**Feature**: specs/001-textbook-chapter-specs/
**Status**: Complete

## Overview

This document defines the quality gates that all textbook content must pass before being merged into the main branch. These gates ensure consistency, accuracy, and educational value across all chapters.

## Pre-Merge PR Checks

### Automated Validation Pipeline

Every pull request triggers the following automated checks:

1. **Build Validation**
   - Docusaurus builds successfully (`npm run build`)
   - No build errors or warnings
   - All pages generate correctly

2. **Markdown Linting**
   - Follows `.mdlintrc` rules
   - Proper heading hierarchy (no skipped levels)
   - Line length compliance (≤120 characters)
   - Code block language specification

3. **Link Validation**
   - All internal links resolve correctly
   - External links return 200 OK status
   - No broken references or 404 errors

4. **Code Syntax Validation**
   - Python code blocks are syntactically valid
   - YAML code blocks are properly formatted
   - Bash scripts follow shellcheck guidelines

5. **Accessibility Check**
   - All images have alt text (≥20 characters)
   - Proper heading hierarchy maintained
   - Lighthouse accessibility score ≥90

### Constitutional Compliance Gates

Each chapter must pass the 6 constitutional principles:

1. **Technical Accuracy & Verifiability**
   - All claims verifiable from official documentation
   - Code examples tested on target platforms
   - Version information current and accurate

2. **Educational Clarity**
   - Reading level appropriate for Grade 8-12
   - Clear learning objectives and outcomes
   - Progressive difficulty (simple → advanced)

3. **Modular Architecture**
   - Chapter can be read independently
   - Proper connections to previous/next chapters
   - Self-contained learning experience

4. **Consistency & Quality**
   - Consistent terminology across chapters
   - Uniform formatting and structure
   - Professional tone and style

5. **Original Content**
   - No copy-paste from other sources
   - Synthesized from multiple authoritative sources
   - Proper attribution and citations

6. **Deployment Readiness**
   - Builds successfully in Docusaurus
   - All links and images resolve
   - Cross-platform compatibility verified

## Manual Review Gates

In addition to automated checks, each chapter requires manual review:

### Technical Review
- [ ] Code examples run successfully on Ubuntu 22.04
- [ ] Code examples run successfully on Windows 10/11
- [ ] Code examples run successfully on macOS 12+
- [ ] All commands work as documented
- [ ] Expected outputs match actual results

### Educational Review
- [ ] Learning objectives are specific and measurable
- [ ] Exercises have clear steps and expected outputs
- [ ] Self-assessment questions are appropriate
- [ ] Prerequisites are clearly stated
- [ ] Content appropriate for stated difficulty level

### Quality Review
- [ ] Minimum content requirements met:
  - ≥2 hands-on exercises per chapter
  - ≥3 code examples per chapter
  - ≥1 diagram per chapter
  - ≥5 self-assessment questions
- [ ] Diagrams have descriptive alt text
- [ ] All external references are current and valid
- [ ] Cross-references to other chapters are correct

## Gate Failure Handling

### Automated Gate Failures
- PRs failing automated checks are blocked from merging
- Author receives specific error messages with failure details
- Author must address all failures before re-requesting review

### Manual Gate Failures
- Reviewer provides specific feedback in PR comments
- Author addresses feedback and requests another review
- Critical failures require additional review by subject matter expert

## Platform Testing Gates

### Cross-Platform Validation
- [ ] Installation instructions tested on all 3 platforms
- [ ] Code examples execute on all 3 platforms
- [ ] Expected outputs consistent across platforms
- [ ] Platform-specific troubleshooting documented

### Performance Gates
- [ ] Docusaurus build completes in <30 seconds
- [ ] Page load time <2 seconds on good network
- [ ] Lighthouse performance score ≥90
- [ ] All images optimized for web delivery

## Content-Specific Gates

### Module 1: ROS 2 Gates
- [ ] ROS 2 Humble compatibility verified
- [ ] All `ros2` commands work as documented
- [ ] Package dependencies clearly specified

### Module 2: Simulation Gates
- [ ] Gazebo Fortress compatibility verified
- [ ] URDF/SDF models load correctly
- [ ] Unity visualization components work

### Module 3: AI/Isaac Gates
- [ ] Isaac Sim 2023.1 compatibility verified
- [ ] RL training examples complete successfully
- [ ] Model deployment verified

### Module 4: VLA Gates
- [ ] Vision-language-action pipeline works
- [ ] All AI components integrate properly
- [ ] Capstone project components function

## Gate Configuration

### GitHub Actions Workflow Integration
```yaml
# Build validation gate
build-check:
  needs: [linting, security]
  if: success()
  steps:
    - run: npm run build
    - verify: build artifacts exist and are valid

# Link validation gate
link-check:
  needs: build-check
  if: success()
  steps:
    - check: all internal links resolve
    - verify: external links return 200 OK

# Constitutional compliance gate
constitution-check:
  needs: [build-check, link-check]
  steps:
    - run: scripts/validate-chapter.py
    - verify: all 6 constitutional principles pass
```

### Validation Script Integration
- `scripts/validate-chapter.py` runs on every chapter
- Reports detailed validation results
- Exits with error code if gates fail

## Gate Maintenance

### Regular Review
- Quality gates reviewed monthly
- Thresholds adjusted based on feedback
- New gates added as needed

### Exception Handling
- Temporary gate waivers possible for valid reasons
- Exception requests require team approval
- Waivers automatically expire after 30 days

## Success Metrics

### Quality Indicators
- Zero broken links in published content
- 100% constitutional compliance rate
- <1% post-publication corrections needed
- Student satisfaction score ≥4.5/5.0

### Process Metrics
- Average PR review time <48 hours
- Automated gate pass rate >90%
- Manual review efficiency >80%

## Responsibilities

### Authors
- Ensure content passes all quality gates
- Address gate failures promptly
- Follow validation guidelines

### Reviewers
- Verify manual review gates
- Approve content meeting quality standards
- Provide constructive feedback

### Maintainers
- Maintain and update quality gates
- Monitor gate effectiveness
- Improve validation processes

---

*This document is maintained by the textbook development team and updated as processes evolve.*