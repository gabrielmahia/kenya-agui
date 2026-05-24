"""tests/test_smoke.py — AG-UI server smoke tests."""
from kenya_agui import KenyaAGUIServer, AGUIEmitter, AGUIEvent


def test_server_instantiates():
    server = KenyaAGUIServer()
    assert server is not None
    assert server.mpesa is None
    assert server.wapimaji is None


def test_agui_event_dataclass():
    event = AGUIEvent(type="state_update", data={"county": "Nairobi"})
    assert event.type == "state_update"
    assert event.data["county"] == "Nairobi"


def test_emitter_instantiates():
    sent = []
    async def mock_send(event): sent.append(event)
    emitter = AGUIEmitter(send=mock_send)
    assert emitter is not None


def test_server_registers_handler():
    server = KenyaAGUIServer()

    @server.on_agent_event
    async def my_handler(event, emit): pass

    assert len(server._handlers) == 1
