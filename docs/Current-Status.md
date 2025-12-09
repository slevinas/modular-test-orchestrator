# Modular Test Orchestrator

A **modular, CI-friendly test orchestration system**.

The  goal is to show how to:

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




Perfect, going with **D** is exactly what I was hoping you’d pick 🙃
Let’s design the **public repo structure** first, then we can slowly “pour” pieces of the XPLG system into it in a safe, generic way.

---

## 1. Proposed Repo Name + One-liner

**Repo name idea:** `modular-test-orchestrator`

**Tagline (for GitHub + LinkedIn later):**

> A modular, Ansible-driven test orchestrator for spinning up remote environments, running Pytest suites in Docker, and publishing Allure reports via CI.

We keep it generic (no XPLG, no Flux, no vendor-specific wording).

---

## 2. Target Folder Structure (High-Level)

Here’s the **outline** I suggest for the new repo:

```text
modular-test-orchestrator/
├── README.md
├── pyproject.toml               # or setup.cfg / setup.py (your choice)
├── pytest.ini
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci-orchestrator.yml          # main CI pipeline
│       ├── ensure-infra.yml             # optional: infra checks
│       └── run-pytest-and-publish.yml   # example “job”
├── ansible/
│   ├── inventories/
│   │   ├── dev.ini
│   │   └── example_hosts.ini
│   ├── playbooks/
│   │   ├── provision-runner.yml         # create dirs, users, etc.
│   │   ├── install-docker.yml
│   │   ├── deploy-test-stack.yml        # pull images / docker-compose
│   │   ├── run-tests.yml                # run pytest inside container
│   │   └── fetch-allure-results.yml     # pull artifacts back
│   └── roles/
│       ├── docker/
│       │   ├── tasks/
│       │   │   ├── install.yml
│       │   │   └── login_registry.yml   # optional
│       ├── python-env/
│       │   └── tasks/
│       │       └── setup_venv.yml
│       └── test-runner/
│           └── tasks/
│               ├── run_pytest.yml
│               └── collect_results.yml
├── orchestrator/
│   ├── __init__.py
│   ├── config.py               # reads YAML/ENV for target hosts, test suite, etc.
│   ├── ansible_runner.py       # Python wrapper around ansible-playbook
│   ├── ssh_helpers.py          # safe, generic SSH helpers (optional)
│   └── allure_push.py          # generic Allure upload, adapted from your old code
├── tests/
│   ├── conftest.py
│   ├── test_example_smoke.py   # small, generic test suite
│   └── resources/
│       └── example_data.json
├── docker/
│   ├── docker-compose.test.yml   # test stack: app + db + whatever
│   └── Dockerfile.runner         # image for running pytest
└── docs/
    ├── Architecture.md           # textual + diagrams (we’ll match Benchmaker style)
    ├── CI-Pipeline.md
    └── Ansible-Playbooks.md
```

This mirrors the **spirit** of your XPLG project:

* `.github/workflows` ⟶ from your existing CI orchestrator YAMLs
* `ansible/` ⟶ replacement for `.ansible` + infra configs
* `orchestrator/` ⟶ clean Python layer replacing your orchestration scripts
* `tests/` ⟶ a small, generic example instead of the full proprietary “flux” suite
* `docker/` ⟶ Docker/compose helpers, but **generic** (no vendor services)

---

## 3. How Your Old Tree Maps Into This

From your original structure:

* `.ci`, `.github/workflows`, `.ansible`
* `scripts/orchestrate_flux_tests*.py` / `.sh`
* `infra/flux-test-ci/configure_git_runner.sh`
* `suites/flux/src/...` (API clients, Jinja templates, task runners, etc.)
* `common/push_to_allure_service.py`

We **don’t copy** all of that 1:1. Instead:

### ✅ Safe to “conceptually port”:

* The *idea* of:

  * “Prepare remote runner”
  * “Start docker compose”
  * “Run pytest”
  * “Collect results”
  * “Push Allure results”
