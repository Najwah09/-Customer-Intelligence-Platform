# Contributing to Telecom Customer Intelligence Platform (CIP) 🤝

Thank you for your interest in contributing to the **Telecom Customer Intelligence Platform**! This guide outlines development setup, coding standards, automated testing requirements, and contribution workflows.

---

## 🛠️ Development Setup

### 1. Prerequisites
- **Python 3.10 - 3.12**
- **Git**
- **Docker & Docker Compose** (Optional for local container testing)

### 2. Environment Setup

```bash
# Clone repository
git clone https://github.com/sarafirdose/-Customer-Intelligence-Platform.git
cd -Customer-Intelligence-Platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies in editable mode
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

---

## 🧪 Testing Guidelines & TDD

Every new feature or bug fix must include automated unit/integration tests before merging.

### Running Test Suite

```bash
# Run full 132-test suite with coverage
pytest tests/ -v

# Run specific dashboard tests
pytest tests/test_dashboard.py -v

# Run MLOps & scheduler tests
pytest tests/test_mlops.py -v
```

---

## 🔄 Automated Ingestion & Watch Folder Workflow

When testing data ingestion locally:
1. Place raw subscriber CSV files into `data/incoming/`.
2. The APScheduler background scanner automatically processes valid files every **1 minute**.
3. Processed files are archived in `data/processed/` and invalid files are moved to `data/failed/`.
4. Run manual watch folder verification:
   ```bash
   python scripts/test_auto_ingestion.py
   ```

---

## 🎨 Code Style & Conventions

- **Formatter**: Follow PEP 8 style guidelines.
- **Type Hints**: Use Python type annotations for function parameters and return types (`typing.Dict`, `typing.List`, `typing.Optional`).
- **Docstrings**: Include clear Google/Sphinx style docstrings for classes and public methods.

---

## 📬 Submitting Pull Requests

1. Fork the repository & create a feature branch (`git checkout -b feat/your-feature-name`).
2. Make clean, atomic commits with conventional commit messages (`feat:`, `fix:`, `docs:`, `test:`).
3. Ensure `pytest tests/ -v` passes with **100% PASS** rate.
4. Push to your fork and submit a Pull Request targeting the `main` branch.

---

## 👤 Maintainer
- **Sara Firdose** (@sarafirdose)
