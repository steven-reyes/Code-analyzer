# Contributing to Code Analyzer

We appreciate your interest in contributing! Below are guidelines to help ensure a smooth collaboration.

---

## 1. Getting Started

1. **Fork** the repo on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/steven-reyes/code-analyzer.git
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature/awesome-update
   ```

---

## 2. Development Workflow

1. **Set up your environment**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
     Or, if using Conda:
     ```bash
     conda env create -f environment.yml
     conda activate code-analyzer-env
     ```
   - Install Node dependencies (if contributing to the front-end):
     ```bash
     npm install
     ```

2. **Run pre-commit hooks** (if configured):
   ```bash
   pre-commit install
   ```

3. **Lint and test your changes**:
   - Python:
     ```bash
     flake8 .  # Python lint
     black .   # Python format
     pytest --maxfail=1 -v  # Python tests
     ```
   - JavaScript/Node.js:
     ```bash
     npm run lint  # JS lint
     npm run test  # JS tests
     ```

---

## 3. Making Changes

1. **Focus your commits**:
   - Keep commits focused and atomic.
   - Use clear and descriptive commit messages.

2. **Add or update tests and documentation**:
   - Ensure that your changes include adequate test coverage.
   - Update related documentation (e.g., `README.md`, `USER_MANUAL.md`, etc.).

3. **Fix bugs by referencing issue numbers** (if applicable):
   - Include a reference to the issue in your commit message or PR description, e.g., `Fixes #123`.

---

## 4. Submitting a Pull Request (PR)

1. **Push your branch** to GitHub:
   ```bash
   git push origin feature/awesome-update
   ```

2. **Open a PR** against the `main` branch in our repository.
3. **Fill out the PR template** (if available) with details such as:
   - What changes were made?
   - Why are these changes needed?
   - Are there any open concerns or questions?

---

## 5. Code Style

1. **Python**:
   - Code is formatted using Black and linted with Flake8 or Pylint.
   - Follow PEP 8 guidelines for Python code.

2. **JavaScript/Node.js**:
   - Code is formatted using Prettier and linted with ESLint.
   - Follow existing patterns and naming conventions.

---

## 6. Communication

1. For major changes, open an issue first to discuss your approach.
2. For security issues, refer to [`SECURITY.md`](SECURITY.md).

---

## 7. License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for your contribution!