* Your Ansible structure: roles, playbooks, inventories
* The orchestration logic (steps, state machine, error handling), but rewritten generically
* The Allure push helper → becomes `orchestrator/allure_push.py`
* The SSH helpers → becomes `orchestrator/ssh_helpers.py`

### ❌ Should *not* port directly:

* Any XPLG-specific naming (flux, product names, internal URL paths, proprietary APIs)
* Real Jinja templates or XML configs for their product
* Real test cases or business-logic assertions from the company
* Any customer data or log paths

We’ll create **new**, simple test targets instead:

* e.g. a tiny sample FastAPI or Flask app container
* tests verify basic endpoints, small workloads, etc.
* the focus is on **orchestration mechanics**, not business domain.

---

## 4. README Outline (for Later, Not Now)

Once the structure exists, the README for this repo will likely have sections like:

1. **Overview** — “What is this orchestrator?”
2. **Architecture** — diagram: GitHub Actions → Ansible → Remote Host → Docker → Pytest → Allure
3. **Components** — `ansible/`, `orchestrator/`, `tests/`, `docker/`
4. **Running Locally** — `docker-compose -f docker/docker-compose.test.yml up`
5. **Running via Ansible** — `ansible-playbook ansible/playbooks/run-tests.yml -i ansible/inventories/dev.ini`
6. **CI Example** — how the GH Action triggers the orchestrator.

We’ll mirror the polish from Benchmaker-Lite, but oriented around **CI / Ansible / testing** instead of OTEL.

---

## 5. Concrete Next Micro-Step

To keep things simple and momentum high, here’s what I suggest you do next:

1. **Create a new empty repo locally** (don’t push yet if you want privacy while we shape it):

   ```bash
   mkdir modular-test-orchestrator
   cd modular-test-orchestrator
   git init
   mkdir -p .github/workflows ansible/{inventories,playbooks,roles} orchestrator tests docker docs
   touch README.md pytest.ini .gitignore
   ```
2. Inside `ansible/playbooks/`, create *empty* files:

   ```bash
   touch ansible/playbooks/{provision-runner.yml,install-docker.yml,deploy-test-stack.yml,run-tests.yml,fetch-allure-results.yml}
   ```
3. Inside `.github/workflows/`, create one empty workflow file:

   ```bash
   touch .github/workflows/ci-orchestrator.yml
   ```

Then you can **paste me the new tree output**:

```bash
tree -C -I ".git" .
```

…and I’ll start **filling in**:

* a minimal `README.md` first
* a simple initial `ci-orchestrator.yml`
* stubbed Ansible playbooks with comments
* and a tiny example test app/test.

---

If you’d rather not touch the shell right now, I can instead:

* write the **exact contents** for `README.md` + initial files so you can just copy-paste them into the new repo.

Up to you, but the strategic answer to your question is:

> **Best next move: scaffold this second project’s repo (like above), then we’ll gradually pour in generic versions of your XPLG orchestrator logic.**

If you tell me **“Let’s scaffold the files now”**, I’ll give you copy-paste content for:

* `README.md` (v1)
* `.github/workflows/ci-orchestrator.yml` (skeleton)
* `ansible/playbooks/run-tests.yml` (skeleton)
* `orchestrator/ansible_runner.py` (skeleton)


---

Nice, this is a perfect clean scaffold to start from 👌

Let’s do a **small but complete “Stage 1”**:

> ✅ Repo has a clear README,
> ✅ pytest works locally,
> ✅ a basic CI workflow runs tests on GitHub.

Then in the next round we’ll layer on Ansible orchestration + Docker.

---

## 1. Add a GitHub Actions workflow + orchestrator package

Run these commands in the repo:

```bash
cd ~/Zigi-work/repositories/modular-test-orchestrator

# CI folder
mkdir -p .github/workflows

# orchestrator package
mkdir -p orchestrator
touch orchestrator/__init__.py
```

---

## 2. Replace `README.md` with this (v1)

````md
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

As we add Ansible and Docker orchestration, we’ll extend CI to:

* provision test runners
* run Ansible playbooks
* publish test artifacts (e.g., Allure results)

---

## Roadmap (high-level)

