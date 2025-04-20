# Email Classification System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📋 Table of Contents
- [Email Classification System](#email-classification-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔍 Project Description](#-project-description)
    - [Key Features](#key-features)
  - [💻 Tech Stack](#-tech-stack)
    - [Frontend](#frontend)
    - [Backend](#backend)
    - [CI/CD](#cicd)
  - [🚀 Getting Started Locally](#-getting-started-locally)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
  - [📝 Available Scripts](#-available-scripts)
    - [Running Tests](#running-tests)
    - [Linting](#linting)
    - [Formatting](#formatting)
  - [🔭 Project Scope](#-project-scope)
    - [Included](#included)
    - [Not Included](#not-included)
  - [📊 Project Status](#-project-status)
  - [📄 License](#-license)

## 🔍 Project Description
The Email Classification System is designed primarily for law firms to organize and classify email attachments efficiently. The system allows users to submit emails in EML format, automatically extracts metadata, and classifies attachments based on predefined categories. This automation significantly reduces the time spent manually searching and organizing documents, improving overall efficiency.

### Key Features
- Secure user authentication
- Email submission with attachment support (pdf, docs, tiff, jpg)
- Automatic metadata extraction (sender, recipient, date, subject)
- Attachment classification using predefined categories
- Filtering and sorting capabilities
- GDPR compliance with encryption in transit and at rest

## 💻 Tech Stack

### Frontend
- Astro 5
- React 19
- Tailwind 4
- shadcn/ui

### Backend
- Python (FastAPI)
- Azure Container App
- Azure Database for PostgreSQL – Flexible Server
- Azure Entra ID
- Azure Blob Storage
- Azure OpenAI Endpoint (for LLM)

### CI/CD
- Azure Pipelines

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone the repository
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the FastAPI server with hot-reload:
```bash
uvicorn src.api.main:app --reload
```

## 📝 Available Scripts

### Running Tests
Execute all tests:
```bash
pytest
```

Watch tests (automatically run tests when files change):
```bash
ptw
```

### Linting
Check your code:
```bash
ruff check .
```

Auto-fix issues when possible:
```bash
ruff check --fix .
```

### Formatting
Format your code:
```bash
ruff format .
```

Check formatting issues without making changes:
```bash
ruff format . --check
```

## 🔭 Project Scope

### Included
- Secure user authentication
- Email submission in EML format
- Metadata extraction
- Attachment classification
- Data storage
- Results viewing with filtering and sorting
- Attachment download

### Not Included
- Comprehensive user account management
- Support for non-EML email formats
- Classification of email content (focus is on attachments only)
- Mass parallel processing (initial performance: 1 attachment per second)
- Mobile version

## 📊 Project Status
The project is currently in MVP (Minimum Viable Product) phase, focusing on achieving:
- At least 90% accuracy in attachment classification
- Full GDPR compliance
- Processing rate of 1 attachment per second

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.