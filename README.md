# kenya-agui

> **The first East African implementation of the AG-UI (Agent-User Interaction) protocol.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Protocol: AG-UI](https://img.shields.io/badge/Protocol-AG--UI-purple)](https://github.com/ag-ui-protocol/ag-ui)
[![Protocol: MCP](https://img.shields.io/badge/Protocol-MCP-blue)](https://github.com/gabrielmahia/mpesa-mcp)
[![Protocol: A2A](https://img.shields.io/badge/Protocol-A2A-green)](https://github.com/gabrielmahia/kenya-a2a)
[![Part of East African Decision Infrastructure](https://img.shields.io/badge/Portfolio-East%20African%20Decision%20Infrastructure-orange)](https://gabrielmahia.github.io)

## What is AG-UI?

AG-UI is the third protocol in the modern agent stack — adopted in 2025-2026 by Google, Microsoft, AWS, LangChain, and CrewAI.

```
MCP     — Agent → Tool communication     (mpesa-mcp, wapimaji-mcp)
A2A     — Agent → Agent communication    (kenya-a2a)
AG-UI   — Agent → User/Frontend          (kenya-agui) ← this repo
```

Where MCP connects agents to tools and A2A connects agents to other agents, **AG-UI connects agents to users** — enabling real-time streaming, generative UI, shared state, and human-in-the-loop workflows directly inside web applications.

## What this repo does

`kenya-agui` provides AG-UI bindings for the East African civic agent stack:

- **Streaming civic data** to a React/Next.js frontend in real time
- **Generative UI** — agents dynamically render drought maps, financial dashboards, and county reports inside the interface
- **Human-in-the-loop** — M-Pesa payment confirmation flows with agent-driven approval
- **Shared state** — bidirectional sync between wapimaji-mcp drought data and the UI layer

## Architecture

```
┌─────────────────────────────────────────────────┐
│           React Frontend (AG-UI Client)          │
│  CopilotKit · useAgent hook · Generative UI      │
└───────────────────┬─────────────────────────────┘
                    │ AG-UI protocol (HTTP/WebSocket)
┌───────────────────▼─────────────────────────────┐
│         kenya-agui Backend (AG-UI Server)        │
│  FastAPI · AG-UI event emitter · state sync      │
└───────┬──────────────────────────┬───────────────┘
        │ MCP                      │ A2A
┌───────▼───────┐         ┌────────▼──────┐
│  mpesa-mcp    │         │  kenya-a2a    │
│  wapimaji-mcp │         │  kenya-adk    │
└───────────────┘         └───────────────┘
```

## Quick Start

```bash
pip install kenya-agui
```

```python
from kenya_agui import KenyaAGUIServer
from mpesa_mcp import MpesaMCP
from wapimaji_mcp import WapimajiMCP

server = KenyaAGUIServer(
    mpesa=MpesaMCP(),
    wapimaji=WapimajiMCP(),
)

# Stream drought data to frontend
@server.on_agent_event
async def handle_drought_query(event, emit):
    data = await server.wapimaji.get_county_water_stress("Turkana")
    await emit.state_update({"drought_data": data})
    await emit.render_ui("DroughtMap", props=data)

server.run(port=8000)
```

```jsx
// React frontend
import { useAgent } from '@copilotkit/react'

export function DroughtDashboard() {
  const { agent } = useAgent({ agentId: "kenya_civic" })
  return (
    <div>
      <h1>Kenya Drought Monitor</h1>
      {agent.state.drought_data && (
        <DroughtMap data={agent.state.drought_data} />
      )}
    </div>
  )
}
```

## Protocol Stack — East Africa Complete

Gabriel Mahia is the **first engineer to implement all four major AI agent protocols for East Africa**:

| Protocol | Repo | Status |
|----------|------|--------|
| MCP | [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) | ✅ Live on PyPI |
| A2A | [kenya-a2a](https://github.com/gabrielmahia/kenya-a2a) | ✅ Live |
| Google ADK | [kenya-adk](https://github.com/gabrielmahia/kenya-adk) | ✅ Live |
| AG-UI | [kenya-agui](https://github.com/gabrielmahia/kenya-agui) | 🚧 In progress |

## Roadmap

- [ ] AG-UI server core (FastAPI + event emitter)
- [ ] CopilotKit React bindings
- [ ] M-Pesa payment approval flow (human-in-the-loop)
- [ ] Drought map streaming UI component
- [ ] county-level civic dashboard generative UI
- [ ] Integration with civic-agent-kit

## Related

- [civic-agent-kit](https://github.com/gabrielmahia/civic-agent-kit) — Unified SDK
- [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) — M-Pesa MCP server
- [wapimaji-mcp](https://github.com/gabrielmahia/wapimaji-mcp) — Drought intelligence
- [AG-UI Protocol](https://github.com/ag-ui-protocol/ag-ui) — The open standard

## License

MIT © Gabriel Mahia | [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