* [ ] **Stage 1** – Local pytest + basic CI (this commit)
* [ ] **Stage 2** – Add minimal Docker stack and test against a sample service
* [ ] **Stage 3** – Add Ansible playbooks to provision / run tests remotely
* [ ] **Stage 4** – Add Allure publishing and richer reporting
* [ ] **Stage 5** – Documentation + diagrams for LinkedIn / portfolio

````

---

## 3. Minimal `pytest.ini`

Put this into `pytest.ini` (overwrite if needed):

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -q
````

---

## 4. Add a tiny smoke test

Create `tests/test_smoke_example.py`:

```python
# tests/test_smoke_example.py

def test_repo_is_alive():
    """
    Simple smoke test so that CI has something to run.
    We'll replace / extend this with real orchestration tests later.
    """
    assert 1 + 1 == 2
```

Run locally:

```bash
pytest
```

You should get 1 passing test.

---

## 5. Add the first CI workflow

Create `.github/workflows/ci-smoke.yml`:

```yaml
name: CI - Smoke Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run pytest
        run: pytest
```

Once you commit & push to GitHub, this will give you a **green checkmark pipeline** for the repo — already something you can point to.

---

## 6. (Optional now) Clean up docs filename

You have `docs/Curren.md` — if that’s just a scratch file, you can rename it:

```bash
mv docs/Curren.md docs/Current-Status.md
```

And maybe drop a quick note there like:

```md
# Current Status

- Stage 1 scaffold created
- CI smoke test workflow added
- Next: design Ansible playbooks + orchestration flow
```

---

### What next?

After you:

1. Paste these file contents
2. Run `pytest` locally
3. Push to GitHub and see CI go green

…send me your updated `tree -C -I ".git" .` and/or a screenshot of the repo, and we’ll move to **Stage 2**:

> define the **Ansible + orchestration story** in a way that mirrors what you did at XPLG but stays generic & portfolio-friendly.



##### Stage 2

Nice, this is the fun part 😊
Stage 2 = give your orchestrator **something real to test**: a small Dockerized service you can bring up/down and hit from tests.

I’ll keep this concrete and copy-pasteable.

---

## 1. Target: a tiny FastAPI “demo system under test”

**Goal:**
Have a container that:

* Exposes `http://localhost:8080/health`
* Exposes `http://localhost:8080/info`
* Is trivial but realistic enough for “modular test orchestration”

### 1.1. Add target app code

Create:

`docker/test-target/app/main.py`

```python
# docker/test-target/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import socket
import os
import time

app = FastAPI(title="Modular Test Orchestrator Demo Target")

START_TIME = time.time()


class EchoRequest(BaseModel):
    message: str


@app.get("/health")
async def health():
    """Simple liveness check."""
    return {"status": "ok"}


@app.get("/info")
async def info():
    """Basic metadata for sanity checks."""
    return {
        "service": "demo-test-target",
        "host": socket.gethostname(),
        "env": os.getenv("APP_ENV", "local"),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@app.post("/echo")
async def echo(body: EchoRequest):
    """Round-trip payload check."""
    return {"echo": body.message}
```

---

## 2. Dockerfile for the target

Create:

`docker/test-target/Dockerfile`

```dockerfile
# docker/test-target/Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn[standard]

COPY app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 3. docker-compose file to run it locally

Create:

`docker/docker-compose.test-target.yml`

```yaml
version: "3.9"

services:
  test-target:
    build:
      context: ./test-target
      dockerfile: Dockerfile
    container_name: modular-test-target
    ports:
      - "8080:8080"
    environment:
      APP_ENV: "local"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 5s
```

> This stays nicely inside `docker/` so later Ansible / CI can just say
> “bring up the test target via this compose file”.

---

## 4. Add a simple smoke test

Under `tests/`, add:

`tests/test_target_smoke.py`

```python
# tests/test_target_smoke.py
import time
from typing import Final

import httpx
import pytest

BASE_URL: Final[str] = "http://localhost:8080"


