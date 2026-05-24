"""
kenya_agui/server.py

AG-UI server for East African civic agents.
Connects mpesa-mcp and wapimaji-mcp to AG-UI-compatible frontends.

AG-UI Protocol: https://github.com/ag-ui-protocol/ag-ui
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class AGUIEvent:
    """Base AG-UI event following the AG-UI protocol spec."""
    type: str
    data: dict = field(default_factory=dict)


class AGUIEmitter:
    """Emit AG-UI events to the connected frontend."""

    def __init__(self, send: Callable):
        self._send = send

    async def state_update(self, state: dict) -> None:
        """Update shared state — synced to frontend in real time."""
        await self._send(AGUIEvent(type="state_update", data={"state": state}))

    async def render_ui(self, component: str, props: dict) -> None:
        """Trigger generative UI rendering on the frontend."""
        await self._send(AGUIEvent(
            type="render_ui",
            data={"component": component, "props": props}
        ))

    async def stream_text(self, text: str, done: bool = False) -> None:
        """Stream text tokens to the frontend chat interface."""
        await self._send(AGUIEvent(
            type="text_delta" if not done else "text_done",
            data={"text": text}
        ))

    async def request_approval(self, action: str, details: dict) -> None:
        """Human-in-the-loop: request user approval before taking action."""
        await self._send(AGUIEvent(
            type="approval_request",
            data={"action": action, "details": details}
        ))


class KenyaAGUIServer:
    """
    AG-UI server wrapping East African civic agents.

    Example:
        server = KenyaAGUIServer()
        server.run(port=8000)
    """

    def __init__(
        self,
        mpesa: Optional[Any] = None,
        wapimaji: Optional[Any] = None,
    ):
        self.mpesa = mpesa
        self.wapimaji = wapimaji
        self._handlers: list[Callable] = []
        logger.info("KenyaAGUIServer initialised")

    def on_agent_event(self, func: Callable) -> Callable:
        """Register an AG-UI event handler."""
        self._handlers.append(func)
        return func

    async def handle_drought_query(self, county: str, emit: AGUIEmitter) -> None:
        """Built-in handler: stream water stress data to frontend."""
        await emit.stream_text(f"Fetching water stress data for {county}...")
        if self.wapimaji:
            data = await self.wapimaji.get_county_water_stress(county)
            await emit.state_update({"drought_data": data, "county": county})
            await emit.render_ui("DroughtMap", props={"county": county, **data})
            await emit.stream_text(
                f"Water stress for {county}: {data.get('stress_level', 'unknown')}",
                done=True
            )
        else:
            await emit.stream_text(
                "wapimaji-mcp not connected. Install: pip install wapimaji-mcp",
                done=True
            )

    async def handle_mpesa_payment(
        self, phone: str, amount: int, reference: str, emit: AGUIEmitter
    ) -> None:
        """Built-in handler: M-Pesa payment with human-in-the-loop approval."""
        await emit.request_approval(
            action="mpesa_stk_push",
            details={
                "phone": phone,
                "amount_kes": amount,
                "reference": reference,
                "description": f"Payment of KES {amount:,} to {phone}"
            }
        )
        # Approval response handled by frontend AG-UI client
        # On approval: mpesa-mcp.stk_push(phone, amount, reference)

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Start the AG-UI server."""
        try:
            import uvicorn
            from .app import create_app
            app = create_app(self)
            uvicorn.run(app, host=host, port=port)
        except ImportError:
            logger.error("Install uvicorn: pip install uvicorn[standard]")
            raise
