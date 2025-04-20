# Email Classification System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📋 Table of Contents
- [Email Classification System](#email-classification-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [🔍 Project Description](#-project-description)
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
    - [Included Features](#included-features)
    - [Excluded Features](#excluded-features)
  - [📊 Project Status](#-project-status)
  - [📄 License](#-license)

## 🔍 Project Description
The Email Classification System is designed primarily for law firms to streamline the process of organizing and classifying email attachments. The system allows users to submit each email in EML format, automatically extracting metadata such as sender, recipient, date, and subject. Attachments (supported formats: pdf, docs, tiff, jpg) are automatically classified into predefined categories to facilitate rapid document retrieval and improved efficiency. The system ensures GDPR compliance with data encryption both in transit and at rest.

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
- Node.js (as specified in the .nvmrc file)
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Setup the Python backend:
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. Setup the frontend:
   - Ensure your Node.js version matches the one specified in the `.nvmrc` file.
   - Install frontend dependencies:
     ```bash
     npm install
     ```

### Running the Application
Start the FastAPI backend server with automatic reload:
```bash
uvicorn src.api.main:app --reload
```

## 📝 Available Scripts

### Running Tests
- Run all tests:
  ```bash
  pytest
  ```
- Watch tests (automatically run tests on file changes):
  ```bash
  ptw
  ```

### Linting
- Check code for linting issues:
  ```bash
  ruff check .
  ```
- Auto-fix linting issues where possible:
  ```bash
  ruff check --fix .
  ```

### Formatting
- Format the code:
  ```bash
  ruff format .
  ```
- Check formatting without modifying files:
  ```bash
  ruff format . --check
  ```

## 🔭 Project Scope

### Included Features
- Secure user authentication
- Email submission in EML format with attachment support
- Automatic extraction of email metadata (sender, recipient, date, subject)
- Automatic classification of attachments using predefined categories
- Data storage and organization of emails and attachments
- Filtering and sorting functionality for fetched records
- Attachment download functionality

### Excluded Features
- Comprehensive user account management (e.g., password reset, profile editing)
- Support for email formats other than EML
- Classification of the email body content (focus is on attachments)
- Mass parallel processing (current performance benchmark: 1 attachment per second)
- Mobile application support

## 📊 Project Status
The project is currently in the MVP (Minimum Viable Product) stage, with the following goals:
- Achieve at least 90% accuracy in attachment classification
- Ensure full GDPR compliance with encryption for data in transit and at rest
- Maintain a processing rate of 1 attachment per second

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.