def wait_for_healthy(timeout: float = 30.0, interval: float = 1.0) -> None:
    """Retry /health until it responds or timeout is hit."""
    deadline = time.time() + timeout
    last_exc: Exception | None = None

    while time.time() < deadline:
        try:
            resp = httpx.get(f"{BASE_URL}/health", timeout=2.0)
            if resp.status_code == 200 and resp.json().get("status") == "ok":
                return
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        time.sleep(interval)

    msg = f"Target service did not become healthy within {timeout}s"
    if last_exc:
        msg += f" (last error: {last_exc})"
    raise RuntimeError(msg)


@pytest.mark.smoke
def test_health_and_info():
    wait_for_healthy()

    health = httpx.get(f"{BASE_URL}/health", timeout=5.0)
    assert health.status_code == 200
    assert health.json().get("status") == "ok"

    info = httpx.get(f"{BASE_URL}/info", timeout=5.0)
    assert info.status_code == 200
    data = info.json()
    assert data["service"] == "demo-test-target"
    assert "uptime_seconds" in data


@pytest.mark.smoke
def test_echo_round_trip():
    wait_for_healthy()

    payload = {"message": "hello-orchestrator"}
    resp = httpx.post(f"{BASE_URL}/echo", json=payload, timeout=5.0)
    assert resp.status_code == 200
    assert resp.json() == {"echo": "hello-orchestrator"}
```

And add `httpx` as a test dependency (either in `requirements-dev.txt` or whatever you’ll use).

---

## 5. How to run this locally

From repo root:

```bash
# 1) Build & start the test target
cd docker
docker compose -f docker-compose.test-target.yml up --build -d

# 2) Run tests from repo root
cd ..
pytest -m smoke -vv

# 3) Tear down when done
cd docker
docker compose -f docker-compose.test-target.yml down
```

If you open a browser to `http://localhost:8080/docs` you should see the small FastAPI app as well.

---

## 6. Why this is a good Stage 2 milestone

With just these pieces you now have:

* A **concrete “system under test”** living under `docker/`
* A **repeatable local workflow**: bring up container → run tests → tear down
* A natural anchor for the *next* steps:

  * CI job that builds this image and runs the smoke tests on GitHub hosted runners
  * Ansible playbooks that can deploy this same container to a remote VM and run the same tests there

If you’d like, next step after you wire this in and test it:

* You send me your updated `tree` and maybe a screenshot of:

  * `docker compose up`
  * `pytest -m smoke` passing

Then we can move to **Stage 3: minimal CI workflow** that uses this target.



Nice 🎉 That screenshot is exactly what we wanted:

* `docker compose … up --build` → test-target container running
* `pytest -m smoke -vv` → both smoke tests **PASSED**
* Only warnings are about the `smoke` mark not being registered.

Let’s clean that up and then wire this into CI in a way that *doesn’t* require a self-hosted runner.

---

## 1️⃣ Silence the `smoke` marker warnings

Edit **`pytest.ini`** at the repo root and make sure it looks like this:

```ini
[pytest]
testpaths = tests

markers =
    smoke: basic smoke tests against the test target
```

Now rerun:

```bash
pytest -m smoke -vv
```

The warnings about `Unknown pytest.mark.smoke` should disappear.

---

## 2️⃣ Document the test-target in `README.md`

Add a small section so recruiters (and Future You) see how this hangs together.

Somewhere under your main intro, add:

````md
## 🧪 Local Test Target

This repo includes a small **FastAPI test target** container and a set of
pytest smoke tests that verify it end-to-end.

**Start the test target:**

