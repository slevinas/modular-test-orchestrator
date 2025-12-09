# Modular Test Orchestrator

A small, focused repo that demonstrates how to:

- Spin up a **Dockerized test target** (FastAPI service)
- Drive it using **pytest smoke tests**
- Run everything in **GitHub Actions CI** on every push / PR

This is a “mini version” of a larger modular testing/orchestration system I built at XPLG, but trimmed down to be easy to read and reuse.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Repository Layout](#repository-layout)
- [Local Development](#local-development)
  - [Prerequisites](#prerequisites)
  - [Start the Test Target](#start-the-test-target)
  - [Run Smoke Tests](#run-smoke-tests)
- [CI Pipeline](#ci-pipeline)
- [Ansible Automation (Future Stage)](#ansible-automation-future-stage)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

This project is a **modular testing harness**:

- A lightweight **FastAPI “test target”** runs inside Docker.
- A **pytest test suite** performs health checks and round-trip tests.
- A **GitHub Actions workflow** builds the container, runs smoke tests, and tears everything down.

The goal is to demonstrate how to take a small service and wrap it with production-style testing and CI orchestration.

---

## Architecture

High-level flow:

1. **Docker test target**: `docker/docker-compose.test-target.yml` starts a FastAPI app that exposes:
   - `GET /health`
   - `GET /echo?value=...`
2. **Test runner**: `pytest` (locally or in CI) calls these endpoints using `httpx`.
3. **CI**: GitHub Actions:
   - builds & runs the Docker service
   - executes smoke tests (`pytest -m smoke`)
   - stops & removes containers after the run

You can think of it as:

```text
pytest (smoke)  →  Dockerized FastAPI test target  →  CI (GitHub Actions)
````

Later stages will plug in **Ansible** to provision remote runners and orchestrate tests on real infrastructure.

---

## Repository Layout

```text
.
├── README.md
├── ansible/               # future: runner provisioning & orchestration
│   ├── inventories/
│   ├── playbooks/
│   │   ├── deploy-test-stack.yml
│   │   ├── fetch-allure-results.yml
│   │   ├── install-docker.yml
│   │   ├── provision-runner.yml
│   │   └── run-tests.yml
│   └── roles/
├── docker/                # Docker-based test target
│   ├── Dockerfile
│   └── docker-compose.test-target.yml
├── docs/
│   └── Curren.md          # design notes / scratchpad
├── orchestrator/          # future: higher-level orchestration logic
├── tests/                 # pytest suite for the test target
│   └── test_target_smoke.py
├── pytest.ini
└── requirements.txt
```

---

## Local Development

### Prerequisites

* Python **3.11+**
* Docker + Docker Compose (`docker compose` CLI)

Install Python dependencies once:

```bash
python -m venv .venv
source .venv/bin/activate       # on Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Start the Test Target

From the repo root:

```bash
cd docker
docker compose -f docker-compose.test-target.yml up --build
```

The FastAPI test target will be available at:

* `http://localhost:8080/health`
* `http://localhost:8080/echo?value=hello`

### Run Smoke Tests

In another terminal (with the venv activated), from the repo root:

```bash
pytest -m smoke -vv
```

What this does:

* `test_health_and_info` validates `/health`.
* `test_echo_round_trip` validates the echo endpoint round-trip behavior.

---

## CI Pipeline

CI is defined in: `.github/workflows/ci-test-target.yml`.

On every **push** and **pull request** to `main`:

1. Check out the repo.

2. Set up Python 3.11.

3. Install dependencies from `requirements.txt`.

4. Build & start the Docker test target:

   ```bash
   cd docker
   docker compose -f docker-compose.test-target.yml up -d --build
   ```

5. Run smoke tests:

   ```bash
   pytest -m smoke -vv
   ```

6. Always tear down the container:

   ```bash
   cd docker
   docker compose -f docker-compose.test-target.yml down
   ```

This makes the repo self-checking: if the container or basic endpoints break, CI will fail.

---

## Ansible Automation (Future Stage)

The next step for this project is to mirror the **real-world setup** I used at XPLG:

* Provision GitHub runners or test VMs using **Ansible**.
* Install Docker / Python on the remote.
* Deploy the test target stack remotely.
* Trigger pytest runs via Ansible playbooks.
* Optionally collect **Allure** results and artifacts.

Folders already stubbed out for this:

* `ansible/playbooks/*`
* `ansible/inventories/*`
* `ansible/roles/*`

---

## Roadmap

**Short term**

* [ ] Add more smoke tests (failure modes, non-200s).
* [ ] Add `Makefile` helpers (`make up`, `make test`, `make ci-local`).
* [ ] Add linting / formatting (ruff, black) and wire into CI.

**Medium term**

* [ ] Implement Ansible playbooks for remote runner setup.
* [ ] Add Allure reporting for pytest results.
* [ ] Add parameterized test targets (different images / versions).

**Long term**

* [ ] Turn this into a reusable template for “test harness around any service”.
* [ ] Add support for multiple environments (dev / staging / prod) via inventories.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

