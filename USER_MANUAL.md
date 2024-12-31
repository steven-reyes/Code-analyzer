# User Manual for Code Analyzer

## 1. Introduction
Welcome to the **Code Analyzer**! This locally hosted application is designed to analyze public/private repositories or local project directories. It identifies inefficiencies, suggests optimizations, and provides detailed recommendations to improve code quality, structure, and scalability.

---

## 2. System Requirements

To run Code Analyzer successfully, ensure the following prerequisites are met:
- **Python** 3.9+
- **Node.js** 16+ (if using the Node front-end or scripts)
- **Docker** & **Docker Compose** (optional, for containerized deployment)
- **Git** (to clone repositories if needed)

---

## 3. Installation Guide

### 3.1 Python Environment (Using Pip)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/steven-reyes/code-analyzer.git
   cd code-analyzer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional**: Use Conda if preferred:
   ```bash
   conda env create -f environment.yml
   conda activate code-analyzer-env
   ```

### 3.2 Node.js (If Using the Front-End or Node Scripts)

1. **Install Node dependencies**:
   ```bash
   npm install
   ```

2. **Run Node-based tasks**:
   ```bash
   npm run lint
   npm run build
   npm run start
   ```

### 3.3 Docker / Docker Compose (Optional)

1. **Build the Docker image**:
   ```bash
   docker build -t code-analyzer:latest .
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   This will spin up the web and database containers if configured in `docker-compose.yml`.

---

## 4. Configuration & Running Locally

1. **Environment Variables**:
   Create a `.env` file in the project root to store environment variables like:
   ```env
   CHATGPT_API_KEY=your_openai_api_key
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. **Running the Python Application**:
   ```bash
   python src/main.py
   ```
   Access the Flask web application at `http://localhost:5000` or interact via the CLI.

---

## 5. Usage Examples

### Analyzing a Local Project
Run the following command, replacing `/path/to/project` with the path to your project directory:
```bash
python src/main.py --project-path /path/to/project
```

### Analyzing a GitHub Repository
Provide the GitHub URL of the repository to analyze:
```bash
python src/main.py --github-url https://github.com/username/repo
```

### ChatGPT Integration (Optional)
Chat with ChatGPT to get real-time suggestions for your code. Ensure your `CHATGPT_API_KEY` is set in the `.env` file.

---

## 6. Troubleshooting

### Common Issues

- **Missing Dependencies**:
  Ensure that all dependencies in `requirements.txt` or `environment.yml` are installed.

- **Docker Issues**:
  - Check that the Docker daemon is running.
  - Ensure sufficient memory allocation for Docker containers.

- **Permission Errors**:
  If your OS blocks file writing, try running the application as an administrator or fixing file permissions.

- **API Key Errors**:
  Verify that `CHATGPT_API_KEY` is correctly set in the `.env` file.

### Debugging
Run the application in debug mode for detailed error logs:
```bash
python src/main.py --debug
```

---

## 7. Advanced Setup & Deployment

### Production Environment

1. **Set Flask to production mode**:
   ```bash
   export FLASK_ENV=production
   ```

2. **Run behind a reverse proxy** (e.g., Nginx):
   - Use Nginx to handle HTTPS and forward traffic to Flask.

### Scaling
Use Kubernetes or hosted container services to deploy at scale. Refer to `k8s/` if a Kubernetes configuration is provided.

### CI/CD Integration
Automate deployment and testing using GitHub Actions. See `.github/workflows/ci.yml` for pipeline configuration.

---

## 8. Known Limitations

- The application currently supports Python and JavaScript repositories.
- Large repositories may take longer to analyze.
- Requires a valid OpenAI API key for ChatGPT integration.

---

## 9. Additional Resources

- **Architecture Documentation**: See `docs/architecture.md` for a high-level overview of system design.
- **API Documentation**: Refer to `docs/api.md` for endpoint details.
- **CHANGELOG.md**: Review release notes and version history.

Enjoy using the Code Analyzer! For further assistance, feel free to open an issue on GitHub or contact the project maintainer.

