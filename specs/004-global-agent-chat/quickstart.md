# Quickstart: Global Agent-Only Chat

## Overview
This guide explains how to implement a global chatbot UI that appears on every page of your Docusaurus textbook site, using only agent-enhanced functionality.

## Prerequisites
- Working Docusaurus v3.x installation
- Existing backend with `/agent-query` endpoint
- Node.js and npm installed

## Implementation Steps

### 1. Create the Global Chat Component
Create a React component that will be displayed globally on all pages:
- Location: `src/components/GlobalChat/GlobalChat.jsx`
- Include UI elements for message display, input field, and send button
- Implement API communication with `/agent-query` endpoint
- Add state management for messages, loading states, and errors

### 2. Add Component Styling
Create CSS module for the component:
- Location: `src/components/GlobalChat/GlobalChat.module.css`
- Use fixed positioning (e.g., bottom-right corner)
- Ensure responsive design for mobile and desktop
- Match styling with Docusaurus theme

### 3. Create API Service
Create a service module for API communication:
- Location: `src/components/GlobalChat/ChatService.js`
- Implement function to call `/agent-query` endpoint
- Handle request/response formatting
- Include error handling

### 4. Integrate with Docusaurus Root
Modify the Root component to include the global chat:
- Location: `src/theme/Root.js` (or create if doesn't exist)
- Import and render the GlobalChat component
- This ensures the chat appears on all pages

### 5. Update Configuration
Update docusaurus.config.js if needed:
- Add any necessary configuration for the new component
- Ensure no conflicts with existing features

## Testing
1. Start local development server: `npm run start`
2. Navigate to any page in the textbook
3. Verify the chat UI appears consistently
4. Test sending messages and receiving responses
5. Verify only `/agent-query` endpoint is called
6. Test on different screen sizes

## Deployment
The component will be automatically included when building the site:
- Run `npm run build` to create production build
- Deploy the build folder to your hosting service
- The global chat will be available on all pages