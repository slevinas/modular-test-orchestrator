---
title: Modular Test Orchestrator
---

# Modular Test Orchestrator

**Dockerized test target + Pytest smoke tests + GitHub Actions CI**

This project is a **minimal but realistic testing harness** that shows how to:

- Spin up a **FastAPI test target** in Docker
- Run **smoke tests** against it with `pytest` + `httpx`
- Wire everything into a **GitHub Actions pipeline**

It’s a small, focused demo of how you can take a service from “runs on my laptop” to “tested automatically on every push”.

---

## 🔎 What this project demonstrates

- **Containerized test target**

  - FastAPI app packaged in a Docker image  
  - Health endpoint + simple echo endpoint
  - `docker-compose.test-target.yml` spins it up on a dedicated network

- **Pytest smoke suite**

  - `tests/test_target_smoke.py`
  - Verifies:
    - `/health` returns 200 + basic info
    - `/echo` round-trip behaves as expected
  - Marked with `@pytest.mark.smoke` so CI can run just the fast checks

- **GitHub Actions CI**

  - Workflow:
    1. Build + start the **test-target** container
    2. Run `pytest -m smoke -vv`
    3. Tear everything down with `docker compose down`
  - Mirrors the kind of “lightweight, always-on” verification you’d run on every PR

- **Extensible design**

  - Space reserved for **Ansible** roles / playbooks (future step)
  - Easy to add:
    - More endpoints & tests
    - Allure reporting
    - Remote VM provisioning via Ansible

---

## ⚙️ Architecture at a glance

```text
          ┌──────────────────────────┐
          │   GitHub Actions CI      │
          │  - build test target     │
          │  - run pytest smoke      │
          └─────────────┬────────────┘
                        │
                        ▼
        ┌────────────────────────────────┐
        │   docker-compose.test-target   │
        │  - FastAPI "test-target" app   │
        │  - dedicated network           │
        └─────────────┬──────────────────┘
                      │  HTTP (localhost:8000)
                      ▼
          ┌──────────────────────────┐
          │  Pytest smoke suite      │
          │  - health + echo tests   │
          │  - httpx client          │
          └──────────────────────────┘
