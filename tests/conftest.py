from starlette.testclient import TestClient

from main import app

test_client = TestClient(app)

prefix: str = '/api/v1'
