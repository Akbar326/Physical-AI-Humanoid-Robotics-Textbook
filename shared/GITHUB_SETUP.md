# GitHub Repository Configuration Guide

## Overview

This guide documents the complete GitHub setup for the Physical AI & Humanoid Robotics textbook project, including repository settings, branch protection rules, CI/CD pipelines, and deployment configuration.

## Repository Information

**Main Repository:**
- Name: `ai-humanoid-robotics`
- Visibility: Public
- License: MIT (recommended)
- Description: "Physical AI & Humanoid Robotics - A comprehensive interactive textbook with 23 chapters across 4 modules"

**Companion Repository:**
- Name: `ai-humanoid-robotics-code`
- Visibility: Public
- License: MIT
- Description: "Code examples, exercises, and datasets for the Physical AI & Humanoid Robotics textbook"

## Part 1: Main Repository Configuration

### Step 1: Create Main Repository

```bash
# Using GitHub CLI
gh repo create ai-humanoid-robotics \
  --public \
  --description "Physical AI & Humanoid Robotics - Comprehensive interactive textbook" \
  --add-readme \
  --license MIT
```

### Step 2: Repository Settings

Navigate to **Settings** → configure:

#### General Settings

- **Description**: "Interactive textbook for learning Physical AI and Humanoid Robotics with ROS 2, Gazebo, Isaac Sim, and Vision-Language-Action models"
- **Website**: (leave empty or add GitHub Pages URL later)
- **Topics**: `robotics`, `ros2`, `gazebo`, `education`, `textbook`, `physical-ai`, `humanoid-robotics`
- **Features**:
  - ✅ Discussions (enable for community Q&A)
  - ✅ Sponsorships (optional)
  - ✅ Wikis (optional, for additional documentation)
  - ❌ Projects (not needed, using issues/PRs)

#### Default Behavior

- **Default branch**: `main`
- **Default branch for pull requests**: `main`
- **Automatically delete head branches**: ✅

### Step 3: Branch Protection Rules

Navigate to **Settings** → **Branches** → **Add Rule**

#### Rule 1: Main Branch Protection

```
Pattern: main
```

**Require:**
- [ ] Require a pull request before merging (Min 1 approval)
- [ ] Require status checks to pass before merging
  - [ ] Strict mode (requires up to date before merge)
  - Add required checks:
    - `Build & Validate`
    - `Cross-Platform Testing`
- [ ] Require code reviews before merging (1 required)
- [ ] Require conversation resolution before merging
- [ ] Include administrators in restrictions: ✅
- [ ] Restrict who can push to matching branches
- [ ] Allow force pushes: ❌
- [ ] Allow deletions: ❌

#### Rule 2: Develop Branch (if using)

```
Pattern: develop
```

- [ ] Require a pull request before merging
- [ ] Allow auto-merge: ✅

### Step 4: Configure GitHub Pages

Navigate to **Settings** → **Pages**

```
Source: Deploy from a branch
Branch: gh-pages (or use GitHub Actions)
Folder: / (root)
```

**Or use GitHub Actions (Recommended):**
- The `deploy.yml` workflow automatically handles this
- No manual configuration needed

### Step 5: Configure Environments

Navigate to **Settings** → **Environments**

#### Environment: Production

- **Deployment branches**: `main`
- **Required reviewers**: ✅ (if strict approval needed)

#### Environment: Staging (optional)

- **Deployment branches**: `develop`

### Step 6: Configure Secrets & Variables

Navigate to **Settings** → **Secrets and variables** → **Actions**

**Secrets** (if applicable):
```
DEPLOY_KEY = [GitHub Pages deploy key]
GITHUB_TOKEN = [automatically provided]
```

**Variables** (for workflows):
```
BUILD_OUTPUT_DIR = build/
PYTHON_VERSION = 3.10
NODE_VERSION = 18
```

## Part 2: CI/CD Pipeline Configuration

### Existing Workflows

The project includes three GitHub Actions workflows:

#### 1. Build & Validate (`build.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`

**Jobs:**
- Build Docusaurus (Node matrix: 18.x, 20.x)
- Markdown linting
- Link checking
- Python/YAML syntax validation
- Spell checking
- Accessibility (Lighthouse)
- Security scanning
- Documentation coverage

**Status Check**: `Build & Validate`

#### 2. Cross-Platform Testing (`cross-platform-test.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Daily schedule (0 2 * * *)

**Matrix:**
- OS: Ubuntu latest, Windows latest, macOS latest
- Python: 3.10, 3.11
- Node: 18, 20

