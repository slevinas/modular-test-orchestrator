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
