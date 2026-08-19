import threading
import time
from pathlib import Path

import pytest
import uvicorn
from pact import Verifier

PROVIDER_HOST = "127.0.0.1"
PROVIDER_PORT = 8001
PROVIDER_URL = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
PACT_PATH = str(Path(__file__).parent.parent / "pacts" / "InvoiceConsumer-InvoiceProvider.json")


@pytest.fixture(scope="module", autouse=True)
def provider_server():
    from provider.main import app

    config = uvicorn.Config(app, host=PROVIDER_HOST, port=PROVIDER_PORT, log_level="error")
    server = uvicorn.Server(config)
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    time.sleep(1)
    yield
    server.should_exit = True


def test_provider_verifies_consumer_pact():
    """Provider verifies it satisfies the Consumer-generated Pact contract."""
    verifier = Verifier(provider="InvoiceProvider", provider_base_url=PROVIDER_URL)
    output, _ = verifier.verify_pacts(PACT_PATH)
    assert output == 0
