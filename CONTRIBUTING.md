# Contributing to ADPilot Pro

Thank you for your interest in contributing to **ADPilot Pro** — the Enterprise Autonomous Marketing Operating System. This guide covers everything you need to get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Branching Strategy](#branching-strategy)
5. [Coding Standards](#coding-standards)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)
8. [Schema Change Protocol](#schema-change-protocol)
9. [Documentation Contributions](#documentation-contributions)
10. [Testing Requirements](#testing-requirements)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to **gharieb@adpilot.dev**.

---

## Getting Started

1. **Fork** the repository: [github.com/GhariebML/ADPilot-Pro](https://github.com/GhariebML/ADPilot-Pro)
2. **Clone** your fork locally
3. **Create** a feature branch from `main`
4. **Make** your changes
5. **Submit** a Pull Request

---

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Backend runtime |
| Node.js | 20+ | Frontend toolchain |
| Git | 2.40+ | Version control |

### Backend Setup

```powershell
# Clone the repository
git clone https://github.com/GhariebML/ADPilot-Pro.git
cd ADPilot-Pro

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows
# source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
Copy-Item .env.example .env
# Edit .env with your API keys (or run in mock mode)

# Start the FastAPI server
$env:PYTHONPATH="src"
uvicorn adpilot.api.main:app --host 127.0.0.1 --port 8001 --reload
```

### Frontend Setup

```powershell
cd frontend
npm install
npm run dev
# Dashboard available at http://localhost:3000
```

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable production code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `docs/*` | Documentation updates |

```powershell
# Create a feature branch
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

---

## Coding Standards

### Python (Backend)

- **Type Hints**: All functions must have complete type annotations.
- **Pydantic v2**: All data contracts use strict Pydantic `BaseModel` schemas.
- **Async-First**: Agent interfaces and API endpoints must be `async`.
- **Linting**: Code must pass `ruff check .` and `ruff format --check .` with zero errors.
- **Docstrings**: Public classes and functions require Google-style docstrings.

### TypeScript (Frontend)

- **Strict Mode**: TypeScript strict mode enabled (`"strict": true`).
- **Functional Components**: React components must be functional (no class components).
- **Interface Types**: All props defined with TypeScript `interface` declarations.
- **Linting**: Code must pass `npm run lint` with zero errors.

### General Rules

- Keep methods small and focused (< 50 lines).
- No raw string passing between agents — use typed Pydantic schemas.
- No hardcoded API keys, secrets, or credentials in source code.
- Do not modify unrelated files in your PR.

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short description>

[optional body]
[optional footer]
```

### Types

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `ci` | CI/CD changes |
| `chore` | Build process, dependencies |

### Examples

```text
feat(rl): add Dirichlet constraint projection to PPO policy
fix(rag): correct RRF fusion constant from k=30 to k=60
docs(agents): add causal explainability tree documentation
test(hitl): add HMAC-SHA256 signature verification test
ci(actions): add frontend Vitest job to CI pipeline
```

---

## Pull Request Process

1. **Ensure all tests pass** before opening a PR.
2. **Fill out the PR template** completely.
3. **Link relevant issues** using `Closes #123` or `Fixes #456`.
4. **Include testing evidence** (test output, screenshots for UI changes).
5. **Request review** from `@GhariebML`.
6. **Address all review comments** before merge.

### Code Review Checklist

- [ ] Code compiles and all tests pass
- [ ] Type annotations are complete
- [ ] Pydantic schemas are used for inter-agent contracts
- [ ] No secrets, credentials, or API keys in code
- [ ] Documentation updated if behavior changed
- [ ] Commit messages follow Conventional Commits format

---

## Schema Change Protocol

Shared schemas in `src/adpilot/schemas/` are **contracts between agents** and must be treated with care:

1. **Open an Issue First** — Create a `Schema Change Request` issue explaining the proposed change.
2. **Document Impact** — List all affected agents and downstream contracts.
3. **Backward Compatibility** — Schema changes must be backward-compatible unless a major version bump is planned.
4. **Tests Required** — Add or update tests for every schema modification.
5. **Team Lead Approval** — Schema changes require explicit approval from `@GhariebML`.

---

## Documentation Contributions

The comprehensive documentation package lives under [`docs/adpilot_system/`](docs/adpilot_system/DOCUMENTATION_INDEX.md) (56 files across 9 subdirectories).

### Guidelines

- All documentation must reflect the **actual current codebase**, not planned features.
- Use `[IMPLEMENTED]`, `[PARTIAL]`, `[PLANNED]`, or `[NOT FOUND]` status tags.
- Reference actual source file paths with clickable links.
- Include code snippets from the real implementation.
- Mathematical formulations use LaTeX notation.

---

## Testing Requirements

### Backend (pytest)

```powershell
$env:PYTHONPATH="src"
pytest tests/ -v
```

### Frontend (Vitest)

```powershell
cd frontend
npm test -- --run
```

### Quality Gates

| Gate | Command | Threshold |
|------|---------|-----------|
| Python Lint | `ruff check .` | 0 errors |
| Python Format | `ruff format --check .` | 0 violations |
| Backend Tests | `pytest tests/ -v` | 100% pass |
| Frontend Tests | `npm test -- --run` | 100% pass |
| Production Build | `npm run build` | 0 errors |

---

<p align="center">
  <strong>Thank you for helping make ADPilot Pro better! 🚀</strong>
</p>
