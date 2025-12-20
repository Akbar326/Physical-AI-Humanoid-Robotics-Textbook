# Quickstart: Docusaurus Documentation Setup

## Prerequisites
- Node.js version >=18.0.0
- npm package manager

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start local development server**
   ```bash
   npm run start
   ```
   This will start the development server at http://localhost:3000

4. **Build for production**
   ```bash
   npm run build
   ```
   This will generate the static site in the `build/` directory

## Troubleshooting

### Common Issues

1. **Missing module errors**: Run `npm install` to ensure all dependencies are installed
2. **Port already in use**: The development server will automatically use a different port if 3000 is taken
3. **Build failures**: Check for syntax errors in documentation files and configuration

### Dependency Issues

If you encounter dependency errors:

1. Clear npm cache:
   ```bash
   npm cache clean --force
   ```

2. Remove node_modules and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## Vercel Deployment

The project is configured for Vercel deployment. When pushing to a Git repository connected to Vercel:

1. Vercel will automatically detect the Docusaurus project
2. It will run `npm run build` during the build process
3. The output from the `build` directory will be served

### Vercel Configuration (if needed)
The project should work with Vercel's default Node.js configuration, but if specific settings are needed:

- Build Command: `npm run build`
- Output Directory: `build`
- Node Version: >=18.0.0 (as specified in package.json engines)