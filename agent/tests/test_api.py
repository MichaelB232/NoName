from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
TOKEN = "test-only-agent-token-not-used-anywhere-000000"


def test_health_is_public() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["success"] is True


def test_audits_reject_missing_service_token() -> None:
    res = client.post("/v1/audits", json={"contract_id": "c1", "organization_id": "o1", "s3_key": "org_o1/x.pdf"})
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "UNAUTHORIZED"


def test_audits_reject_cross_tenant_s3_key() -> None:
    res = client.post(
        "/v1/audits",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"contract_id": "c1", "organization_id": "o1", "s3_key": "org_o2/x.pdf"},
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"


def test_audits_accept_valid_job() -> None:
    res = client.post(
        "/v1/audits",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"contract_id": "c1", "organization_id": "o1", "s3_key": "org_o1/contracts/x.pdf"},
    )
    assert res.status_code == 202
    assert res.json()["data"]["progress_channel"] == "audit-progress:o1:c1"
