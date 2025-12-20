# Quickstart: Fix Docusaurus Build Issues and Landing Page

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development
1. Start development server:
   ```bash
   npm start
   ```
   The site will be available at `http://localhost:3000/physical-ai-robotics-textbook/`

2. To test the build:
   ```bash
   npm run build
   ```

## Key Files to Modify
- `docusaurus.config.js` - Site configuration
- `src/pages/index.js` - New landing page (to be created)
- `README.md` - Repository documentation (to be created)

## Testing the Changes
1. After making changes, run:
   ```bash
   npm run build
   ```
2. Verify no broken links errors appear
3. Start the built site to verify functionality:
   ```bash
   npx serve -s build
   ```