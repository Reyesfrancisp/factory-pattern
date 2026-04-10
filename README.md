# Factory Pattern Model - Calculator API

## Project Overview
This project is a high-performance, containerized Calculator API built with **FastAPI** and **PostgreSQL**. It demonstrates advanced software engineering principles including the **Polymorphic Factory Pattern**, **SQLAlchemy ORM** for data persistence, and **Pydantic** for robust schema validation.

This repository fulfills the Module 11 assignment for **IS 601 at NJIT**, focusing on refactoring legacy code into a scalable, production-ready architecture with a comprehensive CI/CD pipeline.

### Refactoring & Improvements
* **Polymorphic Model**: Refactored the calculation data model to use dedicated `a` and `b` float columns, replacing generic input fields.
* **Factory Pattern**: Implemented a factory for calculator operations to ensure a decoupled and extensible architecture.
* **PostgreSQL Stability**: Pinned the database to **PostgreSQL 16** to ensure cross-platform compatibility and avoid data directory conflicts found in newer versions.
* **Security & Best Practices**: Configured the Docker environment to run as a non-root `appuser`.

---

## Technical Stack
* **Backend**: FastAPI (Python 3.10)
* **Database**: PostgreSQL 16
* **ORM**: SQLAlchemy
* **Testing**: Pytest & Playwright (E2E)
* **DevOps**: Docker, GitHub Actions, Docker Hub, Trivy (Security Scanning)

---

## Getting Started

### Prerequisites
* Docker Desktop installed.
* Git.

### Installation & Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Reyesfrancisp/factory-pattern.git](https://github.com/Reyesfrancisp/factory-pattern.git)
    cd factory-pattern
    ```

2.  **Environment Configuration:**
    Ensure a `.env` file exists in the root directory with the following variables:
    ```env
    DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=fastapi_db
    ```

3.  **Launch the Environment:**
    Build and start the containers in detached mode:
    ```bash
    docker-compose up -d --build
    ```

---

## Running Tests

To maintain environment parity, tests should be executed inside the running `web` container.

### 1. Install E2E Browser Binaries
Because the container runs as a restricted user, Playwright browsers must be installed as root once the container is up:
```bash
docker-compose exec --user root web playwright install --with-deps chromium
```

### 2. Run the Test Suite
Execute unit, integration, and E2E tests with coverage reporting:
```bash
docker-compose exec web pytest --cov=app --cov-report=term-missing
```

**Note:** The project maintains a high coverage standard (**95%+**), ensuring that the core logic, polymorphic relationships, and API endpoints are thoroughly verified.

---

## CI/CD Pipeline
The automated pipeline is configured via GitHub Actions (`.github/workflows/test.yml`):

* **Test Suite**: Validates all code changes against a PostgreSQL service container.
* **Security Audit**: Scans the built image for vulnerabilities using **Trivy**.
* **Automated Deployment**: Builds and pushes the finalized image to Docker Hub on successful `main` branch updates.

**Docker Hub Repository:** [reyesfrancisp/factory-pattern-model](https://hub.docker.com/r/reyesfrancisp/factory-pattern-model)

---

## Author
**Francis Reyes**
* **NJIT UCID**: fdr7
* **Course**: IS 601 - Web Systems Development