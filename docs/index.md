---
title: Modular Test Orchestrator
---

> **A containerized testing harness demonstrating CI/CD automation, service orchestration, and Python-based smoke testing.**

<img src="https://img.shields.io/badge/Python-3.11-blue" />
<img src="https://img.shields.io/badge/GitHub%20Actions-CI-green" />
<img src="https://img.shields.io/badge/Docker-Compose-blue" />

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

```

[ GitHub Actions CI ]
|--> build test-target image
|--> start container
|--> run pytest smoke

[docker-compose.test-target.yml]
|--> FastAPI "test-target" app
|--> HTTP (localhost:8000)

[pytest smoke suite]
|--> health + echo tests
|--> httpx client

```



---

> 🔗 **Source code**: [https://github.com/slevinas/modular-test-orchestrator](https://github.com/slevinas/modular-test-orchestrator)


> **Related:**
> 🔧 [Benchmaker-Lite — FastAPI Benchmarking & Observability Pipeline](https://slevinas.github.io/benchmaker-lite/)

---
