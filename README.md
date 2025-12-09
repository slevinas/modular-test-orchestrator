# Modular Test Orchestrator

A **modular, CI-friendly test orchestration system**.

The long-term goal is to show how you can:

- Prepare remote runners (VMs / containers)
- Use **Ansible playbooks** to install Docker & Python
- Spin up test stacks via `docker-compose`
- Run **pytest** test suites
- Publish results to **Allure** or other reporting systems

Right now this repo is at **Stage 1: Local + CI smoke tests**  
Next stages will gradually add:

- Ansible orchestration under `ansible/`
- A Python orchestration layer under `orchestrator/`
- Example Dockerized test targets under `docker/`
- CI workflows that drive everything end-to-end

---

## Repo Layout (current)

```text
.
├── README.md
├── ansible/          # Ansible inventories, playbooks, roles (coming next)
├── docker/           # Docker & docker-compose test stack (TBD)
├── docs/             # Design notes, diagrams
├── orchestrator/     # Python layer that will call Ansible / Docker
├── tests/            # pytest suites
├── pytest.ini        # pytest config
└── .github/workflows # CI workflows
````

---

## Quickstart: run tests locally

```bash
# from repo root
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install pytest

pytest
```

You should see the example smoke test pass.

---

## CI: GitHub Actions

This repo ships with a very small CI workflow that:

1. Checks out the code
2. Sets up Python
3. Installs pytest
4. Runs the test suite

See: `.github/workflows/ci-smoke.yml`.

---

## Roadmap (high-level)

* [ ] **Stage 1** – Local pytest + basic CI (this commit)
* [ ] **Stage 2** – Add minimal Docker stack and test against a sample service
* [ ] **Stage 3** – Add Ansible playbooks to provision / run tests remotely
* [ ] **Stage 4** – Add Allure publishing and richer reporting
* [ ] **Stage 5** – Documentation + diagrams for LinkedIn / portfolio