```bash
cd docker
docker compose -f docker-compose.test-target.yml up --build
````

This launches a FastAPI app exposing:

* `GET /health` – simple liveness check
* `GET /info` – basic metadata about the running container
* `POST /echo` – round-trip payload echo

**Run the smoke tests:**

```bash
cd ..
pytest -m smoke -vv
```

The smoke suite uses `httpx.AsyncClient` to call the container and assert that
the API behaves as expected.

````

---

## 3️⃣ Add a minimal GitHub Actions workflow (no self-hosted runner needed)

You *can* run this on GitHub’s own runners; no extra setup required.

Create: **`.github/workflows/ci-test-target.yml`**:

```yaml
name: CI - Test Target Smoke

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install test dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest httpx anyio

      - name: Build and run test target
        working-directory: docker
        run: |
          docker compose -f docker-compose.test-target.yml up -d --build
          # give it a few seconds to boot
          sleep 10

      - name: Run smoke tests
        env:
          TEST_TARGET_BASE_URL: http://localhost:8080
        run: |
          pytest -m smoke -vv

      - name: Tear down test target
        if: always()
        working-directory: docker
        run: |
          docker compose -f docker-compose.test-target.yml down
````

This will:

1. Spin up a GitHub-hosted Ubuntu runner.
2. Install Python + pytest/httpx.
3. Build & start your `test-target` container via `docker compose`.
4. Run the `smoke` tests against `http://localhost:8080`.
5. Always tear down the container.

Once you commit + push that, you should see a **“CI - Test Target Smoke”** check appear on PRs and pushes.

---

If you’d like, next we can:

* Add a prettier overview diagram + README polish for this repo, **or**
* Start on the **Ansible orchestration stage** (where we use playbooks instead of shell scripts to run the same flow).


#### after my remarks...

Nice, you’re moving fast 😊

You’re exactly right about the CI error: `httpx` simply isn’t installed on the GitHub runner.

Let’s do your three asks one by one.

---

## 1️⃣ README — Suggested Table of Contents

For **modular-test-orchestrator**, I’d structure the README like this:

```md
# Modular Test Orchestrator

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
```

Then you can fill sections roughly like:

* **Overview** – one-paragraph “what this repo is and why it exists”.
* **Architecture** – short diagram/text: *pytest orchestrator → Docker test target (FastAPI)*; later: *Ansible → remote hosts → pytest*.
* **Repository Layout** – short bullet list of `ansible/`, `docker/`, `orchestrator/`, `tests/`, etc.
* **Local Development** – exact commands for running the compose file and pytest.
* **CI Pipeline** – explain the GH Actions workflow (what it does, when it runs).
* **Ansible Automation (Future Stage)** – a teaser for Stage 3.
* **Roadmap** – checkboxes like “Add Ansible playbooks”, “Add Allure integration”, etc.
* **License** – MIT or whatever you choose.

---

## 2️⃣ Fixing CI: install dependencies from `requirements.txt`

The error:

```text
E   ModuleNotFoundError: No module named 'httpx'
```

means the CI job didn’t install `httpx` (and probably a bunch of other deps).

#### Using requirements.txt 

Since you now have a `requirements.txt`, let’s make the workflow install from that instead of hard-coding packages.

Update your workflow (e.g. `.github/workflows/ci-test-target.yml`) to something like this:

```yaml
name: CI - Test Target Smoke

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        working-directory: ${{ github.workspace }}
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build and run test target
        working-directory: ${{ github.workspace }}/docker
        run: |
          docker compose -f docker-compose.test-target.yml up -d --build
          # give it a few seconds to boot
          sleep 10

      - name: Run smoke tests
        working-directory: ${{ github.workspace }}
        env:
          TEST_TARGET_BASE_URL: http://localhost:8080
        run: |
          pytest -m smoke -vv

      - name: Tear down test target
        if: always()
        working-directory: ${{ github.workspace }}/docker
        run: |
          docker compose -f docker-compose.test-target.yml down
```

Key bits:

* `working-directory: ${{ github.workspace }}` ensures commands run from the repo root.
* `pip install -r requirements.txt` will install `httpx` and all other packages you froze.
* Docker steps run in `…/docker` so the compose file is found.

Once you commit & push this, the next CI run should pass collection and actually run your `smoke` tests.

*(Later we can trim `requirements.txt` down from full `pip freeze` to just the essentials, but it’s fine for now while we’re wiring things up.)*

---

If you’d like, next we can:

* Draft the actual README content using that ToC, **or**
* Add a second CI job (e.g. `pytest -q` for all tests, or `flake8`/`ruff`), so the repo looks even more “production-y” to reviewers.
