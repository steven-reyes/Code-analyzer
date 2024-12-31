# Code Analyzer

A local-hosted application designed to **analyze** public/private repositories or local projects, identifying inefficiencies and suggesting optimizations. By leveraging **LLMs** (e.g., ChatGPT-01), it delivers actionable insights into code quality, structure, and scalability.

---

## Features

- **Comprehensive Scanning**: File structure, Docker configs, requirements, ML workflow, security, logging, etc.
- **ChatGPT Integration**: Real-time suggestions or code edits via ChatGPT-01.
- **User-Friendly Interface**: Web UI (Flask or Node) or optional CLI.
- **Reporting**: Generate PDF, Markdown, JSON, or Excel outputs of analysis results.

---

## Installation

### Prerequisites

- Python 3.9+
- Node.js 16+ (optional for front-end tasks)
- Docker & Docker Compose (optional, for containerized deployment)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/steven-reyes/code-analyzer.git
cd code-analyzer
```

### 2. Python Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Optional: Use Conda**:
   ```bash
   conda env create -f environment.yml
   conda activate code-analyzer-env
   ```

### 3. Node.js Setup (Optional)

1. **Install dependencies**:
   ```bash
   npm install
   ```
2. **Build and run tasks**:
   ```bash
   npm run build
   npm run start  # or npm run dev
   ```

### 4. Docker Setup (Optional)

1. **Build Docker image**:
   ```bash
   docker build -t code-analyzer:latest .
   ```
2. **Run using Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   This spins up the web + DB containers (if configured in `docker-compose.yml`).

---

## Quick Start

1. **Run the Application Locally**:

   ```bash
   python src/main.py
   ```

   Visit `http://localhost:5000` in your browser or use the CLI.

2. **Analyze a Local Project**:

   ```bash
   python src/main.py --project-path /path/to/project
   ```

3. **Analyze a GitHub Repo**:

   ```bash
   python src/main.py --github-url https://github.com/username/repo
   ```

---

## Project Structure