**Tests:**
- Environment verification
- Build output verification
- Python syntax checking
- YAML validation
- Documentation structure validation
- Platform compatibility report

**Status Check**: `Cross-Platform Test`

#### 3. Deploy (`deploy.yml`)

**Triggers:**
- Push to `main` only
- Only on changes to:
  - `docs/**`
  - `sidebars.js`
  - `docusaurus.config.js`
  - `static/**`
  - `.github/workflows/deploy.yml`
  - `package.json`

**Jobs:**
- Build Docusaurus
- Upload artifacts to GitHub Pages
- Deploy to GitHub Pages
- Notification (success/failure)

### Adding Custom Workflows

To add additional workflows, create `.github/workflows/my-workflow.yml`:

```yaml
name: My Custom Workflow

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo "Running custom workflow"
```

## Part 3: Collaboration Settings

### Team Members & Permissions

Navigate to **Settings** → **Manage access**

**Role Levels:**
- **Owner**: Full administrative access
- **Maintain**: Can manage repo without access to sensitive actions
- **Triage**: Can manage issues/PRs
- **Push**: Can pull and push to repo
- **Pull**: Can pull repo only

### Suggested Team Structure

```
Owners (1-2)
├─ Project Lead
├─ Co-Lead (optional)

Maintainers (2-3)
├─ Chapter Writers
├─ Code Reviewers
└─ CI/CD Maintenance

Contributors (Open)
├─ Chapter Contributors
├─ Example Writers
└─ Community Members
```

### Adding Members

```bash
# Via GitHub CLI
gh repo add-collaborator --permission push USERNAME
gh repo add-collaborator --permission maintain USERNAME
```

### Create a CODE_OF_CONDUCT.md

```markdown
# Contributor Covenant Code of Conduct

This project is committed to providing a welcoming and inspiring community.
Please see [Contributor Covenant](https://www.contributor-covenant.org/) for full text.
```

## Part 4: Repository Policies

### SECURITY.md

Create `.github/SECURITY.md`:

```markdown
# Security Policy

## Reporting a Vulnerability

Do not open public issues for security vulnerabilities.
Email: security@physical-ai-lab.org

Please provide:
- Description of vulnerability
- Affected versions
- Reproduction steps
- Suggested fix (if any)

We will acknowledge receipt within 48 hours.
```

### Contributing Guidelines

Update `CONTRIBUTING.md` with:

```markdown
# Contributing Guidelines

## Getting Started
1. Fork the repository
2. Create a branch: `git checkout -b feature/description`
3. Make changes
4. Submit a pull request

## Pull Request Process
- Link to related issues
- Update documentation
- Ensure CI/CD passes
- Request review from maintainers
- Address feedback
- Squash commits if needed
```

### PULL_REQUEST_TEMPLATE.md

Create `.github/pull_request_template.md`:

```markdown
## Description
Brief description of changes

## Related Issues
Closes #[issue number]

## Type of Change
- [ ] New chapter
- [ ] Code example addition
- [ ] Bug fix
- [ ] Documentation update
- [ ] Other (describe):

## Testing
- [ ] Verified on Ubuntu 22.04
- [ ] Verified on Windows 10/11
- [ ] Verified on macOS 12+

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No new warnings generated
```

## Part 5: Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```yaml
---
name: Bug Report
about: Report a bug to help us improve
title: "[BUG] "
labels: bug
---

## Description
Clear description of the bug

## Environment
- OS: [Ubuntu 22.04 / Windows / macOS]
- Python: [version]
- ROS 2: [version]

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected vs Actual
Expected: ...
Actual: ...

## Error Message
```
[Paste full error message]
```

## Additional Context
[Any other information]
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```yaml
---
name: Feature Request
about: Suggest a feature
title: "[FEATURE] "
labels: enhancement
---

## Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
Your suggested implementation

## Alternatives
Other approaches considered
```

## Part 6: Status Checks & Badges

### Required Status Checks

In branch protection rules, ensure these checks are required:

1. **Build & Validate** - Main build and quality checks
2. **Cross-Platform Test** - Compatibility across all platforms
3. **Code Review** - At least 1 approval

### Add Status Badges to README.md

```markdown
# Physical AI & Humanoid Robotics

[![Build & Validate](https://github.com/physical-ai-lab/ai-humanoid-robotics/workflows/Build%20%26%20Validate/badge.svg)](https://github.com/physical-ai-lab/ai-humanoid-robotics/actions)
[![Cross-Platform Testing](https://github.com/physical-ai-lab/ai-humanoid-robotics/workflows/Cross-Platform%20Testing/badge.svg)](https://github.com/physical-ai-lab/ai-humanoid-robotics/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)
![ROS 2 Humble](https://img.shields.io/badge/ROS2-Humble-green)
![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-22.04-orange)
```

