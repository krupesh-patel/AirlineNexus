# 🤝 Contributing to AirlineNexus

Thank you for your interest in contributing to **AirlineNexus**! We welcome contributions from developers of all skill levels. This guide will help you get started and ensure your contributions align with our project standards.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful** and inclusive in all communications
- **Be collaborative** and help others learn and grow
- **Be patient** with newcomers and different skill levels
- **Focus on constructive feedback** and solutions
- **Respect different perspectives** and experiences

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **Git** for version control
- **Virtual environment** management (venv, conda, etc.)
- **Basic understanding** of AI/ML concepts (helpful but not required)

### First-Time Contributors

1. **🍴 Fork the repository** on GitHub
2. **⭐ Star the project** if you find it interesting
3. **👀 Browse existing issues** to find something to work on
4. **💬 Join discussions** in issues and pull requests
5. **📚 Read the documentation** to understand the project structure

## 💻 Development Setup

### 1. Clone Your Fork

```bash
git clone https://github.com/your-username/AirlineNexus.git
cd AirlineNexus
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit with your configurations
# Required variables:
MOONSHOT_API_KEY=your_api_key
MCP_SERVER_URL=http://localhost:8000/mcp
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_username
TIDB_PASSWORD=your_password
TIDB_DATABASE=airline_nexus
```

### 4. Initialize Database

```bash
python db_creation.py
```

### 5. Verify Setup

```bash
# Test CLI interface
python airline_nexus.py

# Test web interface
python run_ui.py
```

### 6. Set Up Pre-commit Hooks (Optional but Recommended)

```bash
pip install pre-commit
pre-commit install
```

## 🛠️ How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 **Bug Fixes**
- Fix existing issues
- Improve error handling
- Resolve performance problems

#### ✨ **New Features**
- Add new agent capabilities
- Integrate additional AI models
- Enhance UI/UX components

#### 📚 **Documentation**
- Improve README and guides
- Add code comments
- Create tutorials and examples

#### 🎨 **UI/UX Improvements**
- Enhance Streamlit interface
- Improve responsive design
- Add new visualizations

#### ⚡ **Performance Optimization**
- Optimize agent response times
- Improve database queries
- Enhance memory usage

### Finding Issues to Work On

- **Good First Issue**: Perfect for newcomers
- **Help Wanted**: Issues where we need community help
- **Bug**: Confirmed bugs that need fixing
- **Enhancement**: New features or improvements
- **Documentation**: Documentation improvements needed

## 📤 Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- **Follow coding standards** (see below)
- **Write clear commit messages**
- **Add tests** for new functionality
- **Update documentation** as needed

### 3. Test Your Changes

```bash
# Test the full application
python run_ui.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add flight booking validation

- Implement booking form validation
- Add error handling for invalid dates
- Update UI feedback messages

Closes #123"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- **Clear title** describing the change
- **Detailed description** of what you've done
- **Reference to related issues** (e.g., "Closes #123")
- **Screenshots** for UI changes
- **Testing information** about how you verified the changes

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have tested these changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Related Issues
Closes #(issue number)
```

## 📝 Coding Standards

### Python Code Style

- **Follow PEP 8** style guidelines
- **Use type hints** where appropriate
- **Write docstrings** for functions and classes
- **Use meaningful variable names**
- **Keep functions focused** and single-purpose

#### Example:

```python
def search_flights(
    departure_airport: str,
    arrival_airport: str,
    departure_date: str,
    passengers: int = 1
) -> Dict[str, Any]:
    """
    Search for available flights based on criteria.
    
    Args:
        departure_airport: Airport code (e.g., 'JFK')
        arrival_airport: Airport code (e.g., 'LAX')
        departure_date: Date in YYYY-MM-DD format
        passengers: Number of passengers
        
    Returns:
        Dictionary containing flight search results
        
    Raises:
        ValueError: If invalid airport codes or dates provided
    """
    # Implementation here
    pass
```

### Code Organization

```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Third-party imports
import streamlit as st
from strands import Agent, tool

# Local imports
from multi_agents.flight_agent import flight_agent
from config.database import db_manager
```

### Error Handling

```python
try:
    result = some_operation()
    return {"success": True, "data": result}
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return {"success": False, "error": str(e)}
```

## 📖 Documentation Guidelines

### Code Documentation

- **Add docstrings** to all functions, classes, and modules
- **Use clear, concise language**
- **Include examples** where helpful
- **Document parameters and return values**

### README Updates

When making changes that affect usage:

- Update installation instructions
- Add new configuration options
- Update examples and use cases
- Modify architecture diagrams if needed

### API Documentation

- Document new endpoints or tools
- Include request/response examples
- Explain error codes and handling
- Update the API reference in `docs/api_reference.md`

## 🐛 Issue Guidelines

### Reporting Bugs

When reporting bugs, please include:

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. macOS, Windows, Linux]
 - Python Version: [e.g. 3.13.1]
 - Browser: [e.g. chrome, safari]
 - AirlineNexus Version: [e.g. 1.0.0]

**Additional Context**
Add any other context about the problem here.
```

### Feature Requests

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 💬 Community

### Getting Help

- **GitHub Discussions**: For general questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **Pull Request Comments**: For code-specific discussions

### Communication Guidelines

- **Be specific** in your questions and descriptions
- **Provide context** about your setup and what you're trying to achieve
- **Search existing issues** before creating new ones
- **Use clear titles** that summarize the issue or question

## 🏷️ Labels and Milestones

### Issue Labels

- `help wanted` - Community help needed
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `question` - Further information is requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue or pull request already exists

### Priority Labels

- `priority: low` - Low priority
- `priority: medium` - Medium priority
- `priority: high` - High priority
- `priority: critical` - Critical issue

### Component Labels

- `component: agents` - Multi-agent system
- `component: ui` - User interface
- `component: database` - Database related
- `component: api` - API related
- `component: docs` - Documentation

## 🎉 Recognition

Contributors are recognized in:

- **README.md** contributors section
- **GitHub contributors** page
- **Release notes** for significant contributions
- **Special mentions** in project updates

## ❓ Questions?

If you have any questions about contributing, please:

1. Check this contributing guide
2. Search existing GitHub issues
3. Create a new discussion in GitHub Discussions
4. Reach out to maintainers in existing issues

Thank you for contributing to AirlineNexus! Together, we're building the future of airline customer service. ✈️

---

<div align="center">

**Happy Contributing! 🚀**

[Report Bug](https://github.com/krupesh-patel/AirlineNexus/issues/new?assignees=&labels=bug&template=bug_report.md) • [Request Feature](https://github.com/krupesh-patel/AirlineNexus/issues/new?assignees=&labels=enhancement&template=feature_request.md) • [Join Discussion](https://github.com/krupesh-patel/AirlineNexus/discussions)

</div>