```
Code_Analyzer/                                     # Main directory for the entire project
├── .github/                                       # (GitHub-Specific) Contains GitHub Actions workflows, issue templates, etc.
│   ├── ISSUE_TEMPLATE/                            # (Issue Templates) Standardized templates for GitHub Issues
│   └── workflows/
│       └── ci.yml                                 # (CI/CD Workflow) Defines automated tests/builds/deployments
├── .gitignore                                     # (Git Ignore Rules) Lists files/folders to exclude from version control
├── .env                                           # (Environment Variables) Stores sensitive info (e.g., API keys, DB credentials)
├── .env.example                                   # (Sample Environment Variables) Stores sensitive info (e.g., API keys, DB credentials)
├── .dockerignore                                  # (Docker Ignore Rules) Files/folders to exclude from Docker builds
├── .editorconfig                                  # (EditorConfig) Consistent coding style across editors
├── .prettierrc                                    # (Prettier Config) Code formatting rules (JS/TS)
├── .eslintignore                                  # (ESLint Ignore) Excludes certain files/folders from ESLint
├── .eslintrc.js                                   # (ESLint Config) JavaScript/TypeScript linting rules
├── .flake8                                        # (Flake8 Config) Python linting rules (if using Flake8)
├── .pylintrc                                      # (Pylint Config) Python linting rules (if using Pylint)
├── .pre-commit-config.yaml                        # (Pre-Commit Hooks) Defines lint/format checks before commits
├── .pytest_cache/                                 # (Pytest Cache) Auto-generated data for Python tests
├── coverage/                                      # (Coverage Reports) Generated coverage data (HTML, JSON) for tests
│   ├── coverage-final.json                        # (Coverage Data) Machine-readable summary
│   └── index.html                                 # (Coverage HTML Report) Human-readable coverage visualization
├── coverage.xml                                   # (Coverage XML) For CI tools (e.g., Cobertura, SonarQube)
├── Dockerfile                                     # (Docker Build) Instructions to build a Docker image
├── docker-compose.yml                             # (Docker Compose) Multi-container orchestration
├── requirements.txt                               # (Python Dependencies) Pinned Python libraries
├── environment.yml                                # (Conda Env Config) Alternative to requirements.txt for Python deps
├── package.json                                   # (Node.js Config) Name, version, scripts, dependencies
├── package-lock.json                              # (Node.js Lock File) Auto-generated by npm
├── yarn.lock                                      # (Yarn Lock File) Auto-generated if using Yarn
├── LICENSE                                        # (Project License) E.g., MIT, Apache, or Proprietary
├── README.md                                      # (Project Overview / Quick Start)
│                                                  #  - High-level description of the project
│                                                  #  - Summarizes core features or goals
│                                                  #  - Often includes minimal setup instructions for a quick start
├── USER_MANUAL.md                                 # (Detailed User Manual)
│                                                  #  - Step-by-step installation instructions (Python, Node, Docker)
│                                                  #  - How to configure and run on localhost
│                                                  #  - Usage examples and troubleshooting tips
│                                                  #  - Advanced setup or deployment guides
├── CONTRIBUTING.md                                # (Contribution Guidelines) Explains how to contribute
├── SECURITY.md                                    # (Security Policy) Guidance on reporting vulnerabilities
├── CHANGELOG.md                                   # (Release Notes) Records changes across versions
├── setup.py                                       # (Python Packaging) For installing/distributing as a Python package
├── pyproject.toml                                 # (PEP 518) Python build system requirements (poetry, flit, setuptools)
├── node_modules/                                  # (Node.js Dependencies) Auto-generated directory (npm or yarn)
│   └── ...                                        # Contains installed packages
├── data/                                          # (Data Directory) Holds raw and processed datasets
│   ├── raw/
│   │   └── dataset.csv                            # (Raw CSV) Unmodified dataset
│   └── processed/
│       └── processed_dataset.csv                  # (Processed CSV) Cleaned/preprocessed dataset
├── docs/                                          # (Documentation) Architecture guides, user manuals, technical docs
│   ├── architecture.md                            # (System Architecture) Explains high-level design
│   ├── api.md                                     # (API Documentation) Endpoints, request/response formats
│   └── ...
├── ml/                                            # (Machine Learning/AI) Houses ML/AI-specific code and configs
│   ├── config/
│   │   ├── model_config.json                      # (Model Config) Hyperparameters or paths for training
│   │   └── dataset_config.json                    # (Dataset Config) Info on datasets, transformations, splitting
│   ├── scripts/
│   │   ├── train.py                               # (Training Script) Model training logic
│   │   ├── evaluate.py                            # (Evaluation Script) Assesses model performance
│   │   └── inference.py                           # (Inference Script) Applies model to new data
│   └── notebooks/
│       └── exploratory_analysis.ipynb             # (Jupyter Notebook) Data exploration, experiments
├── src/                                           # (Source Code) Main app logic
│   ├── __init__.py                                # (Python Init) Declares this dir as a Python package
│   ├── main.py                                    # (Entry Point) Primary script to start the application
│   ├── chatgpt_integration.py                     # (ChatGPT-01 Integration) Logic to interact w/ ChatGPT
│   ├── ui/
│   │   ├── app.py                                 # (UI / Flask App) Example web interface
│   │   └── setup_prompt.py                        # (Hosting Prompt) Localhost vs. remote environment
│   └── templates/
│       └── dashboard.html                         # (UI Template) Example HTML for a dashboard
│   ├── config/
│   │   ├── settings.json                          # (App Config) High-level app settings/environment info
│   │   ├── secrets.json                           # (Sensitive Config) Possibly omitted from version control
│   │   └── settings_loader.py                     # (Config Loader) Merges settings & secrets into one config dict
│   ├── modules/
│   │   ├── example_module.py                      # (Module Example) Additional functionalities/classes
│   │   ├── data_analyzer.py                       # (Data Analysis) Complex transformations, checks
│   │   └── report_generator.py                    # (Reporting) Produce PDF/Markdown/JSON/Excel
│   ├── utils/                                     # (Utilities & Scanners)
│   │   ├── file_utils.py                          # (Utility Functions) For file I/O, path ops, etc.
│   │   ├── file_editor.py                         # Real-time or output-only file edits
│   │   ├── missing_logic_detector.py              # Detects placeholders (TODO, pass, NotImplementedError)
│   │   ├── file_structure_scanner.py              # Recursively scans file/folder structure
│   │   ├── requirements_scanner.py                # Checks Python deps (requirements.txt, environment.yml)
│   │   ├── docker_scanner.py                      # Dockerfile/docker-compose.yml analysis
│   │   ├── ml_scanner.py                          # ML folder checks (configs, scripts, notebooks)
│   │   ├── env_file_scanner.py                    # Ensures .env usage & parse
│   │   ├── security_scanner.py                    # Finds potential security issues/hardcoded secrets
│   │   ├── duplicate_finder.py                    # Detects duplicate or redundant files
│   │   ├── logging_scanner.py                     # Logging & monitoring usage checks
│   │   ├── testing_scanner.py                     # Testing frameworks, coverage configs, etc.
│   │   └── project_analyzer.py                    # (Master Coordinator) Orchestrates all sub-scanners
│   └── ...
├── tests/                                         # (Test Suite) For unit, integration, or end-to-end tests
│   ├── test_main.py                               # (Unit Test) Tests for main.py
│   ├── test_example_module.py                     # (Unit Test) Tests for example_module.py
│   ├── integration/
│   │   └── test_integration_example.py            # (Integration Test) Cross-module checks
│   ├── e2e/
│   │   └── test_end_to_end_flow.py                # (End-to-End Test) Tests the entire workflow
│   └── conftest.py                                # Shared fixtures or hooks for Pytest
├── ml/
│   ├── test_train.py                              # Tests for ml/scripts/train.py
│   ├── test_evaluate.py                           # Tests for ml/scripts/evaluate.py
│   └── test_inference.py                          # Tests for ml/scripts/inference.py
├── cypress/                                       # (Cypress E2E Tests) If using Cypress for front-end testing
│   ├── fixtures/
│   ├── integration/
│   ├── plugins/
│   └── support/
├── scripts/                                       # (DevOps/Automation Scripts)
│   ├── clean_data.py                              # (Data Cleaning) e.g., removing duplicates, nulls
│   ├── generate_configs.py                        # (Config Generator) Creates/updates JSON config files
│   └── deploy.sh                                  # (Deployment Script) Automates build & deployment steps
├── output/                                        # (Analyzer Output) For reports/updated files if "Output Only" chosen
│   ├── updated_files/                             # (Generated Files) New/modified versions of original files
│   └── reports/
│       ├── analysis_report.pdf                    # (PDF Report) Summaries & recommendations from Code Analyzer
│       ├── analysis_report.md                     # (Markdown Report) Same as PDF, in Markdown
│       ├── analysis_report.json                   # (JSON Report) Machine-readable summary of the analysis
│       └── analysis_report.xlsx                   # (Excel Report) Optional Excel format
├── .bak/                                          # (Backup Files) Temporary or backup directory
│   └── main.py.bak                                # (Backup Example) Backup of a key file
└── ...
```

---

## Contributing

We welcome improvements and suggestions! Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on how to get started.

---

## Security

For information on reporting vulnerabilities, please see [`SECURITY.md`](SECURITY.md).

---

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.

---

## Contact

- **Maintainer**: Your Name ([you@example.com](mailto\:you@example.com))
- **Security Issues**: Refer to [`SECURITY.md`](SECURITY.md)

Happy analyzing! If you have any questions, consult the [`USER_MANUAL.md`](USER_MANUAL.md) or open an issue on GitHub.

