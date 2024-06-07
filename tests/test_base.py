
from fastapi.testclient import TestClient
from tolik_bot.main import app


client = TestClient(app)


def test_read_root():
    assert (response := client.get("/")).status_code == 200
    assert (body := response.json())
    assert 'TYPE' in body
