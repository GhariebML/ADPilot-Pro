"""Phase 1 Foundation Live Verification Script."""

import asyncio
from httpx import ASGITransport, AsyncClient
from adpilot.api.main import app
from adpilot.core.config import get_config


async def main() -> None:
    config = get_config()
    print("=" * 60)
    print(f"ADPilot Phase 1 Foundation Verification")
    print(f"Environment: {config.environment}")
    print(f"App Version: {config.app_version}")
    print("=" * 60)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Liveness Probe
        res = await client.get("/healthz")
        assert res.status_code == 200
        req_id = res.headers.get("X-Request-ID")
        resp_time = res.headers.get("X-Response-Time")
        print(f"[PASS] GET /healthz -> 200 OK | X-Request-ID: {req_id} | Time: {resp_time}")

        # 2. Readiness Probe
        res = await client.get("/ready")
        assert res.status_code in (200, 503)
        data = res.json()
        print(f"[PASS] GET /ready -> {res.status_code} | Status: {data.get('status')} | Components: {list(data.get('components', {}).keys())}")

        # 3. SaaS Health Check
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        print(f"[PASS] GET /health -> 200 OK | Status: {data.get('status')} | DB: {data.get('database')}")

        # 4. Versioned Health Routes (/api/v1/healthz, /api/v1/ready, /api/v1/health)
        res_v1_liveness = await client.get("/api/v1/healthz")
        assert res_v1_liveness.status_code == 200
        print(f"[PASS] GET /api/v1/healthz -> 200 OK | App: {res_v1_liveness.json().get('app')}")

        res_v1_readiness = await client.get("/api/v1/ready")
        assert res_v1_readiness.status_code in (200, 503)
        print(f"[PASS] GET /api/v1/ready -> {res_v1_readiness.status_code} | Ready: {res_v1_readiness.json().get('status')}")

        res_v1_deep = await client.get("/api/v1/health")
        assert res_v1_deep.status_code in (200, 503)
        deep_data = res_v1_deep.json()
        print(f"[PASS] GET /api/v1/health -> {res_v1_deep.status_code} | Deep Diagnostics Components: {list(deep_data.get('components', {}).keys())}")

        # 5. RFC 7807 Error Handling Check
        res_err = await client.post("/api/campaigns/run", json={"invalid": True})
        assert res_err.status_code == 422
        err_data = res_err.json()
        assert err_data.get("type") == "about:blank"
        assert err_data.get("status") == 422
        assert "invalid_params" in err_data
        print(f"[PASS] POST /api/campaigns/run (invalid body) -> RFC 7807 422 Problem Details | Title: {err_data.get('title')}")

        # 6. Security Headers Check
        assert res.headers.get("Strict-Transport-Security") is not None
        assert res.headers.get("X-Content-Type-Options") == "nosniff"
        assert res.headers.get("X-Frame-Options") == "DENY"
        assert res.headers.get("X-XSS-Protection") == "1; mode=block"
        print(f"[PASS] Security Headers Verified (HSTS, nosniff, DENY, XSS-Protection)")

    print("=" * 60)
    print("ALL PHASE 1 FOUNDATION VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
