---
id: 4
title: fix-docusaurus-build-plan
stage: plan
date: 2025-12-20
surface: agent
model: claude-haiku-4-5-20251001
feature: fix-docusaurus-build
branch: 003-fix-docusaurus-build
user: claude
command: /sp.plan
labels: [docusaurus, build, links, landing-page, planning]
links:
  spec: specs/003-fix-docusaurus-build/spec.md
  plan: specs/003-fix-docusaurus-build/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-fix-docusaurus-build/plan.md
 - specs/003-fix-docusaurus-build/research.md
 - specs/003-fix-docusaurus-build/data-model.md
 - specs/003-fix-docusaurus-build/quickstart.md
 - specs/003-fix-docusaurus-build/contracts/README.md
tests:
 - null
---

## Prompt

```text
Based on the specification, create a step-by-step implementation plan:

Configuration Fix: Check docusaurus.config.js. Specifically look at baseUrl, url, and onBrokenLinks. Set onBrokenLinks: 'warn' temporarily to allow deployment, but prioritize fixing the paths.

Home Page Logic: Modify src/pages/index.js to act as the Hero section. Extract data from the current docs home and implement a CTA (Call to Action) button using Docusaurus <Link> component.

Navbar Adjustment: Locate themeConfig.navbar.items in the config file. Remove the item with href pointing to GitHub. Update the title or logo object.

Deployment Readiness: Ensure the baseUrl is compatible with Vercel (usually / unless it's a sub-path).

Documentation: Draft a README.md with: Project Title, Introduction, Features (ROS2, Simulation, Isaac Sim, VLA), Installation steps, and Tech Stack.
```

## Response snapshot

Successfully created a comprehensive implementation plan for fixing Docusaurus build issues and improving the landing page. The plan includes:

- Technical context with project details (JavaScript/TypeScript, Docusaurus 3.x, Node.js)
- Constitution check ensuring all principles are met
- Detailed project structure showing all relevant files and directories
- Research findings identifying key issues (broken links, homepage location, navigation)
- Data model defining entities (Documentation Pages, Navigation Configuration, Homepage Component, Site Configuration)
- Quickstart guide for development and testing
- Contracts documentation for frontend interfaces

The plan addresses all requirements from the specification:
1. Configuration fixes for broken links
2. Homepage implementation with hero section and CTA
3. Navigation cleanup
4. Deployment readiness for GitHub Pages/Vercel
5. Repository documentation

## Outcome

- ✅ Impact: Created comprehensive implementation plan with all supporting artifacts
- 🧪 Tests: null
- 📁 Files: specs/003-fix-docusaurus-build/plan.md, research.md, data-model.md, quickstart.md, contracts/README.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Plan is comprehensive and ready for task generation phase

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): /sp.tasks to generate implementation tasks