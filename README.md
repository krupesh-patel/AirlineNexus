<div align="center">

# ✈️ AirlineNexus
#### Aviation intelligence. The secret to seamless travel.

*Multi-Agent AI Airline Assistant*


[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![TiDB](https://img.shields.io/badge/TiDB-Vector_DB-orange?logo=databricks&logoColor=white)](https://tidb.cloud)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🏗️ Architecture](#️-architecture) • [🤝 Contributing](#-contributing)

---

</div>

## 🌟 Overview

**AirlineNexus** is an intelligent, multi-agent AI system designed to revolutionize airline customer service through specialized AI agents that handle different aspects of travel assistance - from flight booking to policy queries and support tickets.

Our system employs a sophisticated multi-agent architecture where different AI specialists collaborate to provide comprehensive airline assistance. Each agent is expertly trained for specific domains, ensuring accurate and contextual responses for every customer interaction.

### ✨ Key Features

| Feature | Description | Technology |
|---------|-------------|------------|
| 🤖 **Multi-Agent Architecture** | Specialized agents for different domains | Strands Agents Framework |
| 🛫 **Flight Operations** | Complete flight search, booking, and management | MCP Server + FastAPI |
| 📋 **Policy Intelligence** | AI-powered policy queries with vector search | TiDB Vector + Embeddings |
| 🎧 **Smart Support** | Automated ticket creation and issue resolution | Python Tools + Email Integration |
| 💬 **Natural Conversations** | Seamless handoffs between specialized agents | Moonshot AI + Kiwi LLM |
| 🖥️ **Modern UI** | Beautiful Streamlit web interface | Streamlit + Custom CSS |
| ⚡ **Real-time Processing** | Live status updates and processing indicators | WebSocket + Async Processing |

### 🧠 Agent Specifications

<details>
<summary><strong>🎯 Coordinator Agent</strong></summary>

**Role:** Central orchestrator and traffic controller

**Responsibilities:**
- Intent classification and routing
- Multi-step workflow coordination  
- Context preservation across agents
- Response synthesis and quality assurance

**Technology:** Strands Framework
</details>

<details>
<summary><strong>🛫 Flight Agent</strong></summary>

**Powered by:** MCP (Model Context Protocol) Server

**Capabilities:**
- Real-time flight search across multiple airlines
- Booking creation and management
- Flight status monitoring
- Schedule modifications

</details>

<details>
<summary><strong>📋 Policy Agent</strong></summary>

**Powered by:** TiDB Serverless Vector Database

**Capabilities:**
- Semantic policy search using embeddings
- Contextual rule interpretation
- Regulation compliance checking

</details>

<details>
<summary><strong>🎧 Support Agent</strong></summary>

**Powered by:** Custom Python Tools

**Capabilities:**
- Automated ticket creation
- Issue complexity analysis
- Priority assignment
- Escalation management

</details>

<details>
<summary><strong>💬 General Agent</strong></summary>

**Role:** Fallback handler for miscellaneous queries

**Capabilities:**
- General travel information
- Conversational assistance
- Context-aware responses

</details>

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **pip** (Python package installer)

### 📥 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/krupesh-patel/AirlineNexus.git
   cd AirlineNexus
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your configurations
   vi .env
   ```
   
   Required environment variables:
   ```env
   MOONSHOT_API_KEY=your_moonshot_api_key
   MCP_SERVER_URL=http://localhost:8000/mcp
   TIDB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
   TIDB_PORT=4000
   TIDB_USER=your_username
   TIDB_PASSWORD=your_password
   TIDB_DATABASE=airline_nexus
   ```

5. **Initialize Database**
   ```bash
   python db_creation.py
   ```

### 🖥️ Running the Application

### If you want to run the demo MCP server:
   ```bash
   python -m mcp_server.flight_tools
   ````

Choose your preferred interface:

#### Option 1: Web UI (Recommended)
```bash
python run_ui.py
```
or
```bash
streamlit run streamlit_app.py --server.port 8501
```

#### Option 2: Command Line Interface
```bash
python airline_nexus.py
```

### 🌐 Access Points

- **Web Interface:** http://localhost:8501
- **MCP Server:** http://localhost:8000/mcp (if running separately)

## 📁 Project Structure

```
AirlineNexus/
├── 📄 README.md                 # Project documentation
├── 📄 requirements.txt          # Python dependencies
├── 📄 airline_nexus.py         # Main CLI application
├── 📄 streamlit_app.py         # Web UI application
├── 📄 run_ui.py               # Launch script
├── 📄 db_creation.py          # Database initialization
├── 
├── 📂 multi_agents/            # Agent implementations
│   ├── flight_agent.py        # Flight operations agent
│   ├── policy_agent.py        # Policy & rules agent
│   ├── support_agent.py       # Customer support agent
│   └── general_agent.py       # General purpose agent
├── 
├── 📂 prompts/                 # Agent system prompts
│   ├── coordinator_prompt.py  # Main coordinator instructions
│   ├── flight_prompt.py       # Flight agent prompts
│   ├── policy_prompt.py       # Policy agent prompts
│   └── support_prompt.py      # Support agent prompts
├── 
├── 📂 mcp_server/              # MCP server implementation
│   └── flight_tools.py        # Flight API tools
├── 
├── 📂 config/                  # Configuration files
│   ├── database.py            # Database connections
│   └── __init__.py
├── 
├── 📂 model/                   # AI model integrations
│   └── moonshot.py            # Moonshot AI client
├── 
├── 📂 utils/                   # Utility functions
│   ├── embeddings.py          # Vector embeddings
│   └── __init__.py
└── 
└── 📂 docs/                    # Additional documentation
    ├── architecture_diagram.md # Detailed architecture
    ├── api_reference.md        # API documentation
    └── deployment.md           # Deployment guide
```

## 🛠️ Technology Stack

<div align="center">

### Core Technologies
| Category            | Technology                   | Purpose |
|---------------------|------------------------------|---------|
| **Language**        | Python 3.13+                 | Primary development language |
| **Web Framework**   | Streamlit                    | Interactive web interface |
| **Agent Framework** | AWS Strands Agents           | Multi-agent orchestration |
| **LLM Tools**       | MCP (Model Context Protocol) | Tool integration |
| **Database**        | TiDB Serverless              | Vector database for embeddings |

### AI & ML Stack
| Component | Technology | Use Case                   |
|-----------|------------|----------------------------|
| **Domain LLM** | Kiwi LLM | Think, Act, React          |
| **Embeddings** | Sentence Transformers | Text embeddings for search |
| **Vector Search** | TiDB Vector | Semantic policy search     |

</div>

## 🎯 Use Cases & Examples

### 🛫 Flight Management
```
👤 User: "I want to book a business class flight for 2 people from London to Toronto on September 25, 2025"

🎯 System Process:
├── Routes to Flight Agent
├── Searches available flights with MCP tools
├── Presents flight options
└── Handles booking confirmation

✅ Result: Complete flight booking with confirmation
```

### 📋 Policy Inquiries
```
👤 User: "Can I carry 20kg baggage?"

🎯 System Process:
├── Routes to Policy Agent
├── Searches policy database using vector similarity (TIDB)
├── Retrieves relevant baggage policies
└── Provides contextual answer

✅ Result: Accurate policy information with rules
```

### 🎧 Support Issues
```
👤 User: "I cancelled my flight, but I didn't get a refund"

🎯 System Process:
├── Routes to Support Agent
├── Analyzes issue complexity → HIGH priority
├── Creates support ticket
└── Provides ticket details and timeline

✅ Result: Support ticket created with tracking ID
```

## 🚀 Features in Detail

### 🖥️ Web Interface Features

- **🎨 Modern Design:** Clean, professional airline-themed UI with custom CSS
- **💬 Real-time Chat:** Instant messaging with typing indicators and animations
- **📊 Agent Visibility:** Live display of which agent is processing your request
- **📈 Session Management:** Conversation history, statistics, and session persistence
- **⚡ Quick Actions:** Pre-built example queries for common use cases
- **📱 Responsive Design:** Works seamlessly on desktop, tablet, and mobile

### 🧠 AI Capabilities

- **🎯 Intent Recognition:** Automatically routes queries to the most appropriate agent
- **🔄 Context Awareness:** Maintains conversation context across agent handoffs
- **📝 Multi-modal Responses:** Text, structured data, tables, and actionable insights
- **🛡️ Error Recovery:** Graceful error handling with alternative suggestions
- **📊 Performance Monitoring:** Real-time tracking of response times and success rates

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🔧 Development Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/krupesh-patel/AirlineNexus.git
   cd AirlineNexus
   ```

2. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

### 🐛 Reporting Issues

Use the [GitHub issue tracker](https://github.com/krupesh-patel/AirlineNexus/issues) to report bugs:

- **Bug Reports:** Include detailed reproduction steps, environment details, and expected behavior
- **Feature Requests:** Provide clear description, use cases, and potential implementation approach
- **Questions:** Use GitHub Discussions for general questions and community support

## 📈 Roadmap

### 🎯 Phase 1: Foundation (✅ Complete)
- [x] Multi-agent architecture implementation
- [x] Core flight operations with MCP server
- [x] Policy query system with vector search
- [x] Support ticket automation
- [x] Streamlit web interface
- [x] CLI interface

### 🚧 Phase 2: Enhancement (TO DO)
- [ ] Real airline API integration
- [ ] Payment processing integration (Stripe, PayPal)
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support

### 🔮 Phase 3: Enterprise (Future Goals)
- [ ] Single Sign-On (SSO) integration
- [ ] Advanced analytics dashboard
- [ ] Custom agent training interface
- [ ] Voice interface integration


<div align="center">

| Support Type | Contact Method |
|--------------|----------------|
| 🐛 **Bug Reports** | [GitHub Issues](https://github.com/krupesh-patel/AirlineNexus/issues) |
| 💡 **Feature Requests** | [GitHub Issues](https://github.com/krupesh-patel/AirlineNexus/issues) |
| ❓ **Questions** | [GitHub Discussions](https://github.com/krupesh-patel/AirlineNexus/discussions) |
| 🏢 **Enterprise** | support@airlinenexus.ai |

</div>

## 🙏 Acknowledgments

- **[TiDB](https://www.pingcap.com/tidb-cloud-starter/)** - Serverless vector database infrastructure
- **[Moonshot AI](https://www.moonshot.ai/)** - Advanced language model capabilities
- **[AWS Strands](https://strandsagents.com/latest/)** - Multi-agent orchestration tools
- **[Streamlit](https://streamlit.io/)** - Amazing web application framework
- **[MCP Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)** - Seamless tool integration

---

<div align="center">

### 🚀 Built with ❤️ for the future of travel

**AirlineNexus** - Aviation intelligence. The secret to seamless travel.

[![GitHub stars](https://img.shields.io/github/stars/krupesh-patel/AirlineNexus?style=social)](https://github.com/krupesh-patel/AirlineNexus/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/krupesh-patel/AirlineNexus?style=social)](https://github.com/krupesh-patel/AirlineNexus/network)

[⭐ Star this project](https://github.com/krupesh-patel/AirlineNexus) • [🍴 Fork it](https://github.com/krupesh-patel/AirlineNexus/fork) • [📢 Share it](https://twitter.com/intent/tweet?text=Check%20out%20AirlineNexus%20-%20Multi-Agent%20AI%20Airline%20Assistant!&url=https://github.com/krupesh-patel/AirlineNexus)

</div>