## Part 7: Automation Configuration

### Branch Management

Enable **Manage access** → **Branch settings**:
- ✅ Automatically delete head branches
- ✅ Require PR reviews before delete

### Auto-merge Configuration

For develop branch PRs (optional):
```bash
gh pr merge --auto --squash --delete-branch
```

### Actions Permissions

Navigate to **Settings** → **Actions** → **General**

- **Actions permissions**: Allow all actions and reusable workflows
- **Fork pull request workflows**:
  - ✅ Run workflows from fork pull requests
  - **Approve all outside collaborators**: Yes (if allowing contributions)

## Part 8: Monitoring & Analytics

### Enable Repository Insights

Access **Insights** tab for:
- Commit frequency
- Code frequency
- Contributors
- Community profile
- Network graph

### Create GitHub Project (optional)

1. Go to **Projects**
2. Create new project: "Textbook Development"
3. Add columns: Backlog, In Progress, In Review, Done
4. Link issues and PRs

## Part 9: Deployment Configuration

### GitHub Pages Setup

Already configured by `deploy.yml` workflow. Verify:

1. Go to **Settings** → **Pages**
2. Confirm:
   - Source: Deploy from a branch (or GitHub Actions)
   - Branch: gh-pages
   - Custom domain: (optional)
   - HTTPS: ✅ (enforced)

3. Custom domain (optional):
   - Create CNAME file in repository
   - Update DNS records
   - Enable automatic HTTPS

### Domain Configuration (Optional)

```bash
# Create CNAME file
echo "yourdomain.com" > static/CNAME
git add static/CNAME
git commit -m "Add custom domain"
git push
```

## Part 10: Verification Checklist

### Core Configuration
- [ ] Repository created and visible
- [ ] Description and topics set correctly
- [ ] Default branch set to `main`
- [ ] Issues enabled
- [ ] Discussions enabled (recommended)
- [ ] Wiki disabled (if using main docs)

### Branch Protection
- [ ] Main branch protection rule created
- [ ] PR requirement: 1 approval minimum
- [ ] Status checks required
- [ ] Administrators included in restrictions
- [ ] Force push disabled

### CI/CD Pipelines
- [ ] `build.yml` workflow created
- [ ] `deploy.yml` workflow created
- [ ] `cross-platform-test.yml` workflow created
- [ ] Workflows passing on main
- [ ] Deployment working (GitHub Pages live)

### Documentation
- [ ] README.md complete
- [ ] CONTRIBUTING.md created
- [ ] .github/SECURITY.md created
- [ ] Issue templates created
- [ ] PR template created
- [ ] CODE_OF_CONDUCT.md created

### Companion Repository
- [ ] Companion repo created (if needed)
- [ ] Linked from main README
- [ ] Same protection rules applied
- [ ] Structure organized by chapters

## Part 11: Maintenance

### Regular Tasks

**Weekly:**
- Review open PRs and issues
- Monitor CI/CD status
- Address failing checks

**Monthly:**
- Analyze commit statistics
- Review community contributions
- Update dependencies
- Verify all chapters up-to-date

**Quarterly:**
- Major version updates if needed
- Security audit
- Performance review
- Update documentation

### GitHub Maintenance Commands

```bash
# Fetch all updates
git fetch --all --prune

# Check branch status
git branch -v

# List stale branches
git branch --merged main

# Clean up local branches
git branch -d branch-name
```

## Useful GitHub CLI Commands

```bash
# View repository status
gh repo view

# List PRs
gh pr list

# List issues
gh issue list

# Create issue
gh issue create --title "Title" --body "Description"

# View workflows
gh run list

# Trigger workflow
gh workflow run build.yml
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Documentation](https://cli.github.com/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Workflow Security Best Practices](https://docs.github.com/en/actions/security-guides)

---

**Implementation Status**: Complete
**Last Updated**: 2025-12-16
**Maintained By**: Physical AI Lab

## Quick Reference URLs

- **Main Repo Settings**: `https://github.com/physical-ai-lab/ai-humanoid-robotics/settings`
- **Branch Protection**: `https://github.com/physical-ai-lab/ai-humanoid-robotics/settings/branches`
- **Actions**: `https://github.com/physical-ai-lab/ai-humanoid-robotics/actions`
- **Pages**: `https://github.com/physical-ai-lab/ai-humanoid-robotics/settings/pages`
- **Environments**: `https://github.com/physical-ai-lab/ai-humanoid-robotics/settings/environments`
