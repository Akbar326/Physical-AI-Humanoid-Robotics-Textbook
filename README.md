# Physical AI & Humanoid Robotics Textbook

A comprehensive, beginner-friendly, project-based guide to robotics, AI, and humanoid systems. This textbook provides 100+ hours of content covering ROS 2, simulation, AI integration, and Vision-Language-Action systems.

## 📚 Overview

This textbook is designed to take you from complete beginner to building autonomous robot systems that understand natural language commands and execute complex tasks. The content is organized into four progressive modules:

- **Module 1: ROS 2 Fundamentals** - Master the Robot Operating System with hands-on exercises
- **Module 2: Simulation** - Create physics-based simulations and high-fidelity visualizations
- **Module 3: AI/Isaac Integration** - Train autonomous robot behaviors using reinforcement learning
- **Module 4: Vision-Language-Action Models** - Integrate vision, language, and action into unified systems

## 🎯 Features

- **Complete Curriculum**: 4 modules with 23 chapters covering the entire robotics pipeline
- **Hands-On Learning**: Practical exercises with expected outputs and troubleshooting guides
- **Cross-Platform Support**: Ubuntu, Windows, and macOS instructions for every concept
- **ROS 2 Foundation**: Built on the latest ROS 2 Humble Hawksbill distribution
- **Simulation First**: Gazebo and Unity simulation environments for safe learning
- **AI Integration**: NVIDIA Isaac Sim for reinforcement learning and autonomous behaviors
- **VLA Systems**: Vision-Language-Action models for natural language robot interaction
- **Interactive Book Queries**: Ask questions about book content using AI-powered RAG system

## 🛠️ Tech Stack

- **ROS 2**: Robot Operating System (Humble Hawksbill)
- **Gazebo**: Physics simulation engine (Fortress)
- **Unity**: High-fidelity visualization (2022 LTS)
- **NVIDIA Isaac Sim**: AI-ready robotics simulation
- **Python 3.10+**: Primary programming language
- **Docusaurus**: Static site generation for textbook
- **JavaScript/React**: Interactive textbook interface
- **FastAPI**: Backend API for RAG queries
- **Qdrant**: Vector database for document retrieval

## 🚀 Installation

### Prerequisites
- Basic Python programming knowledge
- Command-line familiarity
- Ubuntu 22.04, Windows 10/11, or macOS 12+
- For Modules 3-4: NVIDIA GPU recommended (GTX 1060+ or RTX 3060+)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-github-username/physical-ai-robotics-textbook.git
cd physical-ai-robotics-textbook

# Install dependencies
npm install

# Start the development server
npm start
```

The textbook will be available at `http://localhost:3000/physical-ai-robotics-textbook/`

## 🤖 Frontend-Backend Integration

The project includes an advanced frontend-backend integration that allows users to query book content using AI. Here's how to set it up:

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables (OpenAI API key, Qdrant connection, etc.)

4. Start the backend server:
   ```bash
   python run_server.py
   ```
   The backend should be accessible at `http://localhost:8000`.

### Frontend Integration
The frontend includes several components for RAG (Retrieval-Augmented Generation) queries:

- **RagQueryContext**: Main component providing context and state management
- **RagQueryForm**: Form for submitting queries about book content
- **RagQueryResult**: Component for displaying API responses
- **LoadingIndicator**: Shows loading states during API requests
- **Text Selection Utility**: Captures selected text for context-aware queries

### Adding Query Functionality to Pages
To add the query functionality to any Docusaurus page, simply import and include the RagQueryContext component:

```jsx
import RagQueryContext from '@site/src/components/RagQuery/RagQueryContext';

function MyBookPage() {
  return (
    <div>
      <h1>My Book Page</h1>
      <p>Page content here...</p>
      <RagQueryContext />
    </div>
  );
}
```

### Using the JavaScript Integration
For non-React pages, you can use the direct script integration:

1. Include the script in your HTML:
   ```html
   <script src="static/js/rag-integration.js"></script>
   ```

2. Add a container to your HTML:
   ```html
   <div id="rag-query-container" data-rag-integration
        data-base-url="http://localhost:8000"
        data-max-results="5"
        data-include-citations="true">
   </div>
   ```

### Features
- **Natural Language Queries**: Ask questions about book content in plain English
- **Context-Aware Queries**: Select text and ask questions about the specific content
- **Citations**: Responses include source citations for fact-checking
- **Error Handling**: Graceful handling of network errors, timeouts, and API failures
- **Query History**: Previous queries are stored in browser's localStorage
- **Responsive Design**: Works on desktop and mobile devices

## 📖 Learning Paths

**Path 1: ROS 2 Foundations** (Beginner)
- Modules 1 → Stop
- Time: 18-21 hours
- Goal: Master ROS 2 basics

**Path 2: Simulation Developer** (Intermediate)
- Modules 1 → 2 → Stop
- Time: 38-45 hours
- Goal: Build and visualize simulated robots

**Path 3: AI for Robotics** (Advanced)
- Modules 1 → 2 → 3 → Stop
- Time: 57-68 hours
- Goal: Train autonomous robot behaviors

**Path 4: Complete Physical AI** (Expert)
- Modules 1 → 2 → 3 → 4 → Capstone
- Time: 85-107 hours
- Goal: End-to-end VLA systems

## 🎓 Learning Outcomes

After completing this textbook, you will be able to:

### Module 1 (ROS 2)
- Create distributed robot systems using ROS 2
- Build custom nodes and manage communication
- Use services and actions for complex workflows
- Orchestrate multi-node systems with launch files

### Module 2 (Simulation)
- Design and build robot models (URDF)
- Create physics-based simulations in Gazebo
- Add sensors and process data in real-time
- Visualize robots in Unity with high fidelity

### Module 3 (AI/Isaac)
- Train reinforcement learning policies
- Use Isaac Sim for AI-ready environments
- Scale training across multiple parallel environments
- Deploy trained models to ROS 2 systems

### Module 4 (VLA)
- Integrate vision, language, and action systems
- Process natural language commands
- Execute task planning and motion control
- Build end-to-end autonomous robot systems

## 🤖 Capstone Project

After completing all 4 modules, you'll build a real-world robotics system: "Kitchen Robot - Natural Language Task Executor" that can see, listen, think, and act to execute natural language commands in simulation.

## 📁 Companion Repository

All code examples, robot models, exercises, and solutions are available in the [physical-ai-textbook-assets](https://github.com/your-github-username/physical-ai-textbook-assets) companion repository.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information on how to get involved.

## 📄 License

This textbook is completely free and open-source. See the LICENSE file for details.

## 📞 Support

- **Documentation**: Browse the textbook at the live site
- **Issues**: Report problems on [GitHub Issues](https://github.com/your-github-username/physical-ai-robotics-textbook/issues)
- **Community**: Join discussions in the GitHub repository

---

Made with ❤️ for robotics enthusiasts everywhere